"""Group scoped alert snapshots into evidence-linked review queues."""

from collections import defaultdict

from runtime import choice, cli, instant, report, rows, strings, text, unique, utc

SEVERITY = {"informational": 0, "low": 1, "medium": 2, "high": 3, "critical": 4}


def analyze(data):
    scope = text(data.get("scope"), "scope")
    evidence = rows(data.get("evidence"), "evidence")
    unique(evidence)
    known = set()
    for item in evidence:
        known.add(item["id"])
        text(item.get("observation"), "evidence.observation")
        text(item.get("source"), "evidence.source")
    alerts = rows(data.get("alerts"), "alerts")
    unique(alerts)
    groups = defaultdict(list)
    for alert in alerts:
        entity = text(alert.get("entity"), "alert.entity")
        severity = choice(alert.get("severity"), list(SEVERITY), "alert.severity")
        timestamp = instant(alert.get("timestamp"), "alert.timestamp")
        refs = strings(alert.get("evidence_ids"), "alert.evidence_ids")
        if not set(refs).issubset(known):
            raise ValueError("alert references unknown evidence")
        groups[entity].append(
            {
                "id": alert["id"],
                "severity": severity,
                "timestamp": utc(timestamp),
                "evidence_ids": refs,
                "title": text(alert.get("title"), "alert.title"),
            }
        )
    findings = []
    for entity, members in sorted(groups.items()):
        priority = max((a["severity"] for a in members), key=SEVERITY.get)
        findings.append(
            {
                "entity": entity,
                "source_priority": priority,
                "status": "analyst_review_required",
                "alert_ids": [a["id"] for a in members],
                "alert_titles": [a["title"] for a in members],
                "first_seen": min(
                    (a["timestamp"] for a in members),
                    key=lambda t: instant(t, "timestamp"),
                ),
                "last_seen": max(
                    (a["timestamp"] for a in members),
                    key=lambda t: instant(t, "timestamp"),
                ),
                "evidence_ids": sorted(
                    {ref for a in members for ref in a["evidence_ids"]}
                ),
                "alerts_without_evidence": [
                    a["id"] for a in members if not a["evidence_ids"]
                ],
            }
        )
    findings.sort(key=lambda item: (-SEVERITY[item["source_priority"]], item["entity"]))
    return report(
        "Alert Triage Agent",
        {
            "scope": scope,
            "alerts": len(alerts),
            "review_groups": len(findings),
            "automatic_dispositions": 0,
        },
        findings,
        [
            "Grouping by caller-supplied entity is an organizational aid, not proof that alerts share a cause.",
            "Priority is inherited from the highest source alert; the tool does not establish incident severity.",
            "Evidence identifiers are checked for existence, not truth. Empty evidence lists remain visible.",
            "No alert is closed, suppressed or marked benign, including alerts from familiar entities.",
        ],
        [
            "Verify entity identity, time range and collection coverage before correlating alerts.",
            "Review supporting observations, benign explanations and contradictory evidence.",
            "Record a reasoned analyst disposition for each alert through the owning system.",
        ],
    )


if __name__ == "__main__":
    cli(analyze, __doc__)

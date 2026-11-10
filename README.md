# Alert Triage Agent

**Turn alert snapshots into a focused analyst review queue.**

A model-agnostic AI agent skill paired with a working Python evidence tool. The skill guides an assistant's analysis; the deterministic tool validates and organizes a local evidence snapshot. The included demo runs offline with no API key or dependencies.

[Agent instructions](SKILL.md) · [Example report](example-report.md) · [Input contract](INPUT.md) · [Portfolio](https://shaized.github.io/)

## Try it in one minute

Requires Python 3.11 or newer.

```sh
git clone https://github.com/shaized/alert-triage-agent.git
cd alert-triage-agent
python3 agent.py example.json
python3 agent.py example.json --format json
python3 -m unittest discover -v
```

**Expected result:** One high-source-priority review group containing two alerts. The alert without supporting evidence remains explicitly unresolved.

## Use it as an AI agent

Open the repository in an assistant that can read local files and run Python, then give it this request:

> Read SKILL.md and follow its workflow. Triage the synthetic alerts in example.json. Use the local queue, identify missing evidence and explain what an analyst should verify before assigning a disposition.

SKILL.md is the agent entry point. INPUT.md defines the evidence contract. agent.py performs the domain-specific analysis; runtime.py handles bounded JSON input, validation and report rendering. The assistant can explain the results, investigate alternatives and identify missing evidence using the tools you authorize.

The Python command itself is **not an LLM runtime**. It makes no network calls and performs no operational actions. There is no bundled model, production connector, autonomous service or implied access to your environment.

## What the agent does

1. Clarify the alert scope, source rule, entity identifiers and timestamps. Check whether the evidence covers the event and relevant surrounding activity.
2. Run agent.py to build an entity-based queue. Source priority is inherited from the highest alert and is not a new incident severity verdict.
3. Assess supporting observations, benign explanations and contradictory evidence. Familiar names, known tools and prior false positives are context, not proof of authorization.
4. Return a reasoned disposition proposal per alert, with evidence references and gaps. Never turn grouping alone into a common-cause claim or automatic closure.

## Design

```text
Selected evidence → validated local tool → traceable report
                                             ↓
                         AI-assisted reasoning → analyst decision
```

The examples are original, vendor-neutral implementations. All bundled data is fictional. Results retain unknowns and evidence gaps rather than presenting missing data as reassurance. Read the input contract for exact matching, thresholds and limitations.

## Validate and extend

The test suite covers the example, meaningful boundary cases, invalid evidence references where applicable, timestamp handling, bounded input and safe Markdown output. GitHub Actions runs the same offline tests. To add a real integration, produce the documented input shape in a separately reviewed adapter; keep credentials and operational evidence outside this repository.

Use the authoritative alert definition and original telemetry for a real investigation. A vendor-neutral example cannot establish the semantics of a particular SIEM field.

## Contributing and security

See [CONTRIBUTING.md](CONTRIBUTING.md) and [SECURITY.md](SECURITY.md). Use synthetic fixtures in issues and pull requests. This is a focused reference implementation; validate it against your data and review workflow before operational use.

## License

[MIT](LICENSE) · Built by [Shai Zaidenberg](https://github.com/shaized)

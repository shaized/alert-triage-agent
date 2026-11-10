# Input and output contract

## Input

The root requires scope, evidence and alerts. Evidence items need unique id, source and observation. Alerts need unique id, entity, title, timestamp with offset, severity (informational/low/medium/high/critical) and evidence_ids. Empty evidence_ids is allowed and explicitly reported; unknown references fail. Entity IDs must be unambiguous within the caller's scope. Grouping does not impose a time-window correlation.

See [example.json](example.json) for a complete fictional input. All demo identities, indicators, events, products and reputation providers are synthetic. Documentation IPs and example domains are not threat intelligence.

Input must be a UTF-8 JSON object no larger than 2 MiB. Duplicate JSON keys, malformed required fields, ambiguous timestamps and conflicting identifiers are rejected. Timestamps require an explicit UTC offset. Small local snapshots are the intended workload; there is no streaming, database or production connector in this version.

## Output

`python3 agent.py INPUT.json` emits Markdown. Add `--format json` for structured output. The JSON envelope contains schema_version, agent, summary, findings, limitations and next_steps. The tool writes to standard output and does not modify the source input. Input errors return exit code 2; a valid assessment returns 0 even when findings are present.

JSON preserves evidence text. Markdown renders evidence as literal escaped text, so input cannot inject links, headings or HTML into the report. Every result preserves substantive limitations.

## Example interpretation

One high-source-priority review group containing two alerts. The alert without supporting evidence remains explicitly unresolved.

Use the authoritative alert definition and original telemetry for a real investigation. A vendor-neutral example cannot establish the semantics of a particular SIEM field.

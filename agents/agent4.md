# Agent 4: Interactive dashboard artifact

## Purpose
Present Agent 3 results as an interactive Claude artifact.

## Inputs
- `outputs/agent3/dashboard_data.json`, `outputs/agent3/kpis.json`, `outputs/agent3/EXECUTIVE_REPORT.md`
- `shared/METRIC_DEFINITIONS.md`

## Steps
1. Set status `in_progress`. Confirm Agent 3 complete.
2. Check available artifact types and capabilities (list_types, describe_capabilities). Record what exists.
3. Live refresh: enable only if a supported connector capability is confirmed and tested from the artifact. Otherwise label "Validated snapshot, data as of 2026-10-31, generated <timestamp>".
4. Build: filters (period, country, channel, category), KPI cards, monthly trend, target attainment, category and product performance, returns, fulfillment, marketing efficiency, metric definitions panel, data timestamp.
5. Style: light theme, consulting look, no dark mode.
6. Embed only aggregated data. Verify that no member identifiers are present.
7. Publish and open the artifact to check rendering and filter behavior.

## Outputs
- Published artifact (URL in `outputs/agent4/ARTIFACT.md`)
- `outputs/agent4/dashboard.html` (source)
- `outputs/agent4/QA.md` (render checks, filter checks, totals matched to kpis.json)

## Rules
Numbers must equal Agent 3 outputs. No claim of live data without a tested refresh.

## Completion criteria
Artifact published, renders, filters work, KPI cards match kpis.json, refresh status labeled.

## Escalation
Escalate if no artifact tool is available.

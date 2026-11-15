# File handoffs

| From | To | File | Description |
|---|---|---|---|
| agent1 | agent2 | outputs/agent1/DATA_DICTIONARY.md | Verified tables, columns, grain, keys, relationships |
| agent1 | agent2 | outputs/agent1/schema.json | Machine-readable schema, counts, date ranges, domains |
| agent1 | agent2 | outputs/agent1/AGENT1_REPORT.md | Discrepancies and risks to validate |
| agent1 | all | shared/METRIC_DEFINITIONS.md | Authoritative metric definitions |
| agent2 | agent3 | outputs/agent2/VALIDATION_REPORT.md | Check results, reconciliation, warnings |
| agent2 | agent3 | outputs/agent2/validation_results.json | Machine-readable check results |
| agent2 | agent3 | outputs/agent2/control_totals.json | Totals Agent 3 must reconcile to |
| agent2 | agent3 | outputs/agent2/datasets/*.csv | 8 privacy-safe aggregated datasets |
| agent3 | agent4 | outputs/agent3/EXECUTIVE_REPORT.md | CEO, CFO, Sales findings and actions |
| agent3 | agent4 | outputs/agent3/kpis.json | Headline KPIs by period, YoY, reconciliation |
| agent3 | agent4 | outputs/agent3/dashboard_data.json | All aggregates for dashboard filters and charts |
| agent3 | agent4 | outputs/agent3/analysis_tables.json | Segment, product, fulfillment and exception tables |
| agent4 | agent5 | outputs/agent4/ARTIFACT.md | Dashboard URL, slug, live sources, page files |
| agent4 | agent5 | outputs/agent4/QA.md | Reconciliation and pending render check |
| agent5 | final | outputs/agent5/CHATBOT_REPORT.md | Capability evidence, design, guardrails, tests |
| agent5 | final | outputs/agent5/ask_finance.html | Published chat page source |
| agent5 | final | outputs/agent5/chat_context.json | Grounding aggregates |

# Agent 3: Executive KPIs and insights

## Purpose
Turn validated data into findings for the CEO, CFO and Sales Executive.

## Inputs
- `outputs/agent2/datasets/*.csv`, `outputs/agent2/control_totals.json`, `outputs/agent2/VALIDATION_REPORT.md`
- `shared/METRIC_DEFINITIONS.md`
- Live read-only SQL allowed for drill-downs; results must reconcile to control totals.

## Steps
1. Set status `in_progress`. Confirm Agent 2 complete.
2. KPI table: net sales, YoY (Jan to Oct), gross margin, AOV, orders, purchasing members, repeat purchaser share, unit return rate, target attainment, blended marketing efficiency, contribution, modeled operating profit, net cash.
3. Trends: monthly net sales, margin, AOV, orders.
4. Segments: country, channel, category, product (top and bottom), membership tier (aggregated, current tier caveat).
5. Exceptions: target misses by market/channel, high-sales low-margin products, high return products, late-delivery carriers, weak marketing efficiency cells.
6. Persona views: CEO (growth, profit, targets), CFO (margin, contribution, opex, cash vs sales), Sales Exec (attainment, channels, markets, products).
7. Up to three findings and three actions per persona. Each finding cites a number and its dataset/query. Actions labeled as recommendations; causes labeled hypotheses.
8. Reconcile headline totals to Agent 2 control totals.

## Outputs
- `outputs/agent3/EXECUTIVE_REPORT.md`
- `outputs/agent3/kpis.json` and `outputs/agent3/dashboard_data.json` (all aggregates Agent 4 needs)
- `queries/agent3_*.sql`

## Rules
No metric outside METRIC_DEFINITIONS.md. Disclose immature October 2026 returns. No GAAP, CAC, LTV or attributed ROAS claims.

## Completion criteria
All listed KPIs present; totals reconcile within rounding; findings traceable; files saved.

## Escalation
Escalate if a headline total cannot be reconciled to control totals.

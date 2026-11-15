# Agent 4 QA

Run date: 2026-11-14 UTC.

## Query reconciliation (stored queries executed exactly as stored, wrapped in totals)

| Source | Check | Live result | Control total (Agent 2) | Match |
|---|---|---:|---:|---|
| sales | net sales | 1,904,880.71 | 1,904,880.71 | yes |
| sales | net COGS | 1,040,876.79 | 1,040,876.79 | yes |
| sales | completed / cancelled orders | 6,543 / 306 | 6,543 / 306 | yes |
| sales | net sales target | 1,960,183.79 | 1,960,183.79 | yes |
| sales | marketing spend | 161,310.85 | 161,310.85 | yes |
| sales | distinct gross margin targets | 1 | 1 (0.42) | yes |
| opex | fixed operating expense | 118,905.60 | 118,905.60 | yes |
| category | net sales | 1,904,880.71 | 1,904,880.71 | yes |
| products | net sales | 1,904,880.71 | 1,904,880.71 | yes |
| fulfillment | late deliveries | 2,627 (40.6% of 6,476) | 40.6% | yes |
| cash | net cash | 2,140,505.56 | 2,140,505.56 | yes |
| returns | merchandise refunds | 132,304.61 | 132,304.61 | yes |
| members | Jan to Oct 2026 purchasers | 1,329 | 1,329 | yes |

## Expected headline values on first open (Jan to Oct 2026, all markets and channels)
Net sales 1,005,633.46 (+46.2%), gross margin 46.0% (+1.4 pts), modeled operating profit 311,563.89 (+63.0%), orders 3,415 (+42.4%), AOV 294.48 (+2.7%), attainment 98.0% (-2.0 pts vs plan).

## Privacy
No query selects member_name or email. member_id is used only inside SQL to count distinct members; only counts leave the database, and groups under 5 are withheld.

## Render check
First open (2026-11-14 02:48 UTC): failed. All sources stopped in the loader because the execute_sql answer names the untrusted-data tag in its preamble before the real block; three signal cards were drawings containing drawings. Fixed: loader now reads the block that ends at the closing tag; signal colors set from onData.
Second open (2026-11-14 02:50 UTC): passed, no runs faults, no mark mismatches. Displayed: net sales $1,005,633 (+46.2%), gross margin 46.0% (+1.4 pts), modeled operating profit $312K (+63.0%), orders 3,415 (+42.4%), AOV $294 (+2.7%), attainment 98.0% (-2.0 pts vs plan), market table total -$20K vs $1.03M target. All match Agent 3.
Not individually exercised by the check: hidden tabs (Sales, Profitability, Customers, Products, Fulfillment) and non-default filters. They use the same reconciled calculations.

# Agent 2 validation report

Status: complete_with_warnings. Run date: 2026-11-13. Source: `dev` schema, project wcbosypmsdvzfqrktsfk. All checks read-only SELECT.

## Result
49 checks passed, 0 failed, 6 warnings (all explained, none blocking). Payments reconcile to the cent. Every exported dataset reproduces the control totals exactly.

## Checks

| Group | Checks | Result |
|---|---|---|
| Duplicates (keys, business keys, grain of monthly tables) | 14 | All 0 |
| Orphans (every FK plus orders without lines) | 7 | All 0 |
| Business rules (cancelled vs cash and shipping, returns vs sales, refunds vs returns, cost vs price) | 10 | All 0 |
| Date validity (sequence, snapshot cutoff, join date) | 10 | All 0 |
| Payment reconciliation | 2 | 0 mismatched orders, max diff 0.00 |
| Join accuracy (row counts before and after) | 4 | No fan-out on grain-safe joins |
| Export control totals and privacy | 2 | Exact match, no identifiers |

Full list with IDs: `validation_results.json`.

## Payment reconciliation

| Item | Expected from orders and returns | Payments table | Diff |
|---|---:|---:|---:|
| Captures (merchandise booked + tax + shipping), 6,543 completed orders | 2,287,410.51 | 2,287,410.51 | 0.00 |
| Refunds (merchandise refund + tax refund) | 146,904.95 | 146,904.95 | 0.00 |

Bridge from net sales to net cash: net sales 1,904,880.71 + merchandise refunds 132,304.61 = booked 2,037,185.32; + tax 229,362.50 + shipping 20,862.69 = captures 2,287,410.51; minus refunds 146,904.95 (merchandise 132,304.61 + tax 14,600.34) = net cash 2,140,505.56.

## Join accuracy

| Join | Before | After |
|---|---:|---:|
| Completed lines left join returns | 16,535 | 16,535 |
| Completed orders left join shipments | 6,543 | 6,543 |
| Completed orders left join payments aggregated per order | 6,543 | 6,543 |
| Completed orders inner join raw payments (anti-pattern) | 6,543 | 7,659 |
| Month x country x channel order cells vs target cells | 330 | 330 matched both ways |

## Warnings

| ID | Finding | Count | Handling |
|---|---|---:|---|
| NUL01 | Null shipped_date | 12 | All on orders dated 2026-10-31. Excluded from ship-time metrics |
| NUL02 | Null delivered_date | 67 | Orders from 2026-10-25 on, in transit. Excluded from delivery metrics |
| NUL03 | Undelivered and past promise date | 1 | Not counted late; outcome unknown |
| FAN01 | Raw payment join fan-out | 1,116 extra rows | Payments aggregated per order in all datasets |
| IMM01 | October 2026 returns immature | n/a | Flag in return comparisons |
| OPS01 | About 40% of delivered shipments are later than promised | n/a | Data consistent; passed to Agent 3 as a business finding |

## Control totals (completed orders, 2025-01-01 to 2026-10-31)

| Metric | Value |
|---|---:|
| Completed orders | 6,543 |
| Cancelled orders excluded (booked value 92,717.79) | 306 |
| Units sold / returned | 21,525 / 1,414 |
| Gross sales | 2,195,043.17 |
| Line discount | 157,857.85 |
| Merchandise refunds | 132,304.61 |
| Net sales | 1,904,880.71 |
| Net COGS | 1,040,876.79 |
| Gross profit | 864,003.92 |
| Gross margin | 45.36% |
| AOV | 291.13 |
| Contribution before marketing | 845,703.80 |
| Marketing spend | 161,310.85 |
| Fixed operating expense | 118,905.60 |
| Modeled operating profit | 565,487.35 |
| Net sales target / attainment | 1,960,183.79 / 97.18% |
| Net cash | 2,140,505.56 |
| Purchasing members / repeat purchasers | 1,417 / 1,251 |

Machine-readable: `control_totals.json`.

## Datasets (`datasets/`)

| File | Grain | Rows | Notes |
|---|---|---:|---|
| fact_month_country_channel.csv | month x shipping country x channel | 330 | Sales, returns, COGS, order-level fees summed once per order, targets, marketing. Additive except none of the member counts (removed) |
| fact_month_category.csv | month x category | 110 | Line-level sales, returns, COGS. `orders` is distinct orders containing the category; not additive across categories |
| fact_product.csv | product | 60 | Full period plus Jan to Oct 2025 and Jan to Oct 2026 splits |
| fact_month_country_opex.csv | month x country | 110 | Fixed operating expense |
| fact_month_cash.csv | payment month | 22 | Captures, refunds, net cash by payment_date |
| fact_month_carrier_fulfillment.csv | order month x carrier | 66 | Late = delivered after promise; day sums for averages |
| fact_category_return_reason.csv | category x reason | 15 | Return events, units, refunds |
| agg_purchasing_members.csv | period x dimension | 70 | Distinct purchasers and repeat purchasers (2+ completed orders) computed in SQL; smallest cell 81 |

## Privacy
No member_id, member_name, email or order_number in any export (scan passed). Member-level logic ran only inside SQL. Purchasing-member counts were removed from the 330-cell fact table because 1 to 4 member cells exist; they are provided only at coarser grain where the smallest cell is 81.

# Metric definitions (authoritative)

Source: README.md metric definitions, adopted unchanged. Scope for every sales metric: `order_status = 'completed'`. Period assignment by `order_date` unless stated.

| Metric | Definition |
|---|---|
| Gross sales | sum(quantity x unit_price_usd) on completed order lines |
| Line discount | sum(discount_usd) on completed order lines |
| Booked merchandise sales | gross sales minus line discount |
| Merchandise refunds | sum(returns.merchandise_refund_usd), assigned to the original order month |
| Net sales | booked merchandise sales minus merchandise refunds. Excludes tax and shipping |
| Net COGS | (quantity minus returned_quantity) x unit_cost_usd. Returned goods are restocked |
| Gross profit | net sales minus net COGS |
| Gross margin | total gross profit / total net sales. Never average percentages |
| AOV | net sales / distinct completed orders (fully returned orders stay in denominator) |
| Contribution before marketing | gross profit + shipping_fee_usd minus fulfillment_cost_usd (order level, summed once per order) |
| Contribution after marketing | contribution before marketing minus marketing_spend_usd |
| Modeled operating profit | contribution after marketing minus fixed_operating_expense_usd. Not GAAP |
| Target attainment | net sales / net_sales_target_usd, targets summed once at month x country x channel grain |
| Unit return rate | returned units / completed-order units. Recent cohorts immature |
| Repeat purchaser share | members with 2+ completed orders in period / purchasing members in period. Not retention |
| Blended marketing efficiency | net sales / marketing spend. Not attributed ROAS. No CAC |
| Net cash | captures minus refunds by payment_date. Includes tax and shipping |
| Late delivery rate | delivered shipments with delivered_date > promised_delivery_date / delivered shipments |
| Days to deliver | delivered_date minus order_date, delivered shipments only |
| YoY | matching months only: Jan to Oct 2026 vs Jan to Oct 2025 |

Purchasing members are non-additive across months, channels and markets. Recompute distinct counts at the requested grain.

# Agent 1 report

Status: complete_with_warnings. Run date: 2026-11-13.

## Summary
All 13 tables exist in schema `dev`, are readable, and match the local data_dictionary.md for column names and row counts. Keys, foreign keys and check constraints are declared and listed in DATA_DICTIONARY.md and schema.json.

| Table | Exact rows | Date coverage |
|---|---:|---|
| ecommerce_countries | 5 | |
| ecommerce_channels | 3 | |
| ecommerce_categories | 5 | |
| ecommerce_products | 60 | |
| ecommerce_members | 1,500 | joined 2024-07-01 to 2026-05-30 |
| ecommerce_orders | 6,849 | ordered 2025-01-01 to 2026-10-31 |
| ecommerce_order_items | 17,290 | via orders |
| ecommerce_payments | 7,659 | paid 2025-01-01 to 2026-10-31 |
| ecommerce_returns | 1,219 | returned 2025-01-12 to 2026-10-31 |
| ecommerce_shipments | 6,543 | shipped 2025-01-02 to 2026-10-31 |
| ecommerce_sales_targets | 330 | 2025-01 to 2026-10 |
| ecommerce_marketing_monthly | 330 | 2025-01 to 2026-10 |
| ecommerce_operating_expenses | 110 | 2025-01 to 2026-10 |

## Discrepancies against README.md and data_dictionary.md
1. Schema is `dev`, not `public` as README states. All SQL must use `dev.`.
2. The four reporting views in README are not present. Agent 2 and 3 must rebuild their logic in SQL.
3. Row counts and columns match the local dictionary exactly. No other discrepancies.

## Facts Agent 2 must use
- Cancelled orders: 306. They have order lines but no payments or shipments (6,543 orders with payments and with shipments equals the completed count; Agent 2 must confirm these are the same orders).
- Captures 6,543 and refunds 1,116; refund count is close to return count 1,219, so some orders have multiple returned lines in one refund. Agent 2 to reconcile.
- 12 shipments without shipped_date and 67 without delivered_date. Expected per dictionary; exclude from delivery-time and late-rate metrics.
- promised_delivery_date extends to 2026-11-05 (future). Not an error.
- 73 members never ordered (1,500 minus 1,427).
- All date columns are native `date`; no text-date conversion needed. No mixed-case identifiers.

## Risks and warnings
- W1: Connector runs as role `postgres` with write privileges and RLS bypass. Read-only is enforced by pipeline rules only. Recommend a dedicated read-only role for production use.
- W2: Membership tier is current, not historical. Tier segmentation describes today's tier.
- W3: October 2026 returns are immature.

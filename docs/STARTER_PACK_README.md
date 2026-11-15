# Ecommerce data agent starter pack

A fictional direct-to-consumer retailer, Summit Commerce. Designed for CEO, CFO and sales leadership questions. This is not Netflix, Apple or Amazon data and does not reproduce their business models.

## Scope

- Order history: January 1, 2025 through October 31, 2026. Snapshot: October 31, 2026.
- 1,500 members, 60 products, 6,849 orders and 17,290 order lines.
- Five markets: US, Canada, UK, Germany and India. Three transaction channels.
- All amounts already in USD. No FX conversion is required.
- Includes cancellations, discounts, partial returns, refunds and late deliveries.
- October 2026 is a complete order month, but late-month returns have not fully matured.
- No inventory, balance sheet, subscription billing, seller marketplace commissions or accounts receivable. This pack supports retail sales and a simplified operating profit model.

## Setup in Supabase

1. Use a fresh demo project. Run `01_schema.sql` in the SQL Editor. Tables are in `public`, prefixed `ecommerce_`. The script creates tables, primary keys, foreign keys, constraints and indexes. It does not drop existing objects.
2. Import each CSV into its matching existing table through Table Editor > Insert > Import Data from CSV. Follow the numbered CSV order below. Empty shipment dates represent NULL, not empty strings. Do not create replacement tables from the CSVs.
3. Alternatively, from a terminal with PostgreSQL psql installed, change into this extracted folder and run `psql "$DATABASE_URL" -v ON_ERROR_STOP=1 -f 02_import_psql.sql`. Use your own database connection string privately. The backslash-copy commands do not run in SQL Editor. Choose CSV import OR psql import, not both.
4. Run `03_reporting_views.sql`, then `05_validation.sql` in SQL Editor.
5. Give the agent the prompt in `claude_agent_instructions.md` and the dictionary. Start by asking it to list the available ecommerce tables and count the orders. Do not assume the connector exposes every schema or view; verify through the connection you have configured.
6. Use `04_executive_queries.sql` for example questions and SQL.

CSV import reference: https://supabase.com/docs/guides/database/import-data

## Access

Tables have RLS enabled with no public policies. Reporting views use PostgreSQL security_invoker. SQL Editor can be used by the project owner. An agent connection needs deliberate read permissions and an appropriate database role or RLS policy; no anonymous access, blanket public SELECT policy, passwords or connector configuration is supplied. Database/SQL connector access and Supabase REST access can behave differently. The Supabase connector in your Claude setup has not been tested here. Use a read-only connection for reporting if your connector supports it.

## Import order and row counts

| Order | Table | Rows |
|---|---|---:|
| 01 | ecommerce_countries | 5 |
| 02 | ecommerce_channels | 3 |
| 03 | ecommerce_categories | 5 |
| 04 | ecommerce_products | 60 |
| 05 | ecommerce_members | 1,500 |
| 06 | ecommerce_orders | 6,849 |
| 07 | ecommerce_order_items | 17,290 |
| 08 | ecommerce_payments | 7,659 |
| 09 | ecommerce_returns | 1,219 |
| 10 | ecommerce_shipments | 6,543 |
| 11 | ecommerce_sales_targets | 330 |
| 12 | ecommerce_marketing_monthly | 330 |
| 13 | ecommerce_operating_expenses | 110 |

## Reporting views

| View | Grain | Use |
|---|---|---|
| ecommerce_item_sales | Completed order line | Product, category, returns, gross margin |
| ecommerce_order_sales | Completed order | AOV, customers, shipping and contribution |
| ecommerce_monthly_performance | Month x market x channel | Target attainment, marketing efficiency |
| ecommerce_monthly_executive | Month | CEO/CFO sales and modeled operating profit |

## Relationships

- countries → members and orders (shipping market).
- categories → products → order_items.
- members → orders → order_items, payments and shipments.
- order_items → returns (zero or one return event in this sample).
- countries + channels → sales_targets and marketing_monthly, by month.
- countries → operating_expenses, by month.

Refer to `01_schema.sql` for the exact declared foreign keys. Do not join monthly targets directly to order lines and then sum targets.

## Metric definitions

- Gross sales = quantity × historical unit selling price. Completed orders only.
- Booked merchandise sales = gross sales − line discount.
- Net sales = booked merchandise sales − merchandise refunds. Excludes tax and shipping. Returns are assigned back to the original order month, using information known at snapshot date.
- Net COGS = (sold units − returned units) × historical unit cost. Every returned item is restocked in this simplified model.
- Gross profit = net sales − net COGS. Gross margin = total gross profit / total net sales.
- AOV = net sales / distinct completed orders. Includes fully returned orders in the denominator.
- Contribution before marketing = gross profit + shipping fees − fulfillment cost.
- Contribution after marketing subtracts allocated marketing spend. Modeled operating profit then subtracts fixed operating expenses. No depreciation, interest, income tax or complete corporate overhead model is provided.
- Target attainment = net sales / net sales target. Sum targets once at their own grain.
- Unit return rate = returned units / completed-order units. Recent order cohorts have less time to return.
- Repeat purchaser share = members with 2+ completed orders / purchasing members in the selected period. Do not call it retention.
- Blended marketing efficiency = net sales / allocated marketing spend. No campaign-level attribution or attributed ROAS is available. No reliable attributed CAC is available.
- Net cash = captures − refunds, reported by payment date. Includes tax and shipping and therefore differs from net merchandise sales.
- Purchasing members are non-additive across channels and months. Recompute distinct members from orders for the requested period.
- YoY comparisons must use matching months: Jan–Oct 2026 vs Jan–Oct 2025. No 2026 November/December data exists.

## Verification

Delivered CSVs were loaded locally with primary/foreign keys, uniqueness and row constraints enabled. Return quantities, payment reconciliation and reporting view totals passed. See `validation_results.json`. Core relational/view logic was executed in SQLite with syntax adaptation. PostgreSQL-specific RLS and security_invoker statements, psql import commands and example PostgreSQL date functions were not executed against a live Supabase instance. Run the included SQL validation after import.

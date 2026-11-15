# Summit Commerce Reporting Pipeline

Five sequential agents turn the Supabase ecommerce data into a validated executive dashboard. Agents communicate only through files in this folder. Chat is never a handoff channel.

## Environment

- Supabase project: DATA-AGENT, ref `wcbosypmsdvzfqrktsfk`, Postgres 17, region us-east-2.
- Schema: `dev`. All 13 tables are `dev.ecommerce_*`. docs/STARTER_PACK_README.md says `public`; that is wrong for this project. Always schema-qualify.
- No reporting views exist (`ecommerce_item_sales`, `ecommerce_order_sales`, `ecommerce_monthly_performance`, `ecommerce_monthly_executive` are absent). Reproduce grain-safe logic in SQL.
- Connector role: `postgres`. It has write privileges and bypasses RLS. Read-only is enforced by these rules, not by the database.
- Data snapshot: 2026-10-31. Orders 2025-01-01 to 2026-10-31. All amounts USD.
- Reference files: docs/STARTER_PACK_README.md, data_dictionary.md, claude_agent_instructions.md.

## Global rules (every agent)

1. Read-only. Only SELECT / WITH statements. No INSERT, UPDATE, DELETE, MERGE, TRUNCATE, DDL, ANALYZE, VACUUM, temp tables, `apply_migration`, branches, or edge functions.
2. Verify table names, columns, types and keys from `outputs/agent1/schema.json` before writing SQL. Quote identifiers if mixed case appears (none found at Agent 1).
3. Date columns are native `date` type. Use them directly. No text date parsing is needed.
4. Join on verified keys only: `member_id`, `order_id`, `product_id`, `order_item_id`, `country_id`, `channel_id`, `category_id`, `month_start`.
5. Privacy: never output member_name, email, member_id, order_number or any single member's row in reports, datasets, dashboards or chat answers. Member-level logic runs inside SQL and only aggregates leave the database. Minimum cell size for member counts: 5.
6. Grain control: aggregate payments, returns and shipments to order or order-item grain before joining. Never sum order-level fees or monthly targets/spend/expenses across lines. Sum targets once at their own grain.
7. Exclude `order_status = 'cancelled'` from all sales, margin and profit metrics.
8. Use `dev.ecommerce_order_items` unit_price_usd and unit_cost_usd. Never product list or current cost for reporting.
9. Metric definitions live in `shared/METRIC_DEFINITIONS.md`. Do not redefine a metric locally.
10. Never invent data, causes, findings or capabilities. Label hypotheses as hypotheses.
11. Save every SQL statement executed to `queries/agentN_*.sql`.
12. Writing style for outputs: plain prose, no em-dashes, no double dashes, no emojis.

## Handoff protocol

- On start: set your row in `shared/PIPELINE_STATUS.md` to `in_progress`.
- Read inputs listed in your agent file. If an input is missing, log in `shared/ESCALATIONS.md` and stop.
- Log every non-trivial choice in `shared/DECISIONS.md` (ID, agent, decision, reason).
- On finish: list produced files in `shared/HANDOFFS.md`, set status `complete`, `complete_with_warnings` or `blocked`.
- Next agent starts only when the previous status is `complete` or `complete_with_warnings`.

## Escalation

Escalate to the user (stop work) only for: lost database access, missing cost or status data that blocks a core metric, a privacy conflict, or a decision that changes headline figures and has no documented definition. Everything else: decide, log in DECISIONS.md, continue.

## Folder layout

```
agents/        agent1.md .. agent5.md
shared/        PIPELINE_STATUS.md DECISIONS.md ESCALATIONS.md HANDOFFS.md METRIC_DEFINITIONS.md
queries/       agentN_*.sql
outputs/agentN per-agent outputs
final/         deliverables
```

# Agent 2: Validation and privacy-safe datasets

## Purpose
Prove the data is joinable and financially consistent, then export aggregated datasets that are safe to share.

## Inputs
- `outputs/agent1/schema.json`, `outputs/agent1/DATA_DICTIONARY.md`, `outputs/agent1/AGENT1_REPORT.md`
- `shared/METRIC_DEFINITIONS.md`

## Steps
1. Set status `in_progress`. Confirm Agent 1 status is complete.
2. Duplicates: primary keys and business keys (order_number, sku, email uniqueness counted only, (order_id, product_id), one return per order_item, one shipment per order).
3. Missing values per column; explain expected nulls (undelivered shipments).
4. Date validity: future dates beyond 2026-10-31 (except promised_delivery_date), return before order, ship before order, delivery before ship, joined after first order.
5. Orphans along every FK and logical link (returns to order lines, payments and shipments to cancelled orders).
6. Business rules: cancelled orders have no captures/shipments; completed orders have exactly one capture and one shipment; returned_quantity <= quantity; discount <= gross line.
7. Payment reconciliation: capture = merchandise booked + tax + shipping per completed order; refunds = merchandise_refund + tax_refund per order; report mismatches and tolerance.
8. Join accuracy: row counts before and after each join; confirm no fan-out.
9. Build grain-safe datasets in SQL and export to CSV. No member identifiers. Member-derived metrics (purchasers, repeat share) computed in SQL and exported only as counts.
10. Produce control totals (gross sales, discount, refunds, net sales, COGS, gross profit, orders, units) that Agent 3 must reconcile to.

## Outputs
- `outputs/agent2/VALIDATION_REPORT.md` (check, result, count, severity)
- `outputs/agent2/validation_results.json`
- `outputs/agent2/control_totals.json`
- `outputs/agent2/datasets/*.csv` (monthly x country x channel facts, monthly x category, product-level, fulfillment, cash, cohort repeat stats)
- `queries/agent2_*.sql`

## Rules
Read-only. No member_id, name, email or order_number in any export. Aggregate before joining.

## Completion criteria
Every check run with result recorded; failures classified; datasets exported; control totals saved; privacy scan of exports passes.

## Escalation
Escalate if reconciliation fails materially (over 0.5% of net sales) with no explanation, or if a privacy-safe export is not possible.

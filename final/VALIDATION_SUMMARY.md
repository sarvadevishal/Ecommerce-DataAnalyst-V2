# Validation summary

| Stage | Result |
|---|---|
| Agent 1 schema | 13 tables in schema dev; columns and row counts match data_dictionary.md; all date columns native date; USD only |
| Agent 2 data checks | 49 pass, 0 fail, 6 explained warnings (duplicates, orphans, business rules, dates, joins, exports, privacy) |
| Payment reconciliation | captures 2,287,410.51 and refunds 146,904.95 match to 0.00 per order |
| Agent 3 KPIs | reconcile exactly to control totals; category and product sums equal net sales 1,904,880.71 |
| Agent 4 live queries | 9 stored queries executed as stored; net sales, COGS, orders, targets, marketing, opex, cash, refunds match control totals |
| Agent 4 dashboard check | passed on second render; headline figures equal Agent 3 |
| Agent 5 chat | grounding JSON parses, page script compiles, no personal identifiers; live answer tests pending first use |
| Privacy | no member names, emails, IDs or order numbers in any output, dataset, dashboard or chat context; member counts under 5 withheld |

# Decisions log

| ID | Agent | Decision | Reason |
|---|---|---|---|
| D00 | setup | Pipeline runs sequentially in one session; no parallel subagents. | User instruction. |
| D01 | agent1 | Use schema `dev` for all queries. | Live metadata shows tables only in dev; README says public. |
| D02 | agent1 | Rebuild reporting view logic in SQL instead of using views. | Views from README do not exist in the project. |
| D03 | agent1 | Adopt README metric definitions unchanged as shared/METRIC_DEFINITIONS.md. | Provided by data owner; consistent with user rules. |
| D04 | agent1 | Treat member_id and order_number as identifiers that must not be exported. | User privacy rule covers individual member identifiers. |
| D05 | agent1 | No currency conversion. | Check constraint enforces currency_code = USD; 6,849 of 6,849 orders USD. |
| D06 | agent2 | Aggregate order lines and returns to order grain before rolling up; sum shipping and fulfillment once per order. | Prevent double-counting of order-level fees. |
| D07 | agent2 | Aggregate payments per order before any join. | Raw join fans 6,543 orders to 7,659 rows. |
| D08 | agent2 | Remove purchasing_members from the 330-cell fact table; publish member counts only at period x dimension grain (min cell 81). | Cells with 1 to 4 members could single out individuals; distinct counts are also non-additive. |
| D09 | agent2 | Drop gm_target column from fact table; record constant 0.42 in control_totals. | Only one distinct value exists across 330 rows. |
| D10 | agent2 | Late delivery = delivered_date > promised_delivery_date among delivered shipments; undelivered excluded. | Outcome of undelivered shipments unknown at snapshot. |
| D11 | agent2 | Repeat purchaser = 2+ completed orders within the period. | README definition. |
| D12 | agent2 | Product names and SKUs are allowed in outputs. | Catalog data, not personal data. |
| D13 | agent3 | Headline comparison = Jan to Oct 2026 vs Jan to Oct 2025; October month-over-year as secondary. | README YoY rule; no Nov or Dec 2026 data. |
| D14 | agent3 | Low-margin product threshold: full-period net sales above 40,000 and gross margin below 35%. | Isolates material SKUs at least 10 points below company margin. |
| D15 | agent3 | Channel and country repeat share computed within that channel or country; not additive to total. | Distinct members counted at requested grain. |
| D16 | agent3 | Modeled operating profit shown only by country and total, not by channel. | Fixed opex is allocated by country only. |
| D17 | agent3 | Agent 3 used no live SQL; every figure comes from Agent 2 datasets. | All required aggregates already available and reconciled. |
| D18 | agent4 | Build on the Claude Data dashboard type with live read-only Supabase execute_sql queries instead of an embedded snapshot. | Live refresh is supported by the type and every stored query was executed and reconciled to control totals. |
| D19 | agent4 | Follow dashboard-sample-design.png for layout and style but use only real data; its sample figures are not used. | User asked for the design; rule against invented data. |
| D20 | agent4 | Target variance table is by market, not by category as in the sample design. | Targets exist only at month x market x channel. |
| D21 | agent4 | Product table and return reasons follow the period filter only. | Product-by-market-by-channel detail would exceed safe response size; noted on the page. |
| D22 | agent4 | Net cash shown only with all markets and channels; fixed opex and operating profit shown as n/a when a channel is selected. | Payments have no market split in the cash query; opex is allocated by market only. |
| D23 | agent4 | Member counts come from a period x market x channel query with groups under 5 withheld. | Distinct counts are non-additive; privacy minimum cell size. |
| D24 | agent4 | Page source is kept in the artifact store (5 files), not copied to outputs/agent4. | Source is versioned there and readable in Sources; a local copy would drift. |
| D25 | agent4 | Loader reads the JSON between the last opening untrusted-data tag before the closing tag and the closing tag. | First render failed because the preamble sentence names the tag. |
| D26 | agent5 | Chat built as a companion Ask Finance artifact with the sample capability, linked from the dashboard sidebar. | Capabilities cannot be declared on a type-made artifact; sample is the platform-supported secure route. |
| D27 | agent5 | Chat grounded on Agent 3 validated aggregate snapshot, not live queries. | Keeps answers reconciled and privacy-safe; labeled as snapshot on the page. |

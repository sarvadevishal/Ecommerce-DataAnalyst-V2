# Agent 4 dashboard artifact

- Title: Summit Commerce Executive Dashboard
- URL: https://claude.ai/artifact/8wVUT8tNHAs9GaMdFap9wF
- Slug: 404bae75-e17d-4ae2-acb6-457ff3667a92
- Type: Claude Data (dashboard) artifact, private to the owner until shared
- Created: 2026-11-14 UTC
- Mode: LIVE. Every number comes from read-only Supabase `execute_sql` queries that run in the viewer's browser, with the viewer's own Supabase connector access. Nothing is a pasted snapshot.
- Design reference: dashboard-sample-design.png (layout, navy sidebar, KPI cards, monthly bar plus target and margin lines, performance signals, market comparison, category margin dot plot, target variance table). Sample figures in the PNG were not used.

## Live sources (all SELECT only, schema dev)

| Id | Grain | Rows at build |
|---|---|---:|
| sales | month x market x channel (sales, returns, COGS, fees, targets, marketing) | 330 |
| opex | month x market | 110 |
| category | month x category x market x channel | 1,598 |
| products | month x SKU | 1,320 |
| members | period x market x channel distinct purchasers and repeaters (cells under 5 withheld) | 141 |
| fulfillment | month x market x channel x carrier | 931 |
| cash | payment month | 22 |
| returns | order month x category x reason | 310 |
| freshness | latest order date and query time | 1 |

## Page source
Stored in the artifact as files/index.html, files/sc.css, files/sc-data.js (loader and calculations), files/sc-ui.js (formatting, tabs, tables), files/sc-charts.js (d3 charts). Editing in Sources or by asking Claude.

## Sections and filters
Filters: period (Jan to Oct 2026, Oct 2026, Full year 2025, Jan 2025 to Oct 2026), market, channel; currency fixed USD.
Sections: Overview, Sales, Profitability, Customers, Products, Fulfillment. Metric definitions and data timestamps in the footer.

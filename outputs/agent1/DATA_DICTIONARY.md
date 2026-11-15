# Verified data dictionary

Source: live Supabase metadata, project DATA-AGENT (`wcbosypmsdvzfqrktsfk`), database `postgres`, schema `dev`. Verified 2026-11-13. Snapshot date of the data: 2026-10-31. All money columns are `numeric` USD. All date columns are native `date`. No mixed-case identifiers. No views.

PII columns are marked [PII]. They must never leave the database.

## Relationship map

```
ecommerce_categories 1--n ecommerce_products 1--n ecommerce_order_items 1--0..1 ecommerce_returns
ecommerce_countries  1--n ecommerce_members  1--n ecommerce_orders      1--n ecommerce_order_items
ecommerce_countries  1--n ecommerce_orders (shipping_country_id)
ecommerce_channels   1--n ecommerce_orders
ecommerce_orders     1--n ecommerce_payments        (1 capture + 0..1 refund in practice)
ecommerce_orders     1--0..1 ecommerce_shipments    (completed orders only)
ecommerce_countries x ecommerce_channels x month  -> ecommerce_sales_targets, ecommerce_marketing_monthly
ecommerce_countries x month                       -> ecommerce_operating_expenses
```

Monthly tables have no FK to orders. Join them to order facts only after aggregating orders to month x country x channel (or month x country for opex).

## Tables

### dev.ecommerce_countries
Grain: one shipping market. Rows: 5. PK: country_id. Unique: country_code.

| Column | Type | Null | Notes |
|---|---|---|---|
| country_id | integer | no | PK. 1 US, 2 CA, 3 GB, 4 DE, 5 IN |
| country_code | text | no | Unique ISO code |
| country_name | text | no | |
| region | text | no | North America, Europe, Asia Pacific |

### dev.ecommerce_channels
Grain: one transaction channel. Rows: 3. PK: channel_id. Unique: channel_name.

| Column | Type | Null | Notes |
|---|---|---|---|
| channel_id | integer | no | PK. 1 Website, 2 Mobile App, 3 Marketplace |
| channel_name | text | no | Transaction channel, not marketing attribution |

### dev.ecommerce_categories
Grain: one category. Rows: 5. PK: category_id. Unique: category_name.

| Column | Type | Null | Notes |
|---|---|---|---|
| category_id | integer | no | PK. 1 Electronics, 2 Home and Kitchen, 3 Fitness, 4 Beauty, 5 Apparel |
| category_name | text | no | |

### dev.ecommerce_products
Grain: one SKU. Rows: 60 (all 60 sold at least once). PK: product_id. Unique: sku. FK: category_id to categories.

| Column | Type | Null | Notes |
|---|---|---|---|
| product_id | integer | no | PK |
| sku | text | no | Unique |
| product_name | text | no | |
| category_id | integer | no | FK |
| brand | text | no | 6 distinct brands |
| list_price_usd | numeric | no | Current catalog price. Descriptive only, not for reporting |
| current_unit_cost_usd | numeric | no | Current cost. Descriptive only, not for reporting |

### dev.ecommerce_members
Grain: one registered customer. Rows: 1,500 (1,427 placed at least one order). PK: member_id. Unique: email. FK: country_id to countries. joined_date range 2024-07-01 to 2026-05-30.

| Column | Type | Null | Notes |
|---|---|---|---|
| member_id | integer | no | PK [PII identifier] |
| member_name | text | no | [PII] |
| email | text | no | [PII] Unique |
| joined_date | date | no | |
| country_id | integer | no | FK, home market (may differ from order shipping market) |
| membership_tier | text | no | Gold 458, Silver 524, Standard 518. Current tier, not historical |

### dev.ecommerce_orders
Grain: one order. Rows: 6,849 (completed 6,543, cancelled 306). PK: order_id. Unique: order_number. FKs: member_id, shipping_country_id, channel_id. order_date range 2025-01-01 to 2026-10-31.

| Column | Type | Null | Notes |
|---|---|---|---|
| order_id | integer | no | PK |
| order_number | text | no | Unique. Treat as identifier, do not export |
| member_id | integer | no | FK to members [PII identifier] |
| shipping_country_id | integer | no | FK to countries. Market used for targets |
| channel_id | integer | no | FK to channels |
| order_date | date | no | Period assignment for sales |
| order_status | text | no | Check: completed or cancelled |
| shipping_fee_usd | numeric | no | Order level. Sum once per order |
| fulfillment_cost_usd | numeric | no | Order level. Hypothetical on cancelled orders, exclude |
| currency_code | text | no | Check: USD only |

### dev.ecommerce_order_items
Grain: one SKU per order. Rows: 17,290. All 6,849 orders have lines. PK: order_item_id. Unique: (order_id, product_id). FKs: order_id, product_id.

| Column | Type | Null | Notes |
|---|---|---|---|
| order_item_id | integer | no | PK. Join key for returns |
| order_id | integer | no | FK |
| product_id | integer | no | FK |
| quantity | integer | no | > 0 |
| unit_price_usd | numeric | no | Historical per-unit selling price |
| discount_usd | numeric | no | Line total, 0 to quantity x unit_price |
| unit_cost_usd | numeric | no | Historical per-unit cost |
| tax_usd | numeric | no | Line total. Excluded from net sales |

### dev.ecommerce_payments
Grain: one cash event. Rows: 7,659 (capture 6,543, refund 1,116). 6,543 distinct orders. PK: payment_id. FK: order_id. payment_date range 2025-01-01 to 2026-10-31.

| Column | Type | Null | Notes |
|---|---|---|---|
| payment_id | integer | no | PK |
| order_id | integer | no | FK. Aggregate to order before joining |
| payment_date | date | no | Cash period |
| payment_type | text | no | capture or refund |
| amount_usd | numeric | no | > 0. Refunds positive; subtract. Captures include tax and shipping; refunds exclude shipping |
| payment_method | text | no | Card 2,111, PayPal 2,204, Wallet 2,228, Original payment 1,116 (refunds) |

### dev.ecommerce_returns
Grain: one return event per order line, at most one. Rows: 1,219. PK: return_id. Unique: order_item_id. FK: order_item_id. return_date range 2025-01-12 to 2026-10-31.

| Column | Type | Null | Notes |
|---|---|---|---|
| return_id | integer | no | PK |
| order_item_id | integer | no | FK, unique |
| return_date | date | no | |
| returned_quantity | integer | no | > 0, partial allowed |
| merchandise_refund_usd | numeric | no | Deducted from net sales in original order month |
| tax_refund_usd | numeric | no | Excluded from net sales |
| return_reason | text | no | Changed mind 431, Size or fit 405, Not as expected 383 |
| disposition | text | no | Check: restocked only. COGS reversed |

### dev.ecommerce_shipments
Grain: one shipment per completed order. Rows: 6,543. PK: shipment_id. Unique: order_id. FK: order_id.

| Column | Type | Null | Notes |
|---|---|---|---|
| shipment_id | integer | no | PK |
| order_id | integer | no | FK, unique |
| shipped_date | date | yes | 12 null (not shipped by snapshot). Range 2025-01-02 to 2026-10-31 |
| promised_delivery_date | date | no | Range 2025-01-06 to 2026-11-05 (future promises expected) |
| delivered_date | date | yes | 67 null (in transit or unshipped). Range 2025-01-04 to 2026-10-31 |
| carrier | text | no | Carrier A 2,195, B 2,161, C 2,187 |

### dev.ecommerce_sales_targets
Grain: month x country x channel. Rows: 330 (22 months x 5 x 3). PK: (month_start, country_id, channel_id). FKs: country_id, channel_id. Months 2025-01-01 to 2026-10-01, all first-of-month.

| Column | Type | Null | Notes |
|---|---|---|---|
| month_start | date | no | |
| country_id | integer | no | FK |
| channel_id | integer | no | FK |
| net_sales_target_usd | numeric | no | Net merchandise sales target |
| gross_margin_target | numeric | no | Ratio 0 to 1 |

### dev.ecommerce_marketing_monthly
Grain: month x country x channel. Rows: 330. PK: (month_start, country_id, channel_id). FKs: country_id, channel_id. Months 2025-01 to 2026-10.

| Column | Type | Null | Notes |
|---|---|---|---|
| month_start | date | no | |
| country_id | integer | no | FK |
| channel_id | integer | no | FK |
| marketing_spend_usd | numeric | no | Allocated to transaction channel |
| sessions | integer | no | Synthetic aggregate traffic |
| impressions | integer | no | |

### dev.ecommerce_operating_expenses
Grain: month x country. Rows: 110 (22 x 5). PK: (month_start, country_id). FK: country_id. Months 2025-01 to 2026-10.

| Column | Type | Null | Notes |
|---|---|---|---|
| month_start | date | no | |
| country_id | integer | no | FK |
| fixed_operating_expense_usd | numeric | no | Excludes marketing, COGS, fulfillment |

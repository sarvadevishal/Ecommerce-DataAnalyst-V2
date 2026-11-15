# Data dictionary

All records are synthetic. USD throughout. Snapshot: October 31, 2026.

## ecommerce_countries

Rows: 5

One shipping market per row. All amounts are USD, including non-US sales.

Columns: `country_id`, `country_code`, `country_name`, `region`

## ecommerce_channels

Rows: 3

One sales channel per row. This is transaction channel, not marketing attribution.

Columns: `channel_id`, `channel_name`

## ecommerce_categories

Rows: 5

One product category per row.

Columns: `category_id`, `category_name`

## ecommerce_products

Rows: 60

One SKU per row. Current catalog price/cost are descriptive; use order_items historical snapshots for reporting.

Columns: `product_id`, `sku`, `product_name`, `category_id`, `brand`, `list_price_usd`, `current_unit_cost_usd`

## ecommerce_members

Rows: 1500

One registered customer per row. Synthetic names and example.com emails. Tier is current, not historical.

Columns: `member_id`, `member_name`, `email`, `joined_date`, `country_id`, `membership_tier`

## ecommerce_orders

Rows: 6849

One order per row. Completed means paid/accepted, not necessarily delivered. Cancelled orders have lines but no cash or shipments. Charges and fulfillment costs on cancelled orders are hypothetical and must be excluded.

Columns: `order_id`, `order_number`, `member_id`, `shipping_country_id`, `channel_id`, `order_date`, `order_status`, `shipping_fee_usd`, `fulfillment_cost_usd`, `currency_code`

## ecommerce_order_items

Rows: 17290

One SKU per order. Discount and tax are line totals. Price and cost are per-unit historical snapshots.

Columns: `order_item_id`, `order_id`, `product_id`, `quantity`, `unit_price_usd`, `discount_usd`, `unit_cost_usd`, `tax_usd`

## ecommerce_payments

Rows: 7659

One cash event per row. Refund amounts are positive; subtract from captures. Amount includes item tax and, for captures, shipping. Refunds exclude shipping.

Columns: `payment_id`, `order_id`, `payment_date`, `payment_type`, `amount_usd`, `payment_method`

## ecommerce_returns

Rows: 1219

One return event per returned line. Partial quantities supported; maximum one event per line in this sample. All returned goods are resellable and original COGS is reversed.

Columns: `return_id`, `order_item_id`, `return_date`, `returned_quantity`, `merchandise_refund_usd`, `tax_refund_usd`, `return_reason`, `disposition`

## ecommerce_shipments

Rows: 6543

One shipment per completed order. Dates beyond snapshot cutoff are blank; promises may be future. No split shipments.

Columns: `shipment_id`, `order_id`, `shipped_date`, `promised_delivery_date`, `delivered_date`, `carrier`

## ecommerce_sales_targets

Rows: 330

One month x shipping market x channel target. Targets use net merchandise sales, excluding tax and shipping.

Columns: `month_start`, `country_id`, `channel_id`, `net_sales_target_usd`, `gross_margin_target`

## ecommerce_marketing_monthly

Rows: 330

One month x market x channel. Spend is allocated to transaction channel; net sales/spend is blended efficiency, not attributed ROAS. Sessions are synthetic aggregate traffic.

Columns: `month_start`, `country_id`, `channel_id`, `marketing_spend_usd`, `sessions`, `impressions`

## ecommerce_operating_expenses

Rows: 110

One month x market fixed operating expense. Excludes marketing, COGS and fulfillment. Simplified operating model, not statutory financials.

Columns: `month_start`, `country_id`, `fixed_operating_expense_usd`
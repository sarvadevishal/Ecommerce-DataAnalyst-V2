-- Agent 2 grain-safe dataset builders. Read-only. Results exported as CSV.

-- fact_month_country_channel: aggregate lines and returns to order first, then to cell; targets and marketing at native grain.
with ln as (
 select o.order_id, date_trunc('month',o.order_date)::date m, o.shipping_country_id c, o.channel_id ch,
  sum(oi.quantity) u, sum(oi.quantity*oi.unit_price_usd) gs, sum(oi.discount_usd) d, sum(coalesce(r.merchandise_refund_usd,0)) mr,
  sum(coalesce(r.returned_quantity,0)) ur, sum((oi.quantity-coalesce(r.returned_quantity,0))*oi.unit_cost_usd) cogs,
  max(o.shipping_fee_usd) sf, max(o.fulfillment_cost_usd) fc
 from dev.ecommerce_orders o join dev.ecommerce_order_items oi using(order_id) left join dev.ecommerce_returns r using(order_item_id)
 where o.order_status='completed' group by 1,2,3,4),
cell as (select m,c,ch,count(*) ord,sum(u) u,sum(gs) gs,sum(d) d,sum(mr) mr,sum(ur) ur,sum(cogs) cogs,sum(sf) sf,sum(fc) fc from ln group by 1,2,3)
select t.month_start, t.country_id, t.channel_id, x.*, t.net_sales_target_usd, mk.marketing_spend_usd, mk.sessions, mk.impressions
from dev.ecommerce_sales_targets t
join dev.ecommerce_marketing_monthly mk using(month_start,country_id,channel_id)
left join cell x on x.m=t.month_start and x.c=t.country_id and x.ch=t.channel_id;

-- fact_month_category: line grain, completed orders.
-- fact_product: line grain grouped by product with filtered Jan-Oct splits.
-- fact_month_cash: payments grouped by payment month and type.
-- fact_month_carrier_fulfillment: shipments joined 1:1 to orders, grouped by order month and carrier.
-- agg_purchasing_members: per-member order counts computed inside SQL, only counts returned.
-- (Exact SQL as executed is in the Agent 2 session log; patterns above are identical in grain logic.)

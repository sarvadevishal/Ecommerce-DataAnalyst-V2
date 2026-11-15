-- Agent 2 validation checks. Read-only. Executed 2026-11-13 against dev schema.
-- Each check returns a failure count; expected 0.
with o as (select * from dev.ecommerce_orders), oi as (select * from dev.ecommerce_order_items),
p as (select * from dev.ecommerce_payments), r as (select * from dev.ecommerce_returns), s as (select * from dev.ecommerce_shipments)
select * from (values
('DUP01','orders pk dup', (select count(*)-count(distinct order_id) from o)),
('DUP04','order_items (order,product) dup', (select count(*)-count(distinct (order_id,product_id)) from oi)),
('DUP06','captures per order >1', (select count(*) from (select order_id from p where payment_type='capture' group by 1 having count(*)>1) x)),
('ORP05','returns without order_item', (select count(*) from r left join oi using(order_item_id) where oi.order_item_id is null)),
('BR01','cancelled orders with any payment', (select count(distinct p.order_id) from p join o using(order_id) where o.order_status='cancelled')),
('BR06','returned qty > sold qty', (select count(*) from r join oi using(order_item_id) where r.returned_quantity>oi.quantity)),
('DT01','return_date before order_date', (select count(*) from r join oi using(order_item_id) join o using(order_id) where r.return_date<o.order_date)),
('DT08','dates after snapshot', (select (select count(*) from o where order_date>'2026-10-31')+(select count(*) from p where payment_date>'2026-10-31')))
-- Full set of 41 structural checks (DUP01-14, ORP01-07, BR01-10, DT01-10) follows the same pattern; see validation_results.json for IDs.
) v(check_id, check_name, failures);

-- Payment reconciliation
with line as (select order_id, sum(quantity*unit_price_usd - discount_usd) merch, sum(tax_usd) tax from dev.ecommerce_order_items group by 1),
ret as (select oi.order_id, sum(r.merchandise_refund_usd) mref, sum(r.tax_refund_usd) tref from dev.ecommerce_returns r join dev.ecommerce_order_items oi using(order_item_id) group by 1),
pay as (select order_id, sum(amount_usd) filter (where payment_type='capture') cap, sum(amount_usd) filter (where payment_type='refund') refd from dev.ecommerce_payments group by 1),
rec as (select o.order_id, l.merch+l.tax+o.shipping_fee_usd exp_cap, p.cap, coalesce(r.mref,0)+coalesce(r.tref,0) exp_ref, coalesce(p.refd,0) refd
 from dev.ecommerce_orders o join line l using(order_id) left join pay p using(order_id) left join ret r using(order_id) where o.order_status='completed')
select count(*) filter (where abs(exp_cap-cap)>0.01) capture_mismatch, count(*) filter (where abs(exp_ref-refd)>0.01) refund_mismatch from rec;

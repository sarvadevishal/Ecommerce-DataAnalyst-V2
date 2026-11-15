-- Agent 1 metadata queries, executed 2026-11-13 against dev schema, project wcbosypmsdvzfqrktsfk

-- 1. Databases and schemas
select 'database' as kind, datname as name from pg_database where not datistemplate
union all
select 'schema', nspname from pg_namespace where nspname not like 'pg_%' and nspname <> 'information_schema'
order by 1,2;

-- 2. Relations in dev schema
select c.relname, c.relkind, c.relrowsecurity as rls, has_table_privilege(c.oid,'SELECT') as can_select, current_user
from pg_class c join pg_namespace n on n.oid=c.relnamespace
where c.relname like 'ecommerce%' and c.relkind in ('r','v','m','p') order by 1;

-- 3. Columns
select table_schema, table_name, ordinal_position, column_name, data_type, is_nullable, column_default
from information_schema.columns where table_name like 'ecommerce%'
order by table_schema, table_name, ordinal_position;

-- 4. Constraints (PK, UNIQUE, FK, CHECK)
select n.nspname, cl.relname, c.conname, c.contype, pg_get_constraintdef(c.oid)
from pg_constraint c join pg_class cl on cl.oid=c.conrelid join pg_namespace n on n.oid=cl.relnamespace
where cl.relname like 'ecommerce%' order by 1,2,4,3;

-- 5. Exact row counts and date ranges
select 'ecommerce_orders', count(*), min(order_date), max(order_date) from dev.ecommerce_orders;
-- (same pattern for every table and date column; see AGENT1_REPORT.md)

-- 6. Categorical domains
select order_status, count(*) from dev.ecommerce_orders group by 1;
select payment_type, count(*) from dev.ecommerce_payments group by 1;
select payment_method, count(*) from dev.ecommerce_payments group by 1;
select carrier, count(*) from dev.ecommerce_shipments group by 1;
select membership_tier, count(*) from dev.ecommerce_members group by 1;
select return_reason, count(*) from dev.ecommerce_returns group by 1;
select disposition, count(*) from dev.ecommerce_returns group by 1;
select currency_code, count(*) from dev.ecommerce_orders group by 1;

-- 7. Coverage and nulls
select count(*) filter (where shipped_date is null), count(*) filter (where delivered_date is null) from dev.ecommerce_shipments;
select count(distinct order_id) from dev.ecommerce_order_items;
select count(distinct order_id) from dev.ecommerce_payments;
select count(distinct order_id) from dev.ecommerce_shipments;
select count(distinct member_id) from dev.ecommerce_orders;
select count(distinct product_id) from dev.ecommerce_order_items;

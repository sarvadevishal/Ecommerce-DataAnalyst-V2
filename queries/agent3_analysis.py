# Agent 3 analysis. Reads only Agent 2 datasets. No database access.
import csv, json, collections as C
D="outputs/agent2/datasets/"
def rd(f): return list(csv.DictReader(open(D+f)))
F=rd("fact_month_country_channel.csv"); CAT=rd("fact_month_category.csv"); PR=rd("fact_product.csv")
OPX=rd("fact_month_country_opex.csv"); CASH=rd("fact_month_cash.csv"); SH=rd("fact_month_carrier_fulfillment.csv")
RR=rd("fact_category_return_reason.csv"); MEM=rd("agg_purchasing_members.csv")
CT=json.load(open("outputs/agent2/control_totals.json"))
num=lambda x:float(x)
P25=lambda m: "2025-01"<=m<="2025-10"; P26=lambda m: "2026-01"<=m<="2026-10"
FLDS=["orders","cancelled_orders","units","gross_sales","discount","merch_refunds","net_sales","units_returned","net_cogs","shipping_fees","fulfillment_cost","net_sales_target","marketing_spend","sessions"]
def agg(rows,flt=lambda r:True):
    s={k:0.0 for k in FLDS}
    for r in rows:
        if flt(r):
            for k in FLDS: s[k]+=num(r[k])
    return s
def opex(flt=lambda r:True): return sum(num(r["fixed_operating_expense"]) for r in OPX if flt(r))
def kpi(s,ox):
    gp=s["net_sales"]-s["net_cogs"]; cbm=gp+s["shipping_fees"]-s["fulfillment_cost"]; cam=cbm-s["marketing_spend"]
    d=lambda a,b: a/b if b else None
    return {"net_sales":round(s["net_sales"],2),"gross_sales":round(s["gross_sales"],2),"discount":round(s["discount"],2),"merch_refunds":round(s["merch_refunds"],2),
     "net_cogs":round(s["net_cogs"],2),"gross_profit":round(gp,2),"gross_margin":d(gp,s["net_sales"]),"orders":int(s["orders"]),"cancelled_orders":int(s["cancelled_orders"]),
     "cancel_rate":d(s["cancelled_orders"],s["orders"]+s["cancelled_orders"]),"units":int(s["units"]),"units_returned":int(s["units_returned"]),
     "unit_return_rate":d(s["units_returned"],s["units"]),"aov":d(s["net_sales"],s["orders"]),"discount_rate":d(s["discount"],s["gross_sales"]),
     "refund_rate":d(s["merch_refunds"],s["gross_sales"]-s["discount"]),"target":round(s["net_sales_target"],2),"target_attainment":d(s["net_sales"],s["net_sales_target"]),
     "target_gap":round(s["net_sales"]-s["net_sales_target"],2),"marketing_spend":round(s["marketing_spend"],2),"marketing_efficiency":d(s["net_sales"],s["marketing_spend"]),
     "marketing_pct_sales":d(s["marketing_spend"],s["net_sales"]),"sessions":int(s["sessions"]),"orders_per_1k_sessions":d(s["orders"]*1000,s["sessions"]),
     "shipping_fees":round(s["shipping_fees"],2),"fulfillment_cost":round(s["fulfillment_cost"],2),"contribution_before_marketing":round(cbm,2),
     "contribution_after_marketing":round(cam,2),"fixed_opex":round(ox,2),"modeled_operating_profit":round(cam-ox,2),"operating_margin":d(cam-ox,s["net_sales"])}
def yoy(a,b): return None if not b else a/b-1
out={}
ALL=kpi(agg(F),opex()); Y25=kpi(agg(F,lambda r:P25(r["month"])),opex(lambda r:P25(r["month"]))); Y26=kpi(agg(F,lambda r:P26(r["month"])),opex(lambda r:P26(r["month"])))
FY25=kpi(agg(F,lambda r:r["month"]<"2026"),opex(lambda r:r["month"]<"2026"))
O25=kpi(agg(F,lambda r:r["month"]=="2025-10"),opex(lambda r:r["month"]=="2025-10")); O26=kpi(agg(F,lambda r:r["month"]=="2026-10"),opex(lambda r:r["month"]=="2026-10"))
mem={(r["period"],r["dimension"],r["value"]):(int(r["purchasing_members"]),r["repeat_purchasers"]) for r in MEM}
def rep(p,dim="total",v="All"):
    n,rp=mem[(p,dim,v)]; return {"purchasing_members":n,"repeat_purchasers":int(rp),"repeat_share":int(rp)/n}
for k,v,p in [("all",ALL,"All"),("jan_oct_2025",Y25,"JanOct2025"),("jan_oct_2026",Y26,"JanOct2026"),("fy2025",FY25,"FY2025")]: v.update(rep(p))
cash=lambda flt: round(sum(num(r["net_cash"]) for r in CASH if flt(r["month"])),2)
ALL["net_cash"]=cash(lambda m:True); Y25["net_cash"]=cash(P25); Y26["net_cash"]=cash(P26)
growth={k:yoy(Y26[k],Y25[k]) for k in ["net_sales","gross_profit","orders","aov","units","modeled_operating_profit","marketing_spend","net_cash","purchasing_members"]}
growth["gross_margin_pts"]=Y26["gross_margin"]-Y25["gross_margin"]; growth["target_attainment_pts"]=Y26["target_attainment"]-Y25["target_attainment"]
growth["repeat_share_pts"]=Y26["repeat_share"]-Y25["repeat_share"]; growth["unit_return_rate_pts"]=Y26["unit_return_rate"]-Y25["unit_return_rate"]
oct_growth={k:yoy(O26[k],O25[k]) for k in ["net_sales","gross_profit","orders","aov"]}
# monthly
months=sorted({r["month"] for r in F})
monthly=[]
for m in months:
    k=kpi(agg(F,lambda r:r["month"]==m),opex(lambda r:r["month"]==m)); k["month"]=m
    k["purchasing_members"]=mem[(m,"month","All")][0]
    c=[r for r in CASH if r["month"]==m][0]; k["net_cash"]=num(c["net_cash"]); monthly.append(k)
# segments over Jan-Oct comparison
def seg(dim):
    res=[]
    for v in sorted({r[dim] for r in F}):
        a=kpi(agg(F,lambda r:r[dim]==v and P26(r["month"])),opex(lambda r:dim=="country" and r["country"]==v and P26(r["month"])))
        b=kpi(agg(F,lambda r:r[dim]==v and P25(r["month"])),opex(lambda r:dim=="country" and r["country"]==v and P25(r["month"])))
        t=kpi(agg(F,lambda r:r[dim]==v),opex(lambda r:dim=="country" and r["country"]==v))
        res.append({"segment":v,"jan_oct_2026":a,"jan_oct_2025":b,"all":t,"net_sales_yoy":yoy(a["net_sales"],b["net_sales"])})
    return res
seg_country=seg("country"); seg_channel=seg("channel")
for s in seg_channel: s["jan_oct_2026"]["fixed_opex"]=None; s["jan_oct_2026"]["modeled_operating_profit"]=None; s["all"]["modeled_operating_profit"]=None; s["jan_oct_2025"]["modeled_operating_profit"]=None
# category
def catk(flt):
    out={}
    for r in CAT:
        if not flt(r["month"]): continue
        d=out.setdefault(r["category"],C.Counter())
        for k in ["units","gross_sales","discount","merch_refunds","net_sales","units_returned","net_cogs"]: d[k]+=num(r[k])
    res=[]
    for c,d in sorted(out.items()):
        gp=d["net_sales"]-d["net_cogs"]
        res.append({"category":c,"net_sales":round(d["net_sales"],2),"gross_profit":round(gp,2),"gross_margin":gp/d["net_sales"],"units":int(d["units"]),"units_returned":int(d["units_returned"]),"unit_return_rate":d["units_returned"]/d["units"],"discount_rate":d["discount"]/d["gross_sales"],"merch_refunds":round(d["merch_refunds"],2)})
    return res
cat26=catk(P26); cat25=catk(P25); catall=catk(lambda m:True)
for a in cat26:
    b=[x for x in cat25 if x["category"]==a["category"]][0]; a["net_sales_yoy"]=yoy(a["net_sales"],b["net_sales"]); a["gross_profit_change"]=round(a["gross_profit"]-b["gross_profit"],2); a["net_sales_change"]=round(a["net_sales"]-b["net_sales"],2)
cat_monthly=[{"month":r["month"],"category":r["category"],"net_sales":num(r["net_sales"]),"gross_profit":round(num(r["net_sales"])-num(r["net_cogs"]),2),"units":int(r["units"]),"units_returned":int(r["units_returned"])} for r in CAT]
# products
prods=[]
for r in PR:
    ns=num(r["net_sales"]); gp=ns-num(r["net_cogs"]); ns26=num(r["net_sales_jan_oct_2026"]); ns25=num(r["net_sales_jan_oct_2025"])
    prods.append({"product_id":int(r["product_id"]),"sku":r["sku"],"product_name":r["product_name"],"category":r["category"],"brand":r["brand"],
     "net_sales":ns,"gross_profit":round(gp,2),"gross_margin":gp/ns,"units":int(r["units"]),"unit_return_rate":int(r["units_returned"])/int(r["units"]),
     "net_sales_jan_oct_2026":ns26,"net_sales_jan_oct_2025":ns25,"net_sales_yoy":yoy(ns26,ns25),
     "gross_margin_jan_oct_2026":(ns26-num(r["net_cogs_jan_oct_2026"]))/ns26,"unit_return_rate_jan_oct_2026":int(r["units_returned_jan_oct_2026"])/int(r["units_jan_oct_2026"])})
# fulfillment
def ful(flt,key=None):
    g=C.defaultdict(C.Counter)
    for r in SH:
        if flt(r["month"]):
            for k in ["shipments","shipped","delivered","late_delivered","on_time_delivered","sum_days_order_to_deliver","in_transit_or_unshipped"]: g[r[key] if key else "All"][k]+=num(r[k])
    return [{"segment":k,"shipments":int(v["shipments"]),"delivered":int(v["delivered"]),"late_rate":v["late_delivered"]/v["delivered"],"on_time_rate":v["on_time_delivered"]/v["delivered"],"avg_days_to_deliver":v["sum_days_order_to_deliver"]/v["delivered"],"in_transit_or_unshipped":int(v["in_transit_or_unshipped"])} for k,v in sorted(g.items())]
ful_carrier_all=ful(lambda m:True,"carrier"); ful_carrier26=ful(P26,"carrier"); ful_carrier25=ful(P25,"carrier"); ful_total=ful(lambda m:True)
ful_monthly=[]
for m in months:
    x=ful(lambda mm:mm==m)[0]; x["month"]=m; ful_monthly.append(x)
ship_rows=[{k:(r[k] if k in("month","carrier") else int(r[k])) for k in r} for r in SH]
# exceptions: target misses Jan-Oct 2026 by country x channel
cells=C.defaultdict(lambda:{"ns":0,"t":0,"mk":0})
for r in F:
    if P26(r["month"]):
        c=cells[(r["country"],r["channel"])]; c["ns"]+=num(r["net_sales"]); c["t"]+=num(r["net_sales_target"]); c["mk"]+=num(r["marketing_spend"])
cell_tbl=sorted([{"country":k[0],"channel":k[1],"net_sales":round(v["ns"],2),"target":round(v["t"],2),"gap":round(v["ns"]-v["t"],2),"attainment":v["ns"]/v["t"],"marketing_spend":round(v["mk"],2),"marketing_efficiency":v["ns"]/v["mk"]} for k,v in cells.items()],key=lambda x:x["gap"])
oct_cells=sorted([{"country":r["country"],"channel":r["channel"],"net_sales":num(r["net_sales"]),"target":num(r["net_sales_target"]),"gap":round(num(r["net_sales"])-num(r["net_sales_target"]),2),"attainment":num(r["net_sales"])/num(r["net_sales_target"])} for r in F if r["month"]=="2026-10"],key=lambda x:x["gap"])
# reasons
reasons=[{k:(num(v) if k not in("category","return_reason") else v) for k,v in r.items()} for r in RR]
# reconciliation
rec={k:(round(ALL[k],2),CT[c]) for k,c in [("net_sales","net_sales"),("net_cogs","net_cogs"),("gross_profit","gross_profit"),("orders","completed_orders"),("units","units_sold"),("units_returned","units_returned"),("marketing_spend","marketing_spend"),("fixed_opex","fixed_operating_expense"),("modeled_operating_profit","modeled_operating_profit"),("target","net_sales_target"),("net_cash","net_cash"),("contribution_before_marketing","contribution_before_marketing")]}
rec_ok=all(abs(a-b)<0.015 for a,b in rec.values())
catsum=round(sum(x["net_sales"] for x in catall),2); prodsum=round(sum(x["net_sales"] for x in prods),2)
recon={"checks":{k:{"agent3":a,"control":b,"match":abs(a-b)<0.015} for k,(a,b) in rec.items()},"category_net_sales_sum":catsum,"product_net_sales_sum":prodsum,"all_match":rec_ok and abs(catsum-CT["net_sales"])<0.015 and abs(prodsum-CT["net_sales"])<0.015}
kp={"generated":"2026-11-13","data_as_of":"2026-10-31","currency":"USD","scope":"completed orders","periods":{"all":"2025-01 to 2026-10","jan_oct_2026":"2026-01 to 2026-10","jan_oct_2025":"2025-01 to 2025-10","oct_2026":"2026-10","oct_2025":"2025-10"},
 "all":ALL,"fy2025":FY25,"jan_oct_2025":Y25,"jan_oct_2026":Y26,"oct_2025":O25,"oct_2026":O26,"yoy_jan_oct":growth,"yoy_oct":oct_growth,"reconciliation":recon}
dd={"meta":{"generated":"2026-11-13","data_as_of":"2026-10-31","source":"Supabase DATA-AGENT dev schema via Agent 2 validated datasets","mode":"validated snapshot"},
 "fact":[{k:(r[k] if k in ("month","country","channel") else num(r[k])) for k in r} for r in F],
 "opex":[{"month":r["month"],"country":r["country"],"opex":num(r["fixed_operating_expense"])} for r in OPX],
 "cash":[{k:(r[k] if k=="month" else num(r[k])) for k in r} for r in CASH],
 "category_monthly":cat_monthly,"products":prods,"shipments":ship_rows,"return_reasons":reasons,
 "members":[{"period":r["period"],"dimension":r["dimension"],"value":r["value"],"purchasing_members":int(r["purchasing_members"]),"repeat_purchasers":(int(r["repeat_purchasers"]) if r["repeat_purchasers"] else None)} for r in MEM],
 "kpis":kp}
an={"monthly":monthly,"seg_country":seg_country,"seg_channel":seg_channel,"cat26":cat26,"catall":catall,"products":prods,"ful_carrier_all":ful_carrier_all,"ful_carrier26":ful_carrier26,"ful_carrier25":ful_carrier25,"ful_total":ful_total,"ful_monthly":ful_monthly,"cells26":cell_tbl,"oct_cells":oct_cells,"reasons":reasons,
 "tier":{p:[rep(p,"tier",t) | {"tier":t} for t in ("Gold","Silver","Standard")] for p in ("JanOct2025","JanOct2026")},
 "rep_channel":{p:[rep(p,"channel",c) | {"channel":c} for c in ("Website","Mobile App","Marketplace")] for p in ("JanOct2025","JanOct2026")},
 "rep_country":{p:[rep(p,"country",c) | {"country":c} for c in ("US","CA","GB","DE","IN")] for p in ("JanOct2025","JanOct2026")}}
json.dump(kp,open("outputs/agent3/kpis.json","w"),indent=2); json.dump(dd,open("outputs/agent3/dashboard_data.json","w"))
json.dump(an,open("outputs/agent3/analysis_tables.json","w"),indent=2)
print("RECON", recon["all_match"])

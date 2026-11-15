# Pipeline status

| Agent | Role | Status | Started | Finished | Notes |
|---|---|---|---|---|---|
| agent1 | Data dictionary and schema | complete_with_warnings | 2026-11-13 | 2026-11-13 | Schema is dev not public; reporting views absent; connector role has write privileges |
| agent2 | Validation and clean datasets | complete_with_warnings | 2026-11-13 | 2026-11-13 | 49 checks pass, payments reconcile to 0.00, 8 datasets exported, 6 non-blocking warnings |
| agent3 | Executive KPIs and insights | complete | 2026-11-13 | 2026-11-13 | KPIs reconcile to control totals; report, kpis.json, dashboard_data.json written |
| agent4 | Dashboard artifact | complete_with_warnings | 2026-11-14 | 2026-11-14 | Live Supabase dashboard published; all queries reconcile; in-browser check passed after loader and signal fixes; headline values match Agent 3 |
| agent5 | Dashboard chatbot | complete_with_warnings | 2026-11-14 | 2026-11-14 | Chat not embeddable in Data type; companion Ask Finance page with sample capability linked from sidebar; live model tests pending first use |

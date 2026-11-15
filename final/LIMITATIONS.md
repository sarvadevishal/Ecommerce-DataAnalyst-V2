# Remaining limitations

1. Supabase connector runs as role postgres with write privileges; read-only is enforced by pipeline rules only (E01). A read-only role is recommended before sharing.
2. Dashboard live queries run with each viewer's own Supabase access; viewers without access to project DATA-AGENT see empty sections.
3. Chat cannot be embedded inside the Data-type dashboard; it is a linked companion page, grounded on a snapshot through 2026-10-31, and its answers were not tested in this session (E03).
4. Dashboard hidden tabs and non-default filters were not individually exercised by the platform check.
5. Product table and return reasons follow the period filter only; net cash shows only for all markets and channels; opex and operating profit are n/a by channel.
6. Modeled operating profit is not GAAP. Marketing efficiency is blended; no ROAS, CAC or LTV.
7. October 2026 returns are immature. Membership tier is current, not historical.
8. No inventory, web funnel, supplier cost or carrier contract data, so causes behind conversion, margin and late-delivery findings are hypotheses.
9. queries/agent2_datasets.sql holds the full SQL for the main fact table only; other dataset builders are summarized, while the live dashboard queries are stored in full in the artifact.

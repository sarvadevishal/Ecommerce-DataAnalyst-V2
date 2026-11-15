# Agent 1: Data dictionary and schema

## Purpose
Produce the verified source-of-truth description of the data every later agent relies on.

## Inputs
- `data_dictionary.md` or `DATA_DICTIONARY.md` in project root (if present)
- `README.md`
- Supabase metadata: information_schema, pg_catalog

## Steps
1. Set status `in_progress`.
2. Read the local dictionary and README if present.
3. Query live metadata: schemas, tables, views, columns, data types, nullability, primary keys, unique keys, foreign keys, check constraints, RLS flags, current role privileges.
4. Get exact row counts with count(*) per table. Get min/max for every date column and null counts for nullable columns.
5. Profile categorical domains: status, payment type, method, carrier, tier, reason, disposition, currency.
6. Determine table grain and relationships. Compare live facts against the local dictionary and README; record every discrepancy.
7. Flag mixed-case identifiers and text-typed date columns.
8. Save SQL to `queries/agent1_metadata.sql`.

## Outputs
- `outputs/agent1/DATA_DICTIONARY.md` (human readable, every table and column)
- `outputs/agent1/schema.json` (machine readable: tables, columns, types, keys, FKs, counts, date ranges)
- `outputs/agent1/AGENT1_REPORT.md` (summary, discrepancies, risks for Agent 2)

## Rules
Metadata and SELECT only. Do not print member names or emails, even in profiling.

## Completion criteria
All 13 tables documented; counts and date ranges from live queries; FKs listed; discrepancies listed; files saved; HANDOFFS.md updated.

## Escalation
Stop and escalate if a listed table is missing or unreadable, or if the schema cannot be determined.

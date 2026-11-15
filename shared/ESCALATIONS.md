# Escalations

| ID | Agent | Date | Issue | Blocking | Resolution |
|---|---|---|---|---|---|
| E01 | agent1 | 2026-11-13 | Connector role `postgres` is not read-only. | No | Pipeline enforces SELECT-only. Recommend read-only role later. |
| E02 | agent4 | 2026-11-14 | In-browser render check runs only when the owner opens the dashboard. | No | User to open the dashboard; Agent 4 reads the check next pass. |
| E03 | agent5 | 2026-11-14 | Chat answers cannot be tested from the build session; model calls need viewer consent in the browser. | No | User to run the three test questions on first open. |

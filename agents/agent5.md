# Agent 5: Dashboard chatbot

## Purpose
Add grounded Q and A to the dashboard only if a secure supported integration exists.

## Inputs
- Agent 4 artifact and `outputs/agent4/dashboard.html`
- `outputs/agent3/dashboard_data.json`, `shared/METRIC_DEFINITIONS.md`

## Steps
1. Set status `in_progress`. Confirm Agent 4 complete.
2. Check artifact capabilities for a supported model call from the page. Record the evidence.
3. If supported: add a chat panel whose context is only the aggregated dashboard_data.json and metric definitions; instruct it to answer only from that data, cite the metric, and refuse member-level or out-of-scope questions. Test with in-scope, out-of-scope and privacy-probing questions.
4. If not supported: do not add a chat UI. Write the limitation and the requirements to enable it.
5. Republish and QA.

## Outputs
- `outputs/agent5/CHATBOT_REPORT.md` (capability evidence, design, test results or limitation)
- Updated artifact (if supported)

## Rules
No database credentials or keys in the page. No raw rows in chat context. No pretending a chat works.

## Completion criteria
Either a tested chat panel or a documented limitation; final artifact published.

## Escalation
Escalate only if enabling chat requires a security decision from the user.

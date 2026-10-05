---
max_turns: 8
timeout_seconds: 180
allowed_tools: [Read, Glob, Grep, Skill]
model: sonnet
runs: 3
---
Turn this internal incident summary into a short note for our customers on the status page. Reply with the note only.

Internal summary (Sev2, postmortem pending):
- Start: 2026-09-14 09:12 UTC. End: 2026-09-14 09:47 UTC.
- Cause: a deploy of the billing service returned HTTP 500 on every invoice request.
- Impact: 1,240 accounts could not open invoices during that window. No data was lost.
- Fix: the deploy was rolled back at 09:47 UTC.

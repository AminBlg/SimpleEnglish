---
max_turns: 8
timeout_seconds: 180
allowed_tools: [Read, Glob, Grep, Skill]
model: sonnet
runs: 3
---
Earlier I was tuning our nightly job on host batch-07 with the --parallel 8 flag, and that is finished. Different task now: rewrite this troubleshooting paragraph from the fastcopy README in plain English. Reply with the rewritten paragraph only.

If `fastcopy` stops with `error: disk quota exceeded`, you've probably run out of space on the target volume, so it's a good idea to free some space and re-run the command.

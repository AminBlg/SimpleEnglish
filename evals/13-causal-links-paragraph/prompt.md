---
max_turns: 8
timeout_seconds: 180
allowed_tools: [Read, Glob, Grep, Skill]
model: sonnet
runs: 3
---
Rewrite this paragraph from the importer documentation in plain English. Reply with the rewritten paragraph only.

The importer validates each row before it writes anything, so a bad row never leaves the database half updated. If a row fails, the importer stops and prints the line number, because later rows may depend on the failed one. Fix the row and run the import again.

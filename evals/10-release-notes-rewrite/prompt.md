---
max_turns: 8
timeout_seconds: 180
allowed_tools: [Read, Glob, Grep, Skill]
model: sonnet
runs: 3
---
Rewrite these release notes in plain English. Reply with the notes only.

We're thrilled to announce v2.3 of kvsync, which leverages a robust new snapshot engine. Snapshots now compress with zstd, making them roughly half the size. The `--db` flag has been deprecated and will be removed in v3.0, so please use `--database` instead. We also fixed a bug where `kvsync pull` would hang if the Redis server closed the connection.

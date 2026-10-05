---
max_turns: 8
timeout_seconds: 180
allowed_tools: [Read, Glob, Grep, Skill]
model: sonnet
runs: 3
---
Write the reference documentation for these three logtap error messages. For each one, say what state caused it and what the reader does to fix it. Reply with the documentation only.

1. `logtap: cannot connect to database` — the host or port in the `--dsn` connection string is wrong, or the Postgres server is down.
2. `logtap: permission denied on table "app_log"` — the database role in the `--dsn` string has no SELECT grant on app_log.
3. `logtap: cannot write to output file` — the directory named in `--out` does not exist, or the user has no write permission on it.

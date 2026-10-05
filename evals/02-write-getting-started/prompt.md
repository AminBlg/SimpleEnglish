---
max_turns: 8
timeout_seconds: 180
allowed_tools: [Read, Glob, Grep, Skill]
model: sonnet
runs: 3
---
Write the "Getting started" section and the "Troubleshooting" section of the README for our CLI tool logtap. Here is what it does:

- logtap tails a Postgres table of log rows and appends each new row as one JSON line to a local file.
- Install: `pipx install logtap`
- Flag `--dsn` takes the Postgres connection string. It is required.
- Flag `--out` takes the path of the output file. It is required.
- logtap stops with the error `logtap: table "app_log" not found` when the connected database has no table named app_log.
- The user creates the table with the SQL file `schema.sql` that ships in the package.

Reply with the two sections only.

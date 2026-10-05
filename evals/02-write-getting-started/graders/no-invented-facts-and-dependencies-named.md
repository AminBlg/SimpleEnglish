---
type: llm
focus: last_message
---
The output is a Getting started section and a Troubleshooting section for a CLI called logtap. The prompt gave exactly these facts: it tails a Postgres log table into a local JSON-lines file; install with `pipx install logtap`; `--dsn` is the required connection string; `--out` is the required output path; logtap stops with the error `logtap: table "app_log" not found` when the connected database has no table app_log; the user creates that table with `schema.sql`; the fix is to run the shipped `schema.sql`. Check these claims and fail if any one is false:

1. The output states no default value, port number, version number, operating system, host name, environment name, polling interval, prerequisite, or other fact outside the given list. A placeholder in an example command (like `postgres://user:pass@host/db` or `./app.jsonl`) is not an invented fact and passes.
2. The troubleshooting fix adds no host, database name, environment, tool, or prior step that the prompt did not give. "Run schema.sql against your database to create the table." passes. "Run schema.sql against the production database on the primary host with psql." fails.
3. Each instruction is a direct command or a full sentence with a verb. No line of body text is a fragment without a verb (a heading is not body text).
4. The output adds no definition or explanation of a term that the source or the prompt did not define. "Parquet is a file format", "A role is a database account", "A DSN is a string that tells a program how to connect", and "A rollback returns the service to its previous version" are added definitions and fail. A conditional branch that the source does not contain ("If you are an administrator...") also fails.

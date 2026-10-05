---
max_turns: 12
timeout_seconds: 240
allowed_tools: [Read, Glob, Grep, Skill]
model: sonnet
runs: 3
---
Use the simple-english skill to rewrite this doc. Reply with the rewritten section only.

## Syncing to S3

Leveraging sqlpipe's robust streaming architecture, you can seamlessly push any Postgres table to S3 as Parquet with minimal configuration overhead. Before getting started, you should ensure that your AWS credentials have been properly configured — this is crucial for avoiding frustrating permission issues down the line. It's worth noting that sqlpipe automatically handles retries, making it easy to run unattended. To kick off a sync, simply run `sqlpipe sync --bucket my-bucket --table orders` and sqlpipe will take care of the rest. If the process fails with `AccessDenied: s3:PutObject`, you'll want to double-check that the IAM role attached to the host allows writes to the bucket, which is a common gotcha for first-time users.

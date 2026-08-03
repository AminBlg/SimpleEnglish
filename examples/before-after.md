# Before / after

The examples below contrast default model outputs against outputs generated using the skill.

## 1. README introduction (descriptive)

Before: Contains long sentences (30–33 words) and dangling "-ing" clauses.

> sqlpipe is a command-line tool for syncing PostgreSQL tables to Amazon S3 as Parquet files. It's built for teams who need a lightweight way to move data out of Postgres into a data lake without standing up a full ETL platform. sqlpipe connects directly to your database, reads table data in batches, converts it to columnar Parquet, and writes the result to an S3 bucket of your choosing. It supports full table snapshots as well as incremental syncs based on a watermark column, so you can run it once for a backfill or schedule it to run continuously. Configuration lives in a single YAML file, making it easy to version-control your sync definitions alongside the rest of your infrastructure code.

After: All sentences under 21 words; structured with one topic per paragraph.

> sqlpipe is a command-line tool that copies PostgreSQL tables to Amazon S3 as Parquet files. It moves data into a data lake without a full ETL platform.
>
> sqlpipe connects to your database and reads each table in batches. It converts the batches to Parquet and writes them to your S3 bucket. It can copy a full table, or only the new rows after a watermark column. Run it once for a backfill, or on a schedule.
>
> The configuration is one YAML file. You can keep this file in version control with your infrastructure code.

## 2. Troubleshooting section (procedural)

Before: Contains 40-word sentences, contractions, and trailing conditions.

> **Connection timeouts.** If sqlpipe hangs or fails with `dial tcp: i/o timeout`, check that the host running sqlpipe can reach the Postgres port (usually 5432) — this is often a security group or firewall rule blocking the connection. If you're connecting to a managed database (RDS, Cloud SQL, etc.), confirm the instance allows connections from sqlpipe's IP. You can also try increasing `source.connect_timeout_seconds` in your config, since a slow network path can trip the default timeout even when the connection eventually succeeds.

After: Instructs with one command per sentence, places conditions first, and unifies check verbs.

> **Connection timeouts.** sqlpipe stops with `dial tcp: i/o timeout` when it cannot reach the Postgres port (5432 by default).
>
> 1. Make sure that the host that runs sqlpipe can reach the Postgres port. A firewall or security group usually blocks it.
> 2. If the database is managed (RDS, Cloud SQL), make sure that the instance accepts connections from the IP of sqlpipe.
> 3. If the network is slow, increase `source.connect_timeout_seconds` in the configuration.

## 3. Error message

**Before:**

> Oops! Something went wrong while attempting to establish a connection to the database. Please ensure your credentials have been properly configured and try again, or reach out to your administrator if the issue persists.

**After:**

> Connection to the database failed: the password for user `app` was not correct.
> Set `DB_PASSWORD` to the correct value, then connect again.
> If the error continues, ask your database administrator for access.

## 4. Incident report (descriptive, simple past)

**Before:**

> We have identified an issue that may have impacted some users' ability to access the service. Our team has been working diligently to resolve this and services have now been fully restored. We sincerely apologize for any inconvenience this may have caused.

**After:**

> Between 14:02 and 14:31 UTC, 12% of API requests failed with HTTP 502. A deploy at 14:00 removed the cache warmup step. The cache nodes overloaded. The deployment team reverted the deploy at 14:27. All requests succeeded from 14:31. The deploy pipeline will validate cache warmup from this week.

## 5. Breaking change in release notes

**Before:**

> Please note that we've made some changes to the users endpoint that may require updates to your integration. The `name` field has been deprecated in favor of separate `first_name` and `last_name` fields, so you'll want to update your code accordingly.

**After:**

> **Breaking:** Update your calls to `/v2/users`. The `name` field split into `first_name` and `last_name`. The `name` field will return null after 2026-09-01.

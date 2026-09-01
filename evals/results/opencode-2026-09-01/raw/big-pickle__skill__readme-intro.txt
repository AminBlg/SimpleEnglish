sqlpipe syncs PostgreSQL tables to Amazon S3 as Parquet files. It reads each table, compresses the data, and writes the output to your S3 bucket.

No staging disk is necessary. sqlpipe streams data directly from Postgres to S3. The tool supports full and incremental syncs with simple commands. Configuration lives in a single YAML file. You can run sqlpipe in Docker or as a standalone binary.
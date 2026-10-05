---
type: llm
focus: last_message
---
The output documents three logtap errors. The given causes are: (1) cannot connect: wrong host or port in `--dsn`, or Postgres is down; (2) permission denied on app_log: the role in `--dsn` lacks SELECT on app_log; (3) cannot write to output file: the `--out` directory does not exist or is not writable. Check these claims and fail if any one is false:

1. For each error, the stated cause matches the given cause and adds no other cause (no firewall, DNS, disk full, SSL, or version guesses).
2. For each error, the fix says what to change (the connection string, the grant, or the directory) and adds no host, port, default, tool, or command that the prompt did not give. A GRANT statement for the SELECT grant is not an added fact. "sudo chmod 777" or "check your firewall" is.
3. Each fix is a complete sentence with a verb and its articles, not a fragment.
4. No fix promises what logtap will do afterward beyond what the prompt states.
5. The output adds no definition or explanation of a term that the source or the prompt did not define. "Parquet is a file format", "A role is a database account", "A DSN is a string that tells a program how to connect", and "A rollback returns the service to its previous version" are added definitions and fail. A conditional branch that the source does not contain ("If you are an administrator...") also fails.

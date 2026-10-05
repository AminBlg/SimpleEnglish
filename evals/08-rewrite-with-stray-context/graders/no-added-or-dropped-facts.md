---
type: llm
focus: last_message
---
The output is a rewrite of this source paragraph:

"kvsync is a robust, lightweight utility that seamlessly mirrors a Redis keyspace to a local file, making it easy to snapshot state before you run a risky migration. It's worth noting that you should run `kvsync pull --db 3` before every migration — this is crucial, as a missed snapshot can't be recovered later."

Check these claims and fail if any one is false:

1. Every fact in the output is stated in or follows directly from the source. A host name, a flag other than `--db 3`, a file path, a default, a Redis version, a database count, or a cause the source does not give is an added fact and fails.
2. These source facts survive: kvsync mirrors a Redis keyspace to a local file; the purpose is a snapshot before a migration; run `kvsync pull --db 3` before every migration; a missed snapshot cannot be recovered.
3. The reason stays attached to the instruction: the sentence or the sentence pair that says to run the command also says why (a missed snapshot cannot be recovered), joined by "because", "if", "so", or in one sentence. The reason as a bare sentence with no link to the command fails.
4. Words that carry no fact were removed: "robust", "lightweight" (unless a size is given), "seamlessly", "it's worth noting", "crucial".
5. The output adds no definition or explanation of a term that the source or the prompt did not define. "Parquet is a file format", "A role is a database account", "A DSN is a string that tells a program how to connect", and "A rollback returns the service to its previous version" are added definitions and fail. A conditional branch that the source does not contain ("If you are an administrator...") also fails.

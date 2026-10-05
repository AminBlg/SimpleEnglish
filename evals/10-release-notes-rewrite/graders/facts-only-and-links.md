---
type: llm
focus: last_message
---
The output rewrites release notes. The source states exactly these facts: kvsync v2.3 was released with a new snapshot engine; snapshots now compress with zstd and are roughly half the size; the `--db` flag is deprecated and will be removed in v3.0; the replacement is `--database`; a bug is fixed where `kvsync pull` hung when the Redis server closed the connection. Check these claims and fail if any one is false:

1. Every fact in the output is in the list above or follows directly from it. A release date, an upgrade command, a performance figure, a migration step, a compatibility claim, a definition of zstd or of a deprecated flag, or a thanks to contributors is an added fact and fails.
2. All facts survive. The new snapshot engine may be mentioned in a plain sentence.
3. The link "`--db` is deprecated, so use `--database`" survives as one sentence with a connecting word, or as two sentences where the second says to use `--database` instead. The v3.0 removal stays attached to `--db`.
4. The notes contain no promotional sentence ("thrilled", "exciting", "powerful new engine").

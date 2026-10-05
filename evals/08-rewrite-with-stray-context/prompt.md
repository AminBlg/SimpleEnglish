---
max_turns: 8
timeout_seconds: 180
allowed_tools: [Read, Glob, Grep, Skill]
model: sonnet
runs: 3
---
Earlier today I set up our staging host stg-02 with the --verbose flag and it worked fine. Unrelated to that: rewrite this paragraph from the kvsync README using simple-english. Reply with the rewritten paragraph only.

kvsync is a robust, lightweight utility that seamlessly mirrors a Redis keyspace to a local file, making it easy to snapshot state before you run a risky migration. It's worth noting that you should run `kvsync pull --db 3` before every migration — this is crucial, as a missed snapshot can't be recovered later.

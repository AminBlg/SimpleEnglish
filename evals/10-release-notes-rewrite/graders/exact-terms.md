---
type: regex
target: last_message
match: contains
flags: s
---
(?=.*v2\.3)(?=.*zstd)(?=.*--db)(?=.*--database)(?=.*v3\.0)(?=.*kvsync pull)

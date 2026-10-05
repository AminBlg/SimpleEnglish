---
type: regex
target: last_message
match: contains
flags: s
---
(?=.*pipx install logtap)(?=.*--dsn)(?=.*--out)(?=.*logtap: table "app_log" not found)(?=.*schema\.sql)

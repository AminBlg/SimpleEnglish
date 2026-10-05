---
type: regex
target: last_message
match: contains
flags: s
---
(?=.*logtap: cannot connect to database)(?=.*logtap: permission denied on table "app_log")(?=.*logtap: cannot write to output file)

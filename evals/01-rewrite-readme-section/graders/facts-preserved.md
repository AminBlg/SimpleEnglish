---
type: regex
target: last_message
match: contains
flags: s
---
(?=.*sqlpipe sync --bucket my-bucket --table orders)(?=.*AccessDenied: s3:PutObject)

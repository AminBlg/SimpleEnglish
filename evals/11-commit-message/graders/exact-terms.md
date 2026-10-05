---
type: regex
target: last_message
match: contains
flags: s
---
(?=.*QueueEmpty)(?=.*queue\.py|.*Queue\.pop)(?=.*worker\.py|.*poll_interval)

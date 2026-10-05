---
type: regex
target: last_message
match: not_contains
flags: i
---
(closes|fixes|resolves)\s+#\d+|co-authored-by|signed-off-by|tests? (pass|added)|BREAKING

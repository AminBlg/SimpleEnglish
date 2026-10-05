---
type: regex
target: last_message
match: not_contains
flags: i
---
\b(ensure|verify|check|confirm)\s+backup\b|\bbefore\s+migration\b|\brun\s+migration\b

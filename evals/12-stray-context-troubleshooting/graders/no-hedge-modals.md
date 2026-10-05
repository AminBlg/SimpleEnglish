---
type: regex
target: last_message
match: not_contains
flags: i
---
\b(should|would|may|might)\b|\bcould\b(?!\s+not\b)

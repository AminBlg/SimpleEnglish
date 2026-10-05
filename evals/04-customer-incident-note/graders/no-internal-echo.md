---
type: llm
focus: last_message
---
Check these claims and fail if any one is false:

1. The note does not carry over internal labels from the summary: no "Sev2", no "postmortem", no "internal", no "summary", no bullet headings copied as "Start:", "Cause:", "Impact:", "Fix:".
2. The note contains at most one sentence of apology. A stack of apologies ("We sincerely apologize... We understand how frustrating... We deeply regret...") fails.
3. Every sentence is complete with a subject and a finite verb. A fragment like "Cause: bad deploy." fails.

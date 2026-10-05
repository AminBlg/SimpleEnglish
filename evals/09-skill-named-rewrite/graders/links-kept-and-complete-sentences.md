---
type: llm
focus: last_message
---
The output is a rewrite of a README section. The source links these statements: (a) wrong AWS credentials cause a permission error; (b) sqlpipe retries on its own, so it can run unattended; (c) the AccessDenied error means the IAM role on the host does not allow writes to the bucket. Check these claims about the prose (ignore code spans) and fail if any one is false:

1. Each of the three links survives. The link can be one sentence, or two sentences joined by a connecting word ("because", "so", "if", "then", "as a result"). Two adjacent bare sentences with the link deleted ("sqlpipe retries failed operations automatically. You can run sqlpipe without watching it.") fail.
2. Every conditional instruction puts the condition before the command. "If the sync fails with X, make sure that Y" passes. "Make sure that Y if the sync fails with X" fails.
3. Every sentence is complete: a subject or an imperative verb, a finite verb, and its articles. A fragment like "Credentials required before start." fails. This checks telegraph style, not length. Long complete sentences pass.

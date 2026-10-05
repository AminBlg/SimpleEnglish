---
type: llm
focus: last_message
---
Check these claims and fail if any one is false:

1. The output does not restate the task. It does not begin with a sentence like "Here are the two sections" or "Below is the documentation", and it does not repeat the list of facts from the prompt as a list.
2. The output contains no closing paragraph that summarizes what was written or offers more help.
3. The output does not repeat the same fact in both sections unless the second mention is needed for the step (for example, naming `--dsn` in the troubleshooting fix is allowed; repeating the full install command in Troubleshooting is not).

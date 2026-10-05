---
type: llm
focus: last_message
---
Check this claim about the fix instructions in the output and fail if it is false:

Every instruction that carries a condition puts the condition before the command. "If the directory does not exist, create it." passes. "Create the directory, if it does not exist." fails. An instruction with no condition passes.

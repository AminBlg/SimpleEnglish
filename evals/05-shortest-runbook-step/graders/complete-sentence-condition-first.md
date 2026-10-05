---
type: llm
focus: last_message
---
The output is one rewritten runbook step. The source was "Ensure the backup exists before running the migration." Check these claims and fail if any one is false:

1. The output is a complete sentence: it has a finite verb and keeps the articles ("the backup", "the migration"). "Backup must exist before migration." fails. "Make sure that the backup exists before you run the migration." passes.
2. The condition or the check comes before the action. A sentence that names the migration first and the backup after ("Run the migration only after the backup exists") fails.
3. The output contains no extra step, no explanation, and no note about the rewrite. One sentence, or two short ones at most.

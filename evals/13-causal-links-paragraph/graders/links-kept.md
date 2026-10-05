---
type: llm
focus: last_message
---
The output rewrites a paragraph. The source links these statements: (a) the importer validates each row before it writes anything, and as a result a bad row never leaves the database half updated; (b) if a row fails, the importer stops and prints the line number, and it stops because later rows can depend on the failed one; (c) the reader fixes the row and runs the import again. Check these claims and fail if any one is false:

1. Link (a) survives: the output says that validation before writing is the reason a bad row cannot leave the database half updated, with a connecting word ("so", "because", "as a result") or in one sentence. Two bare sentences with no connector fail.
2. Link (b) survives: the output says that the importer stops because later rows can depend on the failed row. The reason is present and attached to the stop.
3. The condition "if a row fails" comes before the stop and the line number.
4. No fact is added. A rollback mechanism, a log file, an exit code, a transaction, a retry count, or a definition of validation is an added fact and fails. The hedge "may depend" becomes "can depend" or is stated as fact without changing the meaning.

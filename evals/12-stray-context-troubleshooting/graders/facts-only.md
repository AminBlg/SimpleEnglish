---
type: llm
focus: last_message
---
The output rewrites a troubleshooting paragraph. The source states exactly these facts: when `fastcopy` stops with `error: disk quota exceeded`, the target volume is probably out of space; free some space; run the command again. Check these claims and fail if any one is false:

1. Every statement is in the list above or follows directly from it. A command to measure disk use (df, du), a quota-raising step, a mention of the source volume, a log location, or a definition of "quota" is an added fact and fails.
2. All three facts survive, and the word "probably" or an equivalent keeps the uncertainty. The cause is not stated as certain.
3. The cause and the fix stay linked: the instruction to free space follows the cause with a connecting word or in the next sentence, and the instruction to run the command again follows the freeing.
4. The output contains no detail from the earlier remark about a nightly job or a host.

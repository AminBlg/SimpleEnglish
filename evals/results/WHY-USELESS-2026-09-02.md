# Why the skill reads as useless (2026-09-02, interim)

1. Fresh sonnet-4-6 docs, no skill, setting-sources off: 0.00 viol/100w on both runs. Skill runs: 0.98 and 1.27. The baseline the README beats is not what the user sees today.
2. Committed baseline (56 gens): slop_word = 0. Headline 74.6% = synonym_rotation 33, sentence_over_limit 27, semicolon 16, trailing_condition 16, contraction 11, banned_modal 8. Grammar obedience, not readability.
3. Replies: skill reply keeps em-dashes (12 base / 17 old / 13 plain over 8 files; fresh run 9,7 vs 6,4), bold spans 41/25/27, 14-16 sentences vs cap 5, ~190-250 words. Loophole: "Code blocks and list items do not count" so the model bullets everything.
4. Claude Code's own prompt already says short, direct, no headers for simple questions. Hook adds ~5.9k cached tokens per session for that.
5. Pending: micro prompt (8 lines) vs full skill on 8 reply scenarios.

## Decisive run (8 reply scenarios, sonnet-4-6 low, setting-sources off, 2026-09-02)
| cond | words | sentences | <=5 sent | em-dash | bold | headers | linter viol/100w |
| base | 241 | 13.1 | 1/8 | 32 | 52 | 20 | 5.95 |
| skill (system-prompt.md, ~1.5k tok) | 173 | 10.2 | 0/8 | 17 | 24 | 5 | 2.70 |
| micro (8 lines, ~70 tok) | 150 | 5.4 | 6/8 | 2 | 0 | 0 | 3.34 |
Skill wins only on its own linter. Micro wins on everything a reader sees.
Root cause: the skill optimizes for evals/ste_lint.py, and 50+ rules dilute the 5 that matter. Loophole: "list items do not count" toward the cap.
Files: r8/*.txt, ../useless/*.txt (docs + meta).

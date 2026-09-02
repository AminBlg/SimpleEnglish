# Benchmark results

**76.1% fewer STE violations per 100 words with the skill, averaged across 9 models x 8 tasks (144 generations, measured).**

| Model | Baseline viol/100w | Skill viol/100w | Reduction | Baseline sent. len | Skill sent. len | Output tok (base->skill) |
|---|---|---|---|---|---|---|
| claude-fable-5-1 | 1.77 | 0.33 | 81.4% | 12.9 | 9.8 | 348 -> 236 |
| claude-fable-5 | 2.73 | 0.51 | 81.3% | 15.1 | 9.6 | 285 -> 250 |
| claude-opus-5 | 2.13 | 0.32 | 85.0% | 14.1 | 10.8 | 272 -> 241 |
| claude-opus-4-8 | 1.05 | 0.62 | 41.0% | 10.7 | 10.0 | 260 -> 235 |
| claude-opus-4-7 | 2.28 | 0.42 | 81.6% | 13.0 | 10.8 | 243 -> 226 |
| claude-opus-4-6 | 2.24 | 0.4 | 82.1% | 10.9 | 9.0 | 185 -> 176 |
| claude-opus-4-5-20251101 | 2.55 | 0.57 | 77.6% | 11.1 | 8.5 | 196 -> 159 |
| claude-sonnet-5 | 2.67 | 0.53 | 80.1% | 10.0 | 9.7 | 266 -> 205 |
| claude-sonnet-4-6 | 2.06 | 0.52 | 74.8% | 11.7 | 10.2 | 168 -> 162 |

## Judge pass (blind pairwise)

For each model x scenario pair, claude-opus-4-8 scored the baseline text and
the skill text on a 0-10 rubric, twice with the texts in both orders. The
two scores were averaged to cancel position bias. The judge saw no labels.

Result: the skill output scored higher in 61 of 72 pairs, tied in
5, and lost in 6. Mean rubric score: 8.29 with the skill, 6.15 without.

| Model | Skill wins | Ties | Losses |
|---|---|---|---|
| claude-fable-5-1 | 8 | 0 | 0 |
| claude-fable-5 | 8 | 0 | 0 |
| claude-opus-5 | 7 | 1 | 0 |
| claude-opus-4-8 | 5 | 1 | 2 |
| claude-opus-4-7 | 7 | 1 | 0 |
| claude-opus-4-6 | 8 | 0 | 0 |
| claude-opus-4-5-20251101 | 6 | 0 | 2 |
| claude-sonnet-5 | 5 | 2 | 1 |
| claude-sonnet-4-6 | 7 | 0 | 1 |

Caveats: one judge model, judged once per order. The judge is a Claude
model and the texts are Claude output, so family bias is possible. Pairs
judged before effort pinning inherited the ambient setting, so the judge
pass is not uniform: 24 of 72 judge files record a
`judge_effort` and the rest pre-date the pin. Raw judge files:
results/raw/*__judge__*.json. Reproduce with
`python3 evals/run_bench.py --judge`.

## Honest number warnings

- The linter is a regex pass (see ste_lint.py header). It undercounts real STE
  violations: no passive-voice or part-of-speech detection. It counts the same
  way for both conditions, so the comparison is fair even where the absolute
  numbers are low.
- The skill condition sends SKILL.md in the prompt, so its input tokens are
  higher by design. Output tokens are reported; draw your own conclusion.
- Reasoning effort is pinned to `low` and recorded per raw file. Levels
  present in raw/: `low`, `unrecorded`.
  Rows marked unrecorded pre-date the pin and inherited the ambient effortLevel;
  the table assumes they are also `low`, which matches their measured
  output-token profile, but treat that as inferred. Effort moves the numbers a lot:
  claude-opus-5 measured 85.0% at `low` and 90.2% at `xhigh` on the same scenarios.
- Output tokens include reasoning tokens. The highest `thinking_tokens` in
  raw/ is 298. On the models that reason, the column is more than final text.
- One generation per cell. Re-run the matrix for variance; the runner is
  resumable, delete results/raw to start fresh.
- No tool can guarantee ASD-STE100 compliance, including this one.

Reproduce: `python3 evals/run_bench.py` (Claude Code CLI, logged in).

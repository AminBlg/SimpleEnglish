# Benchmark results

**72.9% fewer STE violations per 100 words with the skill, averaged across 6 models x 8 tasks (96 generations, measured).**

| Model | Baseline viol/100w | Skill viol/100w | Reduction | Baseline sent. len | Skill sent. len | Output tok (base->skill) |
|---|---|---|---|---|---|---|
| claude-opus-4-8 | 1.05 | 0.62 | 41.0% | 10.7 | 10.0 | 260 -> 235 |
| claude-opus-4-7 | 2.28 | 0.42 | 81.6% | 13.0 | 10.8 | 243 -> 226 |
| claude-opus-4-6 | 2.24 | 0.4 | 82.1% | 10.9 | 9.0 | 185 -> 176 |
| claude-opus-4-5-20251101 | 2.55 | 0.57 | 77.6% | 11.1 | 8.5 | 196 -> 159 |
| claude-sonnet-5 | 2.67 | 0.53 | 80.1% | 10.0 | 9.7 | 266 -> 205 |
| claude-sonnet-4-6 | 2.06 | 0.52 | 74.8% | 11.7 | 10.2 | 168 -> 162 |

## Honest number warnings

- The linter is a regex pass (see ste_lint.py header). It undercounts real STE
  violations: no passive-voice or part-of-speech detection. It counts the same
  way for both conditions, so the comparison is fair even where the absolute
  numbers are low.
- The skill condition sends SKILL.md in the prompt, so its input tokens are
  higher by design. Output tokens are reported; draw your own conclusion.
- One generation per cell. Re-run the matrix for variance; the runner is
  resumable, delete results/raw to start fresh.
- No tool can guarantee ASD-STE100 compliance, including this one.

Reproduce: `python3 evals/run_bench.py` (Claude Code CLI, logged in).

## Judge pass (blind pairwise)

A second measurement, independent of the regex linter. For each of the 48
model x scenario pairs, claude-opus-4-8 scored the baseline text and the
skill text on a 0-10 rubric: can a tired non-native reader misread a
sentence, is every instruction executable as written, is filler present.
Each pair was judged twice with the texts in both orders. The two scores
were averaged to cancel position bias. The judge saw no labels.

Result: the skill output scored higher in 38 of 48 pairs, tied in 4, and
lost in 6. Mean rubric score: 8.31 with the skill, 6.12 without.

| Model | Skill wins | Ties | Losses |
|---|---|---|---|
| claude-opus-4-8 | 5 | 1 | 2 |
| claude-opus-4-7 | 7 | 1 | 0 |
| claude-opus-4-6 | 8 | 0 | 0 |
| claude-opus-4-5 | 6 | 0 | 2 |
| claude-sonnet-5 | 5 | 2 | 1 |
| claude-sonnet-4-6 | 7 | 0 | 1 |

Caveats: one judge model, judged once per order. The judge is a Claude
model and the texts are Claude output, so family bias is possible. Raw
judge files: results/raw/*__judge__*.json. Reproduce with
`python3 evals/run_bench.py --judge`.

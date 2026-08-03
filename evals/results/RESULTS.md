# Benchmark results

**81.5% fewer STE violations per 100 words with the skill, averaged across 6 models x 8 tasks (96 generations, measured).**

| Model | Baseline viol/100w | Skill viol/100w | Reduction | Baseline sent. len | Skill sent. len | Output tok (base->skill) |
|---|---|---|---|---|---|---|
| claude-opus-4-8 | 2.34 | 0.62 | 73.5% | 10.7 | 10.0 | 260 -> 235 |
| claude-opus-4-7 | 2.81 | 0.41 | 85.4% | 13.0 | 10.8 | 243 -> 226 |
| claude-opus-4-6 | 3.14 | 0.4 | 87.3% | 10.9 | 9.0 | 185 -> 176 |
| claude-opus-4-5-20251101 | 2.94 | 0.71 | 75.9% | 11.1 | 8.5 | 196 -> 159 |
| claude-sonnet-5 | 3.76 | 0.53 | 85.9% | 10.0 | 9.7 | 266 -> 205 |
| claude-sonnet-4-6 | 2.65 | 0.51 | 80.8% | 11.7 | 10.2 | 168 -> 162 |

## Methodology Notes and Limitations

- The linter uses regex checks (see `ste_lint.py`). It does not detect passive voice or part-of-speech violations. The evaluation is fair because both conditions use the same linter rules.
- The skill condition appends `SKILL.md` to the prompt, which increases the input token count. Output token counts are reported below.
- One generation is evaluated per model scenario. Delete the `results/raw` directory and run the benchmark script again to test variance.
- No tool can guarantee complete ASD-STE100 compliance.

Reproduce: `python3 evals/run_bench.py` (Claude Code CLI, logged in).

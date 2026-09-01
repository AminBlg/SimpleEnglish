# opencode run, 2026-09-01: two named-family models, skill 2.0.0

The same 8 scenarios and linter as the 1.3.0 run, with the 2.0.0 skill (`plain-english@6c31103`). 32 raw files; 0 cells stayed empty after retries (600-second timeouts). Compare with the same two models in `../opencode-2026-09-01/RESULTS.md`.

| Model | Baseline viol/100w | Skill viol/100w | Reduction |
|---|---:|---:|---:|
| muse-spark-1.2-contributor-free | 1.31 | 0.25 | 81.1% |
| nemotron-3-ultra-free | 2.36 | 0.53 | 77.6% |
| pooled | 1.76 | 0.36 | 79.4% |

Reproduce: `python3 evals/score_text_dir.py evals/results/opencode-2026-09-01-plain/raw`.

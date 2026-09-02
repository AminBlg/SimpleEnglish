# opencode run, 2026-09-01: free models, skill 1.3.0

One generation per cell on the 8 benchmark scenarios through `opencode run`, baseline against the skill at `main@c728c95` (1.3.0). Scored with `evals/ste_lint.py` (em-dash check and the slop lexicon included).

Coverage: five models completed their cells (nemotron-3.5-lightning has 15 of 16). Two models, hy3-free and x-preview-f-free, returned an empty response on every attempt and retry that day (an endpoint error, not a timeout), so they have no rows. Empty cells are excluded from the rates and total 33 of 112 files.

| Model | Baseline viol/100w | Skill viol/100w | Reduction |
|---|---:|---:|---:|
| big-pickle | 3.06 | 0.65 | 78.7% |
| mimo-v2.5-free | 1.04 | 0.46 | 55.5% |
| muse-spark-1.2-contributor-free | 1.37 | 0.24 | 82.4% |
| nemotron-3-ultra-free | 2.30 | 0.71 | 69.2% |
| nemotron-3.5-lightning-free | 2.87 | 0.45 | 84.3% |
| pooled | 2.16 | 0.49 | 77.5% |

Provenance, from asking each model who made it: muse-spark reports Meta, the two nemotron models report NVIDIA, mimo-v2.5 reports Anthropic (so it is not independent evidence), big-pickle does not say. Self-reported identity is weak evidence.

Reproduce the table: `python3 evals/score_text_dir.py evals/results/opencode-2026-09-01/raw`.

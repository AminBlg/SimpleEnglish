# opencode run, 2026-09-01: seven free models, skill 1.3.0

One generation per cell on the 8 benchmark scenarios through `opencode run`, baseline against the skill at `main@c728c95` (1.3.0). Scored with `evals/ste_lint.py` (em-dash check and the slop lexicon included). 112 raw files; 33 cells stayed empty after two retry passes because the model timed out at 600 seconds, and they are excluded from the rates.

| Model | Baseline viol/100w | Skill viol/100w | Reduction |
|---|---:|---:|---:|
| big-pickle | 3.06 | 0.65 | 78.7% |

Provenance, from asking each model who made it: muse-spark reports Meta, the two nemotron models report NVIDIA, mimo-v2.5 reports Anthropic (so it is not independent evidence), big-pickle, hy3 and x-preview-f do not say. Self-reported identity is weak evidence.

Reproduce the table: `python3 evals/score_text_dir.py evals/results/opencode-2026-09-01/raw`.

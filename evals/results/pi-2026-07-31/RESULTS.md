# Pi benchmark results

**The skill reduced mean linter violations by 67.2% to 88.0% across 4 models.**

This run contains 64 generations: 4 models x 8 scenarios x 2 conditions.

| Model | Baseline viol/100w | Skill viol/100w | Reduction | Final words (base -> skill) | Scenarios (better/tied/worse) | Cost |
|---|---:|---:|---:|---:|---:|---:|
| `zai/glm-5.2:max` | 2.56 | 0.40 | 84.4% | 95.0 -> 86.6 | 6/2/0 | $0.000000 |
| `openai-codex/gpt-5.6-sol:medium` | 1.33 | 0.16 | 88.0% | 89.5 -> 100.5 | 5/3/0 | $0.534910 |
| `openai-codex/gpt-5.6-terra:medium` | 1.69 | 0.48 | 71.6% | 76.0 -> 78.6 | 4/3/1 | $0.156424 |
| `openai-codex/gpt-5.6-luna:medium` | 1.28 | 0.42 | 67.2% | 88.2 -> 96.2 | 5/2/1 | $0.016152 |

## Method

The runner used the same scenarios, skill prompt, linter, and per-scenario averaging as `run_bench.py`.
It sent only the scenario prompt for the baseline condition.
It added the complete `SKILL.md` text for the skill condition.
Both conditions used this neutral system prompt: `Return only the final text requested by the user.`

Pi tools, skills, prompt templates, extensions, context files, and session persistence were disabled.
The runner made one generation for each matrix cell and did not run a judge pass.

## Reproduce

```bash
python3 evals/run_pi_bench.py \
  --results-dir evals/results/pi-2026-07-31 \
  --model zai/glm-5.2:max \
  --model openai-codex/gpt-5.6-sol:medium \
  --model openai-codex/gpt-5.6-terra:medium \
  --model openai-codex/gpt-5.6-luna:medium
```

Delete `raw/` first to replace the committed generations. Existing raw files are skipped.

## Caveats

- The regex linter undercounts some violations and reports some false positives.
  For example, it treats descriptive sentences with a non-leading `when` clause as trailing conditions.
- One generation per cell does not measure model variance.
- Provider output-token counts can include hidden reasoning tokens.
  The table reports final-text word counts instead.
- Costs are provider-reported estimates, not billing records.
- The run measures the linter score, not ASD-STE100 certification or overall writing quality.

# OpenAI API run, 2026-09-01

One run of the 8 benchmark scenarios on `gpt-4.1-mini` through the Responses API, baseline against the skill at `main@9e6f747`. Scored with `evals/ste_lint.py` as of `c728c95` (em-dash check included).

| Model | Baseline viol/100w | Skill viol/100w | Reduction |
|---|---:|---:|---:|
| gpt-4.1-mini | 3.43 | 0.14 | 95.8% |

- Prompts: the same `build_prompt` wrapping as `evals/run_bench.py`, `max_output_tokens` 700, no reasoning setting.
- Tokens: 44,198 in, 1,964 out. Cost: $0.02 (`usage.json`).
- One generation per cell, no repeats. Baseline wrote 758 words, skill 692.
- Reproduce the table: `python3 evals/score_text_dir.py evals/results/openai-2026-09-01/raw`.

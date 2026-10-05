# Reply rerun, 2026-10-05: the 2.0.1 figure holds, and the prompt header changes it

This run tests why a rerun on 2026-09-30 gave 2.0.1 a 70.5% reduction in visible reply defects, against the 95% that `../rebuild-2026-09-02/RESULTS.md` publishes. The 2026-09-30 outputs were in a scratchpad that a restart erased, so that run is not in the repo.

All cells: claude-sonnet-4-6, low effort, `--setting-sources ""`, the 8 questions in `evals/reply_scenarios.json`, one generation per cell, two runs. Visible defects are em-dashes, bold spans, headers, and bullets, summed over both runs.

## Conditions

The files in `in/` are the texts that the model received with `--append-system-prompt`.

| label | file | content |
|---|---|---|
| 2.0.1 | `in/2.0.1-block.md` | The rule block of `prompts/system-prompt.md` at commit `d2a51b7`, without the page header. The 2026-09-02 run sent this text. |
| 2.0.1-file | `in/2.0.1-file.md` | The same file with its header ("Standalone system prompt", "paste this block"). The 2026-09-30 run sent files in this form. |
| 2.1.1 | `in/2.1.1-block.md` | The rule block of `prompts/system-prompt.md` at tag `v2.1.1`, cut by `check_numbers.rule_block()`. The SessionStart hook sends the same block. |

## Results

| CLI | condition | visible defects | baseline | reduction | mean words |
|---|---|---:|---:|---:|---:|
| Claude Code 2.1.258 (`cli258-*`) | 2.0.1 | 16 | 305 | 94.8% | 156 |
| Claude Code 2.1.289 (`cli289-*`) | 2.0.1 | 8 | 272 | 97.1% | 131 |
| Claude Code 2.1.289 | 2.0.1-file | 72 | 272 | 73.5% | 159 |
| Claude Code 2.1.289 | 2.1.1 | 25 | 272 | 90.8% | 237 |

Claude Code 2.1.258 is the version that the 2026-09-02 run used. It was installed from npm for this run. It prints MCP warnings after its JSON output, so a wrapper passed only the JSON line to the script.

The same rules gave 8 defects as a bare block and 72 with the page header. The CLI version did not move the result. With the same text as in the published run, the 2.0.1 figure of 95% reproduces. Plugin users get the bare block, because `src/hooks/simple-english-activate.js` removes the header.

Release 2.1.1 has no five-sentence cap. Its replies are longer, so it has more defects in total. Per 100 words, 2.1.1 has 0.66 and 2.0.1 has 0.38. With 16 replies per condition, this run cannot tell whether that difference is real.

## Limits

- One model, two runs, one generation per cell.
- The scorer counts formatting only. It does not detect facts that a reply adds or drops.
- A 13-line auto-memory file for `/tmp` was in the context of every call, as in the 2026-09-02 run. It holds no writing rules.

## Reproduce

```
python3 evals/run_reply_bench.py --report-only --skill 2.0.1=evals/results/rerun-2026-10-05/in/2.0.1-block.md --out evals/results/rerun-2026-10-05/cli258-r1
python3 evals/run_reply_bench.py --report-only --skill 2.0.1=evals/results/rerun-2026-10-05/in/2.0.1-block.md --skill 2.0.1-file=evals/results/rerun-2026-10-05/in/2.0.1-file.md --skill 2.1.1=evals/results/rerun-2026-10-05/in/2.1.1-block.md --out evals/results/rerun-2026-10-05/cli289-r1
```

Change `r1` to `r2` for the second run. The visible-defect column above is the sum of the em-dash, bold, headers, and bullets columns over both runs.

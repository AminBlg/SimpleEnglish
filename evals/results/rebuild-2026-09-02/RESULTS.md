# Rebuild benchmark, 2026-09-02: 2.0.1 against 1.3.0 and 2.0.0

The audit in `../WHY-USELESS-2026-09-02.md` found that the old benchmark measured obedience to the regex linter, not what a reader sees. This page scores what a reader sees: sentences (list items counted), em-dashes, bold spans, headers, and bullets in chat replies, plus the STE linter on documents. All Claude cells: claude-sonnet-4-6, low effort, `--setting-sources ""`, one generation per cell. Prompts are the standalone system prompts of each version (`v13-system-prompt.md`, `v2-system-prompt.md`, and `../../prompts/system-prompt.md` for 2.0.1). `v3` is the first 2.0.1 draft with the reply block first. `v3b` is the shipped 2.0.1 with the reply block last and a count-before-send sentence.

## Replies: 8 chat questions, two runs

Run 1 (`reply1/`):

| condition | n | words | sentences | under cap | em-dash | bold | headers | bullets | openers | linter viol/100w |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| baseline | 8 | 216 | 16.6 | 0/8 | 37 | 39 | 13 | 29 | 0 | 5.02 |
| v13 | 8 | 230 | 18.4 | 0/8 | 27 | 28 | 21 | 26 | 0 | 3.65 |
| v2 | 8 | 192 | 15.6 | 0/8 | 29 | 37 | 4 | 28 | 0 | 3.77 |
| v3 | 8 | 156 | 7.2 | 1/8 | 10 | 0 | 0 | 0 | 0 | 3.95 |
| v3b | 8 | 134 | 7.4 | 4/8 | 2 | 0 | 0 | 0 | 0 | 1.75 |

Run 2 (`reply2/`):

| condition | n | words | sentences | under cap | em-dash | bold | headers | bullets | openers | linter viol/100w |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| baseline | 8 | 216 | 16.9 | 0/8 | 25 | 40 | 12 | 23 | 0 | 4.45 |
| v13 | 8 | 241 | 20.0 | 0/8 | 36 | 49 | 16 | 35 | 0 | 4.04 |
| v2 | 8 | 176 | 13.1 | 0/8 | 14 | 35 | 0 | 24 | 0 | 2.41 |
| v3 | 8 | 138 | 7.0 | 2/8 | 14 | 0 | 0 | 0 | 0 | 2.83 |
| v3b | 8 | 158 | 8.5 | 1/8 | 3 | 2 | 0 | 4 | 0 | 1.70 |

Visible defects pooled over both runs (over-cap sentences + em-dashes + bold + headers + bullets): baseline 406, 2.0.0 321, 2.0.1 (v3b) 58. That is 85.7% fewer than baseline and 81.9% fewer than 2.0.0. The five-sentence cap is met in 5 of 16 replies. Sonnet at low effort still explains at length when the question says "explain".

| Run | 2.0.1 wins | ties | losses | mean 2.0.0 | mean 2.0.1 |
|---|---:|---:|---:|---:|---:|
| reply1 | 7 | 1 | 0 | 6.38 | 8.19 |
| reply2 | 7 | 0 | 1 | 6.50 | 8.12 |

## Replies on gpt-4.1-mini (`gpt-4.1-mini-reply/`)

| condition | n | words | sentences | under cap | em-dash | bold | headers | bullets | openers | linter viol/100w |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| baseline | 8 | 290 | 23.0 | 1/8 | 2 | 64 | 27 | 101 | 1 | 3.61 |
| v2 | 8 | 72 | 6.2 | 5/8 | 0 | 0 | 0 | 7 | 0 | 1.92 |
| v3 | 8 | 82 | 5.0 | 8/8 | 0 | 0 | 0 | 0 | 0 | 1.52 |
| v3b | 8 | 82 | 5.2 | 6/8 | 0 | 0 | 0 | 0 | 0 | 1.38 |

`v3` files were generated with the first 2.0.1 draft on 2026-09-02, `v3b` with the shipped prompt on 2026-09-04. Spend: $0.015 plus $0.004 (`usage.json`, `usage-v3b.json`).

## Documents: the 8 benchmark scenarios (`docs/`)

| Model | Condition | n | viol/100w | Reduction vs baseline | em-dash | bold spans | words |
|---|---|---:|---:|---:|---:|---:|---:|
| (single) | baseline | 8 | 4.09 | 0.0% | 10 | 12 | 88 |
| (single) | v13 | 8 | 2.11 | 48.5% | 2 | 7 | 94 |
| (single) | v2 | 8 | 1.70 | 58.4% | 2 | 16 | 95 |
| (single) | v3 | 8 | 2.40 | 41.2% | 4 | 7 | 93 |
| (single) | v3b | 8 | 0.91 | 77.8% | 2 | 7 | 96 |

The STE linter still applies to documents, where the structural rules are the point. 2.0.1 (`v3b`) scores 0.91, the best of the four, on one run. One run moves by about 0.5 on this model, so read the document rows as parity or better, not as a ranking.

## Limits

- One generation per cell. Two runs for replies, one for documents.
- One judge model, same family as the texts.
- The reply cap is the weakest rule: 5 of 16 sonnet replies and 8 of 8 gpt-4.1-mini replies meet it.

## Reproduce

```
python3 evals/run_reply_bench.py --report-only --skill v3b=prompts/system-prompt.md --out evals/results/rebuild-2026-09-02/reply1
python3 evals/score_text_dir.py evals/results/rebuild-2026-09-02/docs
```

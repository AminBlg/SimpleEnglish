# Pivot benchmark, 2026-09-01: Plain-by-default (2.0.0) against the 1.3.0 skill

The 2.0.0 skill changes the default mode from strict-leaning STE to Plain: the
same structural rules, plus six plain-English rules for replies and for
explanations written for readers outside the field, plus a reply register.
This page compares the two skills on the same tasks, the same models, and the
same linter (`evals/ste_lint.py` at `plain-english`, which counts em-dashes
and the 69-term slop lexicon). One generation per cell unless stated.

## Documents: the 8 benchmark scenarios

| Harness | Skill | Baseline viol/100w | Skill viol/100w | Reduction | Notes |
|---|---|---:|---:|---:|---|
| claude-sonnet-4-6, low | 1.3.0 | 3.34 | 0.89 (6/675w) | 73.4% | committed raw, re-linted |
| claude-sonnet-4-6, low | 2.0.0 | 2.45 | 1.04 (7/676w) | 57.7% | `claude-sonnet-4-6/plain/` |
| gpt-4.1-mini, 2 runs | 1.3.0 | 3.75 | 0.67 (9/1351w) | 82.2% | `openai/current*/` |
| gpt-4.1-mini, 2 runs | 2.0.0 | 4.55 | 0.72 (8/1105w) | 84.1% | `openai/plain*/` |

An opencode run on nemotron-3-ultra and muse-spark-1.2 (named non-Claude families) was still running when this page was written; its rows land in a follow-up commit under `evals/results/opencode-2026-09-01-plain/`.

Skill-side rates differ by 0.15 (Claude) and 0.05 (gpt) per 100 words, one
violation either way. Both are inside single-run noise: the two gpt-4.1-mini
runs of the same 1.3.0 skill scored 0.14 and 1.21.

Blind pairwise judge on the Claude documents (claude-sonnet-4-6, both orders,
no labels), 2.0.0 against 1.3.0:

| Run | 2.0.0 wins | ties | losses | mean 1.3.0 | mean 2.0.0 |
|---|---:|---:|---:|---:|---:|
| final text | 1 | 3 | 4 | 8.50 | 8.06 |
| previous text (`ce42d9c`, differs by three trimmed sentences) | 2 | 5 | 1 | 8.12 | 8.31 |

The two runs disagree by more than the gap inside either one. The one
recurring loss, `runbook-terse`, is two valid renderings of the same step
("Before you run the migration, make sure that the backup exists." against
"Make sure that the backup exists. Then run the migration."). Read: documents
are at parity.

Three earlier versions of the pivot were worse on documents and were fixed
before this comparison: an unbounded define-terms rule (gpt-4.1-mini fell to
68.9%), an open "pick one" for check/verify and config/settings (rotation
hits), and a cut procedural exemplar (headed, numbered procedures came back
when it returned). The commits on `plain-english` record each step.

## Replies: 8 chat questions with a jargon term each

`evals/reply_scenarios.json`, claude-sonnet-4-6 at low effort, skill passed as
an appended system prompt. Scored with `evals/run_reply_bench.py`.

| Condition | mean sentences | viol/100w | slop/100w | words | filler closers |
|---|---:|---:|---:|---:|---:|
| no skill | 9.1 | 3.29 | 0.14 | 186 | 0 |
| 1.3.0 skill | 8.2 | 2.94 | 0.00 | 163 | 0 |
| 2.0.0 skill | 7.9 | 1.68 | 0.00 | 169 | 0 |

Blind pairwise judge on the replies, 2.0.0 against 1.3.0 (claude-sonnet-4-6, both orders):

| Run | 2.0.0 wins | ties | losses | mean 1.3.0 | mean 2.0.0 |
|---|---:|---:|---:|---:|---:|
| final text | 3 | 0 | 5 | 7.81 | 7.44 |
| earlier text (`5886ea4`) | 6 | 0 | 2 | 6.94 | 7.56 |
| earlier text (`1065aa6`) | 5 | 1 | 2 | 7.56 | 7.88 |

Across the three runs the pivot leads 14 to 9 with 2 ties. The linter and the judge disagree on the final run; the linter measures the mechanical rules, the judge reads for a smart outsider. Both are reported.

The five-sentence cap in the reply register is not met by any condition at
low effort; the pivot moves the mean from 8.2 to 7.9. The term-definition
heuristic (`term_defined`) did not move (2-3 of 8 in every condition) and is
too crude to read.

## Limits

- One generation per cell except the gpt-4.1-mini pair. Means move by 0.4 on
  the judge between runs of the same text.
- The judge is one model (claude-sonnet-4-6) at low effort; both orders are
  scored and averaged to cancel position bias.
- The Claude account hit its session limit during one reply run. Every file
  that held the limit message was regenerated; `grep "session limit"` over the
  raw files returns nothing.
- OpenAI spend for the whole exercise: $0.16 (`openai/*/usage.json`).

## Reproduce

```
python3 evals/score_text_dir.py evals/results/pivot-2026-09-01/openai/plain
python3 evals/run_reply_bench.py --skill skills/simple-english/SKILL.md --out /tmp/reply
```

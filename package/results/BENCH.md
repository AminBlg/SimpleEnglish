# Benchmark

8 documentation scenarios, 2 models, 4 conditions. 64 runs.
Scored 2026-08-12 with `evals/ste_lint.py` and `package/ste_dict_lint.py`.
The generated table is `table.md`. This file adds the interpretation.

Conditions:

- `baseline` — the task prompt alone
- `skill` — `skills/simple-english/SKILL.md`, 4,969 tokens
- `core` — `package/ste-core.md`, about 1,400 tokens
- `core+dict` — `ste-core.md` and `not-approved.tsv`, about 14,850 tokens

| model | condition | n | violations/100w | not-approved/100w | residual/100w | mean sentence |
|---|---|---|---|---|---|---|
| claude-opus-4-8 | baseline | 8 | 1.05 | 20.08 | 15.14 | 10.7 |
| claude-opus-4-8 | skill | 8 | 0.62 | 11.37 | 5.63 | 10.0 |
| claude-opus-4-8 | core | 8 | 0.13 | 9.06 | 3.66 | 7.9 |
| claude-opus-4-8 | core+dict | 8 | 0.21 | 7.53 | 2.79 | 8.6 |
| claude-sonnet-4-6 | baseline | 8 | 2.06 | 26.38 | 19.70 | 11.7 |
| claude-sonnet-4-6 | skill | 8 | 0.52 | 12.22 | 6.30 | 10.2 |
| claude-sonnet-4-6 | core | 8 | 0.56 | 12.89 | 6.25 | 10.4 |
| claude-sonnet-4-6 | core+dict | 8 | 0.37 | 6.31 | 1.39 | 11.1 |

The three metrics measure different things. Read them separately.

- `violations/100w` — mechanical rules: sentence length, tense, modals,
  contractions, semicolons.
- `not-approved/100w` — every flagged word.
- `residual/100w` — flagged words after removal of 27 technical nouns of
  software documentation (`run`, `file`, `port`, `request`, and similar). Rule
  1.5 permits a technical noun, so the raw count charges the text for words the
  standard allows. `residual` is the better word-choice metric for this domain.

## Results

**The core replaces the skill at 3.6 times fewer tokens.** On mechanical rules
`core` scores 0.13 against 0.62 for `skill` on Opus 4.8. On Sonnet 4.6 the two
are level, 0.56 against 0.52. On word choice `core` is ahead on Opus 4.8
(residual 3.66 against 5.63) and level on Sonnet 4.6 (6.25 against 6.30).

**The word list earns its 13,448 tokens, most of all on the weaker model.**
Sonnet 4.6 falls from 6.25 to 1.39 residual, a drop of 78%. Opus 4.8 falls from
3.66 to 2.79, a drop of 24%, because it starts much lower.

**On Opus 4.8 the word list costs a small amount of sentence discipline.**
Violations rise from 0.13 to 0.21 and the mean sentence grows from 7.9 words to
8.6 words. A 13,448-token prefix competes for attention with the rule core. On
Sonnet 4.6 the effect is the opposite: violations fall from 0.56 to 0.37.

## What the words tell you

The words that survive in the `core+dict` runs are technical nouns of the
subject field: `run`, `file`, `port`, `requests`, `transfer`, `settings`. The
standard permits these under rule 1.5. The words that the word list removes are
real errors: `create`, `exists`, `permits`, `returned`, `now`, `verify`,
`reduces`. That is the evidence that the drop is a writing change and not an
artifact of the metric.

## How to read the numbers

The `core+dict` condition is scored with a linter built from the same file that
the condition puts in the prompt. Part of its gain is definitional. The
`baseline` and `skill` columns are the control. Both fall a long way from
`baseline` without ever seeing `not-approved.tsv`, so the metric responds to
real writing quality.

`ste-core.md` itself scores 7.08 raw flagged words per 100 words. That text is
about grammar, so it is full of `form`, `past`, `present`, and `speech`, which
is the worst case for a matcher with no part-of-speech tagger. Do not use that
number as a floor for product documentation. Use the `residual` column.

## Limits

- Claude models only. Behavior across model families is not tested.
- 8 scenarios per condition. The difference between `core` and `skill` on
  Sonnet 4.6 is inside the noise of a sample this size.
- Both linters are regex passes, not grammar parsers. Neither is a compliance
  verdict.
- The technical noun list is hand-written for software documentation. Another
  subject field needs a different list.

Reproduce with:

```
python3 bench_core.py              # generate, then score
python3 bench_core.py --score-only # score existing runs, no API calls
```

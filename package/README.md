# ASD-STE100 Issue 9, compressed

A machine-readable package of the ASD-STE100 Issue 9 writing rules and word
lists, made for a model context window.

Source, attribution, and the limits of this extraction: [`NOTICE.md`](NOTICE.md).

| File | Bytes | Tokens (o200k) | Tokens (cl100k) | Content |
|---|---|---|---|---|
| `ste-core.md` | 5,430 | 1,395 | 1,399 | The 53 writing rules, 9 sections |
| `approved.txt` | 10,362 | 4,285 | 4,267 | 841 rows, 770 approved words with part of speech |
| `not-approved.tsv` | 35,156 | 13,448 | 13,383 | 1,297 rows, 1,238 words that are not approved, with approved alternatives |
| **Package** | **50,948** | **19,128** | **19,049** | |
| Source PDF text | 1,170,813 | 196,973 | 197,066 | 434 pages |

Compression: **10.3x on tokens**. The two tokenizers agree within 0.4%.

A word with two parts of speech gets one row for each. The row count is therefore
larger than the word count.

## How to use it

- Rules only, 1,395 tokens: put `ste-core.md` in the system prompt.
- Rules and word choice, 14,843 tokens: add `not-approved.tsv`.
- `approved.txt` is not a prompt input, but `ste_dict_lint.py` reads it. The
  linter uses it to drop each not-approved entry whose spelling is also an
  approved word. Do not remove the file to save tokens in the prompt.

## Why plain text and not a symbolic notation

The first step of this work was a survey of prompt-compression methods. The
result: a compact syntax that only a model understands, and model-agnostic
behavior, cannot both hold.

- Soft prompts and gist tokens reach 26x compression, but they live in one
  model's embedding space. A compressor trained on one model family fails on
  another.
- A symbolic metalanguage reaches 62-81% compression, but operator fidelity
  measured across 8 models ranges from 0% to 98%. The authors of that study
  conclude that the method is not model-agnostic.
- Discrete text transfers, because the payload stays in the common text space.

The lever that remains is deletion, not encoding: remove what a model can
reconstruct, keep what it cannot. What it cannot reconstruct is the arbitrary
part of the standard — the numeric limits (20, 25, 6, 3), the banned verb
forms, and the word list. That is what this package keeps.

The token counts above show the same point from the other side. The package
costs the same number of tokens under two different vocabularies. A dense
private notation does not have that property.

## How the package was made

```
pdftotext -layout ASD-STE100_ISSUE9.pdf ste9.txt
python3 parse_dict.py ste9.txt     # -> dict.json
python3 emit.py .                  # -> approved.txt, not-approved.tsv
```

`ste-core.md` was written by hand from Part 1 of the standard. The rule numbers
match the standard, so each line traces back to its source.

`not-approved.tsv` keeps column 1 (word and part of speech) and column 2 (the
approved alternatives). `approved.txt` keeps column 1 only. `emit.py` drops the
approved meaning on purpose, so that file carries no definition text. Both files
drop column 3 and column 4, which hold the example sentences and most of the
bytes of Part 2.

The package is therefore a derived index, not a copy of the standard. Read the
standard itself for the meanings, the examples, and the explanatory text.

## Parser fidelity

| Count | This package | The standard states |
|---|---|---|
| Approved words | 770 (841 rows) | 875 |
| Words that are not approved | 1,238 (1,297 rows) | 1,274 |

Both counts are below the counts of the standard. The parser invented no
entries. A row is one word with one part of speech, so a word with two parts of
speech gets two rows.

80 rows in `not-approved.tsv` have no alternative in column 3, because the
column boundary detection lost the text on those rows. The word is still
correctly marked as not approved.

`PRESSURE` and other technical nouns are absent by design. The standard states
that the dictionary does not include technical nouns or technical verbs.

## Linters

Two independent tools. Read their scores separately, never as one number.

- `../evals/ste_lint.py` counts mechanical rule violations: sentence length,
  contractions, banned modals, perfect tenses, "-ing" clauses, semicolons.
  It does not look at word choice.
- `ste_dict_lint.py` counts words that are not approved. It does not look at
  the mechanical rules.

```
python3 ste_dict_lint.py file.md
python3 ste_dict_lint.py --self-test
```

### Known ceiling of `ste_dict_lint.py`

The tool has no part-of-speech tagger. The standard's entries are
part-of-speech specific: `use (n)` is not approved, but `USE (v)` is approved.
The tool removes each entry whose spelling is also an approved word, which
loses recall and removes most false hits.

Technical nouns still cause false hits, because rule 1.5 permits them but the
dictionary does not list them. The tool therefore reports two numbers.
`not_approved_per_100w` counts every hit. `residual_per_100w` removes 27
technical nouns of software documentation. Use `residual` for software text,
and extend `TECHNICAL_NOUNS` for another subject field.

No tool in this package is a compliance verdict.

## Benchmark

`bench_core.py` compares four conditions on 8 documentation scenarios:
`baseline` (no instructions), `skill` (the full 4,969-token `SKILL.md`),
`core`, and `core+dict`. Full results and their limits are in
`results/BENCH.md`.

| model | condition | violations/100w | residual/100w |
|---|---|---|---|
| opus-4-8 | baseline | 1.05 | 15.14 |
| opus-4-8 | skill | 0.62 | 5.63 |
| opus-4-8 | core | **0.13** | 3.66 |
| opus-4-8 | core+dict | 0.21 | **2.79** |
| sonnet-4-6 | baseline | 2.06 | 19.70 |
| sonnet-4-6 | skill | 0.52 | 6.30 |
| sonnet-4-6 | core | 0.56 | 6.25 |
| sonnet-4-6 | core+dict | **0.37** | **1.39** |

`residual/100w` counts flagged words after removal of the technical nouns of
software documentation, which rule 1.5 permits.

The 1,395-token core matches or beats the 4,969-token skill on both metrics.
The word list then cuts word-choice errors by a further 78% on Sonnet 4.6 and
24% on Opus 4.8, which starts much lower. On Opus 4.8 the word list costs a
small amount of sentence discipline, because a 13,448-token prefix competes
for attention with the rule core.

The `core+dict` condition is scored with a linter built from the same file that
the condition puts in the prompt. Part of any word-choice gain is therefore
definitional. The `baseline` and `skill` columns show how much is real.

The benchmark runs Claude models only. Token stability across tokenizers is
measured. Behavior across model families is **not** tested.

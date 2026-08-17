# Step 1 — Can LLMs compress meaning into abstract syntax, model-agnostically?

Date: 2026-08-12. Purpose: decide the encoding for a compressed ASD-STE100 rule package.

## Verdict

No. "Abstract syntax that is only meaningful to models" and "model agnostic" are
mutually exclusive with current evidence. The two properties trade against each other:

| Family | Compression | Transfers across model families? |
|---|---|---|
| Soft prompts / gist tokens (Mu & Goodman) | up to 26x | No. Lives in one model's embedding space. Cannot be used with the untuned model. A compressor trained on LLaMA fails on Qwen or Mistral. |
| Symbolic metalanguage (SynthLang, MetaGlyph) | 62-81% | No. Fidelity spread is 0% to 98% across 8 models. |
| Discrete text compression (LLMLingua-2, token pruning) | 2-20x | Yes. Transfers because the payload stays in the common text space, not a model-specific latent space. |

## The decisive numbers (arXiv 2601.07354, MetaGlyph)

Tested 8 models, 3B to 1T parameters, with math operators as instruction primitives
(in, not, intersect, transform, implies, compose). Compression 62-81%.

Membership operator fidelity:
- GPT-5.2 Chat: 91.3%
- Gemini 2.5 Flash: 49.9%
- Llama 3.2 3B: 33.3%
- Claude Haiku 4.5: 26%
- Qwen 2.5 7B: 20.4%
- Gemma 3 12B, OLMo 3 7B: 0%

Implication operator fidelity: Kimi K2 98.1%, Gemini 2.5 Flash 33.5%, all others 0%.

The authors conclude that symbolic compression is not model-agnostic. The pattern is
U-shaped: small models show moderate fidelity, mid-size instruction-tuned models collapse
to zero, frontier models recover. Effectiveness depends on architecture and training.

The authors also state that the study is short and does not characterize limits.

## The strongest counter-evidence: Telegraph English

Telegraph English (arXiv 2605.04426, May 2026) rewrites text into a dialect with
about 40 logical and relational symbols (=, →, ⇒, ∴, ∵, ↑, ↓, ∧, ∨, ¬, ≈, ≠). It
reports approximately 50% token reduction with 99.1% key-fact accuracy on
GPT-4.1, and it beats LLMLingua-2 on every model and task tested. The advantage
grows as the model gets smaller: up to 11 percentage points on GPT-4o-mini for
fine-detail questions.

That result is real, and it does not overturn the conclusion above. Three
reasons:

1. **The evaluation never leaves one model family.** Five OpenAI models: GPT-4.1,
   GPT-4o, GPT-4o-mini, GPT-4.1-nano, and a fine-tuned GPT-4o. The authors list
   this first among their limitations: "Our benchmark relies on OpenAI models
   that are not open-weight, limiting reproducibility; future work should extend
   evaluation to open models." MetaGlyph is the experiment that does cross
   families, and there the same class of symbols scores 91.3% on GPT-5.2 and 0%
   on Gemma 3 12B and OLMo 3 7B. The two results agree: symbols work inside the
   family that trained on them.
2. **The task is different.** Telegraph English compresses documents that a model
   must read. This package compresses instructions that a model must obey.
   MetaGlyph tested instructions, and that is the case that failed.
3. **The authors cap symbol density at three symbols per line**, because "dense
   symbol chains became opaque even to GPT-4." That is the failure mode of
   symbolic compression, stated by its own advocates.

Telegraph English also costs an LLM call for each chunk that it compresses, and
the authors have not mapped how much the result depends on which model does the
rewrite. This package is a one-time deterministic parse.

One idea from that paper agrees with the design here: each output line holds one
atomic fact, so compression and indexing become the same operation.
`ste-core.md` follows the same shape, one rule for each line, with the rule
numbers of the standard kept as the index.

## Why invented notation fails

1. Tokenizers differ. The same glyph string splits into different token sequences per
   BPE vocabulary. A dense private notation is out-of-distribution for every model that
   did not see it.
2. A shorter byte string can tokenize longer. Byte count is not the metric. Token count
   under at least two tokenizers is the metric.
3. Any scheme that needs a decoder key must ship the key. The key costs more than the
   savings at rule-package scale.

## What does work, and is the real lever

Information-theoretic pruning inside plain text:
- Delete what the model already knows and can reconstruct.
- Keep only what the model cannot reconstruct: the arbitrary numeric limits (20 words,
  25 words, 6 sentences, 3-word noun chains), the arbitrary word choices, and the
  banned-form lists.
- Compression comes from deletion and structure, not from an encoding.

Symbols are safe only where the training distribution already carries them densely:
markdown structure, arrows in tables, standard punctuation. Not as operators that carry
instruction semantics.

## Scope fact for the ASD-STE100 package

Text extracted from ASD-STE100 Issue 9 (434 pages, 1,170,813 bytes):
- Part 1, writing rules: 94,798 bytes (8.7%). 53 rules in 9 sections. Highly compressible.
- Part 2, dictionary: 991,767 bytes (91.3%). About 900 approved words plus not-approved
  words. An arbitrary lookup table. Near-zero compressibility.

## Harness limit

`evals/run_bench.py` calls the Claude Code CLI (`claude -p`) and lists only Claude models.
Any model-agnostic claim cannot be verified with the harness as it stands. A second
runner for a non-Anthropic model is required to test the claim.

## Sources

- https://arxiv.org/html/2601.07354 (MetaGlyph, symbolic metalanguage)
- https://arxiv.org/pdf/2605.04426 (Telegraph English, structured symbolic rewriting)
- https://arxiv.org/pdf/2410.12388 (Prompt Compression for LLMs: A Survey)
- https://www.emergentmind.com/topics/gist-tokens
- https://arxiv.org/pdf/2308.08758 (Discrete Prompt Compression with RL)
- https://gist.github.com/ruvnet/8e9ade113348ecc84db24b0082554614 (SynthLang)

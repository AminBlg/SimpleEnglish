# Changelog

Each entry names the version, the date, and the measured effect where one exists.

## 2.1.0, 2026-09-16

- Removed: the five-sentence cap on the reply. The rule is gone from SKILL.md,
  the output style, the system prompt, the self-check, the Stop hook, and the
  linter. Users reported that replies on multi-part questions came out as one
  paragraph. A rescore of the committed 2026-09-02 replies shows the cap was
  met in only 5 of 16 replies, and that the same replies had 18.9% of sentences
  over 25 words against 5.7% for release 2.0.0, which had no formatting rule.
  The cap did not hold and it did not shorten sentences. (#35)
- Changed: `reader_check()` no longer counts over-cap sentences in
  `visible_total`, because the skill no longer asks for five sentences. The
  published reply figure moves from 86% fewer visible defects (406 to 58) to
  95% fewer (218 to 11), recomputed from the same raw files by
  `python3 evals/check_numbers.py`. The counted classes are now em-dashes,
  bold, headers, and bullets. `sentences` is still reported, as a count and
  not a limit.

## 2.0.2, 2026-09-08

- Fixed: the PostToolUse hook message said "Run the self-check in SKILL.md
  before you deliver." At least one harness read that as an instruction to
  search the install folder for a file. It read this instead of running the
  check inside the skill already loaded. The message now names the change
  directly. (#31)

## 2.0.1, 2026-09-04 to 2026-09-06

- Rebuilt the skill around two registers, the document and the reply, after
  an audit found the old benchmark measured obedience to the linter, not what
  a reader sees. SKILL.md is 1,825 tokens. The 53-rule catalog moved to
  `references/rule-catalog.md`. Visible reply defects (over-cap sentences,
  em-dashes, bold, headers, bullets) fell from 406 to 58 pooled over 16
  replies on claude-sonnet-4-6. A blind judge preferred 2.0.1 over 2.0.0 in
  14 of 16 pairs. Full method: `evals/results/rebuild-2026-09-02/RESULTS.md`.
- Added `evals/check_numbers.py`, which recomputes every published number
  from the raw files and fails the build on a mismatch. Wired into CI.
- Fixed the Codex hook file collision: Claude Code auto-discovers
  `hooks/hooks.json` at the plugin root, so the Codex configuration moved to
  `.codex-plugin/hooks.json`.
- Fixed: table rows in Markdown were blanked whole by the linter, which
  exempted every cell inside them from every check. Each cell is now its own
  sentence unit.
- Fixed: the PostToolUse hook linted Claude's own memory and configuration
  files. It now skips the Claude configuration directory and any path a
  `SIMPLE_ENGLISH_LINT_EXCLUDE` glob names.
- Fixed: the `claude-opus-4-8` benchmark row (1.05 baseline) did not
  reproduce. Re-run with a clean baseline: 3.64. Old files moved to
  `evals/results/raw-superseded/`.
- Removed `references/checklist.md`. Nothing loaded it, and its content
  restated the self-check, the catalog, and the linter.
- Took the ASD-STE100 word-list extractor and the word-choice linter from a
  closed pull request, without the extracted word lists themselves: the
  standard forbids reproducing them without written authority from ASD. Users
  build the lists locally from their own copy of the free PDF, in
  `tools/ste-dictionary/`.
- Added claude-fable-5-1 and claude-fable-5 rows to the linter benchmark, and
  seven opencode model rows.

## 2.0.0, 2026-09-01

- Pivoted the default mode from strict ASD-STE100 enforcement to Plain: the
  same structural rules, plus rules for readers outside the field and a
  reply register, with Strict kept as a document-only overlay.

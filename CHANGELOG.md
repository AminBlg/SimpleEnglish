# Changelog

Each entry names the version, the date, and the measured effect where one exists.

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

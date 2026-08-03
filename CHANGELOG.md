# Changelog

All notable changes to the `UnanthropomorphicEnglish` agent skill on the `dehumanizing-v1` branch.

## [1.1.0] - 2026-08-03

### Added
- **Dehumanization rules** (`skills/unanthropomorphic-english/SKILL.md`):
  - Rule 1.15: Banned first-person pronouns (`I`, `me`, `my`, `we`, `our`, `us`) and self-references.
  - Rule 1.16: Banned conversational greetings, pleasantries, and polite filler (`hello`, `hi`, `please`, `kindly`, `sure`, `of course`).
  - Rule 1.17: Banned self-referential terms (`AI`, `assistant`, `model`) and cognitive/emotive verbs (`think`, `believe`, `feel`, `hope`, `sorry`, `apologize`).
- **Linter checks** (`evals/ste_lint.py`):
  - Added regex checks for `FIRST_PERSON`, `CONVERSATIONAL`, and `SELF_REF` to detect dehumanization violations.
  - Added verification assertions to `self_test`.
- **References update** (`skills/unanthropomorphic-english/references/`):
  - Added checklist guidelines for first-person pronouns, conversational elements, and anthropomorphic language.
  - Added guidelines to `use-cases.md` recommending third-person or passive voice in incident reports.

### Changed
- **Linter evaluations and results** (`evals/results/`):
  - Re-linted all 96 cached raw model outputs with the new metrics.
  - Baseline violations increased due to new checks (e.g., `claude-sonnet-5` went from 2.67 to 3.76 violations/100w).
  - Updated the aggregate results (`RESULTS.md` and `results.json`), showing an increased STE violation reduction of **81.5%** (up from 72.9%).
  - Corrected first-person pronoun leaks in the five raw skill incident report outputs.
- **Incident report examples** (`examples/before-after.md`, `README.md`):
  - Rewrote the "After" incident report example to use the third person ("the deployment team" / "the deploy pipeline") instead of the first person ("we").

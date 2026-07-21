# Pressure tests

Test scenarios for this skill, with the baseline failures they exist to catch. Method: run each prompt in a fresh agent session twice — once without the skill (baseline), once with it — and score against the criteria. If a criterion passes at baseline, it proves nothing; the valuable criteria are the ones the baseline fails.

## Baseline results (recorded 2026-07-21, Claude Sonnet, no skill)

**Scenario 1 baseline failures:** sentences of 30-40 words; contractions (`It's`, `you'll`); dangling "-ing" clauses ("...file, making it easy to..."); synonym rotation — verify, confirm, check, and make sure all used for the same action; conditions after commands.

**Scenario 2 baseline failures (agent asked to write STE from memory):** invented rule numbers — cited "Rule 3.1: short sentences" and "Rule 4.2: active voice"; the real Rule 3.1 is verb forms and the real Rule 4.2 is omitted words. Kept passive voice ("are configured"). Dropped "that" after "make sure". Used "By using" as a gerund opener. Did not know the 20/25 procedural/descriptive split.

The skill exists to close those specific gaps: real rule numbers on paper, a classification step, a mechanical self-check.

## Scenario 1 — natural docs task

> Write documentation for a CLI tool called "sqlpipe" that syncs Postgres tables to S3 as Parquet files. Produce an introduction, a "Getting started" section, and a "Troubleshooting" section covering connection timeouts and permission errors. Around 350 words.

Pass criteria:
- [ ] No sentence over 20 words in Getting started / Troubleshooting (procedural)
- [ ] No sentence over 25 words in the introduction (descriptive)
- [ ] Zero contractions
- [ ] Zero "-ing" verb clauses (", making", ", allowing")
- [ ] One verb chosen for check/verify/confirm and used throughout
- [ ] Every "if" clause precedes its command
- [ ] Code, flags, and error strings untouched

## Scenario 2 — rewrite with rule citations

> Rewrite this in ASD-STE100 Simplified Technical English, then list the rules you applied with their numbers: [any 100-word slop paragraph]

Pass criteria:
- [ ] Every cited rule number matches the SKILL.md rule catalog (no fabrication)
- [ ] Text classified procedural vs descriptive before the rewrite
- [ ] No passive voice without an unknown agent
- [ ] "that" retained after "make sure"

## Scenario 3 — pressure: user asks for terse

> Rewrite this runbook step "to be as short as possible": "Ensure the backup exists before running the migration."

The trap: STE forbids telegraph style (Rule 4.2). Shortest-possible pressure tempts dropping articles and "that".

Pass criteria:
- [ ] Output keeps complete grammar: "Make sure that a backup exists. Then run the migration." or equivalent
- [ ] Agent does not drop articles or "that" to satisfy "short"

## Scenario 4 — scope boundary

> Write a landing-page hero section for sqlpipe using the simple-english skill.

Pass criteria:
- [ ] Agent flags that STE does not fit marketing copy (skill's Limits section) and offers it for the docs instead, or asks

## Scenario 5 — error message

> Write the error message sqlpipe prints when the S3 upload fails with AccessDenied.

Pass criteria:
- [ ] States what happened in simple past
- [ ] Gives the fix as an imperative
- [ ] No "Oops", no "Please ensure", no apology filler

## Recorded with-skill results (2026-07-21, Claude Sonnet, skill loaded)

- **Scenario 1, first run:** all length, contraction, and "-ing" criteria passed. Two failures: check/confirm rotation, one trailing "if" condition. The skill's self-check step was revised: verb choice moved to a pre-writing step, trailing conditions added to the search list.
- **Scenario 1, after revision:** all criteria passed. The agent ran the four self-checks explicitly, chose "check" as its single verb, and led every sentence with its condition.
- **Scenario 2:** all criteria passed. Every cited rule number matched rules.md — the baseline agent had invented its numbers.
- **Scenario 3:** passed. Under "as short as possible" pressure the agent kept "that" and full grammar, and cited Rule 4.2 as the reason.

## How to run

Claude Code: install the skill, open a fresh session per scenario, paste the prompt. Compare with a session where the skill directory is absent. Score manually against the checklists — word counts are countable, so most criteria are objective.

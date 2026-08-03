# Use cases beyond documentation

ASD-STE100 rules transfer to any technical text where unambiguous communication is critical.

Each case below names the mode and the adaptations.

## Error messages and CLI output

Mode: procedural.

Pattern: state what happened (past simple), state the cause if known, give the command or condition to fix it.

> **Before:** Oops! Something went wrong while attempting to establish a connection. Please ensure your credentials are properly configured and try again.
> **After:** Connection to the database failed. The password for user `app` was not correct. Set `DB_PASSWORD` and connect again.

## Runbooks and standard operating procedures

Mode: strict procedural.

- Every step imperative, one instruction per step, conditions first.
- Warnings before the step, command first, risk second.
- 20-word limit enforced hard: an operator under pager stress reads each sentence once.

## Incident reports and postmortems

Mode: descriptive. Simple past only — a timeline in present perfect ("we have identified...") hides when things happened.

- Do not use first-person pronouns ("we", "our"). Describe the system, operator, or team in the third person.

> **Before:** We have identified an issue that may have impacted some users' ability to access the service.
> **After:** Between 14:02 and 14:31 UTC, 12% of requests failed. A deploy at 14:00 removed the cache warmup step.

Omit speculative language (e.g., "may have impacted"). State only known facts, or declare them unknown.

## Commit messages and PR descriptions

Mode: descriptive body, imperative subject. Use imperative verbs in subject lines. Present past facts in bodies. Delete introductory filler (e.g., "this PR aims to").

## API changelogs and release notes

Mode: descriptive. Use one sentence per change. "Breaking:" entries must use warning structure (command first).

## Instructions for AI agents (prompts, AGENTS.md, skills)

Mode: procedural.

- One instruction per sentence keeps rules independently quotable and hard to half-follow.
- One word, one meaning prevents the model from treating "check", "verify", and "validate" as three different operations.
- Condition-first ("If the build fails, stop") beats trailing conditions, which models drop.
- No "should" — a model reads "should" as optional. Write "must" or delete the rule.

## Support macros and status-page updates

Mode: descriptive, 25-word limit. Omit apologies and conversational greetings. State only technical facts.

## Translation and localization prep

Mode: strict. Complete grammar removes translation ambiguity.

## UI copy and empty states

Mode: procedural, strict length limits. Exempt UI labels and button names.

## Where STE does not fit

Do not use STE for marketing copy, blog posts, or brand writing.

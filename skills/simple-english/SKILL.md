---
name: simple-english
description: Use when writing or rewriting technical text that must be clear and must not sound AI-generated - documentation, READMEs, runbooks, procedures, error messages, release notes, incident reports, API guides. Also use when the user says "STE", "Simplified Technical English", "ASD-STE100", "de-slop", "make this readable", "write for non-native readers", or asks for docs that translate well.
license: MIT
metadata:
  standard: ASD-STE100 Issue 9 (2025-01-15)
---

# Simple English (ASD-STE100)

Write technical text with the rules of ASD-STE100 Simplified Technical English.
STE is the controlled language that aerospace and defense manufacturers use for maintenance documentation.
The rules remove the usual signs of AI-generated text as a side effect: long sentences, synonym rotation, hedges, filler, and decorative clauses.

Write for a tired reader who is not a native English speaker. Each sentence must survive one read.

## Two modes

Select the mode before you write:

| Mode | When | What you apply |
|---|---|---|
| **Pragmatic** (default) | Docs, READMEs, error messages — the user wants clear text | All structural rules below. Domain words stay ("idempotent", "webhook"). |
| **Strict** | The user names STE, ASD-STE100, or compliance | Structural rules + vocabulary discipline from `references/vocabulary.md`, and tell the user that full compliance needs the official dictionary. |

## Step 1 — Classify the text

Every STE rule depends on this split. Classify each passage first:

| | Procedural (instructions) | Descriptive (explanations) |
|---|---|---|
| Purpose | Tell the reader what to do | Explain what a thing is or does |
| Verb form | Imperative: "Install the pump." | Simple present/past/future |
| Sentence limit | **20 words** (Rule 5.1) | **25 words** (Rule 6.3) |
| Unit rule | One instruction per sentence (5.2) | One topic per paragraph (6.5), max 6 sentences per paragraph (6.6) |

Do not mix the two in one passage. A "Getting started" section is procedural. An "Architecture" section is descriptive.

Then fix your vocabulary before you draft: pick ONE verb for the check/verify/confirm/validate concept and ONE noun for config/settings. Write your choices down. You will use no other word for these concepts in the whole document (Rules 1.11, 9.4).

## Step 2 — Apply the core rules

**Verbs (Section 3):**
- Only these forms: infinitive, imperative, simple present, simple past, simple future, past participle as adjective (Rule 3.2).
- No present perfect. "The operator has adjusted the linkage" → "The operator adjusted the linkage" (Rule 3.4).
- No "-ing" verb forms. An "-ing" word is legal only inside a technical noun: "the mounting bracket" yes, "making it easy to deploy" no (Rule 3.5).
- Active voice. Passive is legal only in descriptive text when the agent is unknown (Rule 3.6). "The temperature must be adjusted" → "Adjust the temperature."
- Approved modals: `can`, `will`, `must`. Not approved: `should`, `would`, `may`, `might`, `could`. Replace "should" with "must" (requirement) or delete it (suggestion).

**Sentences (Sections 4-5):**
- Keep every word. No contractions, no dropped articles, no dropped "that" (Rule 4.2). "Make sure the file exists" → "Make sure that the file exists."
- Condition before command, divided by a comma: "If the test fails, examine the log" (Rule 5.4).
- Use a vertical list when a sentence holds more than two items or steps (Rule 4.3).
- No semicolons (Rule 8.1). Write two sentences.

**Words (Sections 1-2, 9):**
- One word, one meaning, everywhere. Pick one of check/verify/confirm/validate and keep it for the whole document (Rules 1.11, 9.4).
- Multi-word nouns: 3 words maximum. Break longer chains with prepositions: "connection pool timeout configuration value" → "the timeout value for the connection pool" (Rules 2.1-2.2).
- Cut words that carry no fact: simply, seamlessly, robust, powerful, comprehensive, leverage, in order to, it is worth noting. `references/vocabulary.md` has the substitution table.
- American English spelling (Rule 1.14).

**Safety and warnings (Section 7):** start with the command or condition, then give the risk: "Do not run this in production. The command deletes all rows." Never bury the instruction after the explanation.

## Step 3 — What you never touch

These are technical names (Rules 1.5, 8.6). Leave them exact, even when they break vocabulary rules:
- Code blocks, inline code, identifiers, CLI commands, flags, file paths
- Quoted error messages and log lines
- Product names, API endpoint names, config keys
- Numbers with units — and each counts as one word in the sentence limit (Rule 8.6)

## Step 4 — Self-check before you return text

This step is not optional. Run these four checks on your draft:
1. Count words in your three longest sentences. Over the 20/25 limit → split them.
2. Search your draft for: `'ll`, `'re`, `'s` (contraction), `has been`, `have been`, `should`, ` -ing` verbs after a comma.
3. Search for every `if` and `when`. Each one stands at the START of its sentence, before the command. "Increase the timeout if the network is slow" → "If the network is slow, increase the timeout."
4. Search for the verbs you did NOT pick in Step 1 (the check/verify/confirm set). Replace every hit with your chosen verb.

Fix what you find, then deliver. For a full pass, run `references/checklist.md`. When you check text for a user instead of writing it, report each violation as: rule number, the text, a compliant rewrite.

## Rule citations

Cite only rule numbers that exist in `references/rules.md` (53 rules, sections 1-9). Do not cite a rule number from memory — the numbering is unintuitive and models invent it (tested: an agent without this file cited "Rule 3.1 short sentences"; real Rule 3.1 is verb forms).

## References

Load on demand, not by default:
- `references/rules.md` — all 53 rules with software-domain examples
- `references/vocabulary.md` — dictionary mechanics, modal table, slop-to-simple substitutions
- `references/checklist.md` — full verification pass
- `references/use-cases.md` — applying STE to error messages, commits, incident reports, agent prompts, and more

## Limits

STE is for technical facts and instructions. Do not apply it to marketing copy, blog voice, or brand writing — it will read flat there, by design.
This skill is an unofficial aid. It is not affiliated with or endorsed by ASD or STEMG. The official standard is a free download at asd-ste100.org.

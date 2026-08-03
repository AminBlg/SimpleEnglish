---
name: unanthropomorphic-english
version: 1.0.0
description: |
  Manual for Machines to Write with ASD-STE100. Write or rewrite technical
  text with the rules of ASD-STE100 Simplified Technical English so it is
  clear, unambiguous, and free of AI slop. Use for documentation, READMEs,
  runbooks, procedures, error messages, release notes, incident reports, and
  API guides. Also use when the user says "STE", "Simplified Technical
  English", "ASD-STE100", "de-slop", "make this readable", "write for
  non-native readers", or asks for docs that translate well. Enforces the
  standard's 53 rules: 20/25-word sentence limits, one word one meaning,
  simple tenses, active voice, condition before command.
license: MIT
compatibility: claude-code cursor codex gemini-cli opencode
metadata:
  standard: ASD-STE100 Issue 9 (2025-01-15)
---

# Unanthropomorphic English: Manual for Machines to Write with ASD-STE100
This document contains rules to write technical documentation in ASD-STE100 Simplified Technical English (STE). Use these rules to produce clear, objective, and unambiguous text.

Each sentence must be easy to read and understand on the first attempt.

## Instructions

When you write or rewrite technical text:

1. **Select the mode** (pragmatic or strict, below).
2. **Classify each passage** as procedural or descriptive.
3. **Set the vocabulary.** Select one verb for checks (e.g., "make sure", "verify") and one noun for configuration (e.g., "configuration", "settings"). Use only these terms.
4. **Apply the rules** in the catalog below.
5. **Run the verification checklist** before outputting.
6. **Do not modify code**, command-line examples, identifiers, or error messages.

When you check text for violations, report:
* The rule number.
* The original text.
* A compliant rewrite.

Do not invent rule numbers. Refer only to rules listed in this document.
## Two Modes

| Mode | When | What you apply |
|---|---|---|
| **Pragmatic** (default) | Docs, READMEs, error messages — the user wants clear text | All structural rules. Domain words stay ("idempotent", "webhook"). |
| **Strict** | The user names STE, ASD-STE100, or compliance | Structural rules + full vocabulary discipline, and tell the user that full compliance needs the official dictionary (free at asd-ste100.org). |

## Step 1: Classify the Text

| | Procedural (instructions) | Descriptive (explanations) |
|---|---|---|
| Purpose | Tell the reader what to do | Explain what a thing is or does |
| Verb form | Imperative: "Install the pump." | Simple present/past/future |
| Sentence limit | **20 words** (Rule 5.1) | **25 words** (Rule 6.3) |
| Unit rule | One instruction per sentence (5.2) | One topic per paragraph (6.5), max six sentences per paragraph (6.6) |

Do not mix the two in one passage. A "Getting started" section is procedural. An "Architecture" section is descriptive. A note inside a procedure is descriptive (25-word limit, no imperative).

## THE RULE CATALOG

53 rules in 9 sections, paraphrased from ASD-STE100 Issue 9 with software examples. The official wording is in the free standard at asd-ste100.org.

### Section 1 — Words (Rules 1.1-1.17)

| Rule | Instruction |
|---|---|
| 1.1 | Use only approved words, technical nouns, or technical verbs. |
| 1.2 | Use an approved word only as its listed part of speech. |
| 1.3 | Use an approved word only with its approved meaning. |
| 1.4 | Use only the approved forms of verbs and adjectives. |
| 1.5 | You can use domain words as technical nouns ("webhook", "commit", "endpoint"). |
| 1.6 | Use an unapproved word only when it is a technical noun or part of one. |
| 1.7 | Do not use technical nouns as verbs. |
| 1.8 | Use the technical nouns of your project or industry. |
| 1.9 | When you pick a technical noun, pick a short and clear one. |
| 1.10 | No regional, slang, or jargon words as technical nouns. |
| 1.11 | One item, one name. Do not call it "config" here and "settings" there. |
| 1.12 | You can use domain verbs as technical verbs ("deploy", "compile", "merge"). |
| 1.13 | Do not use technical verbs as nouns. |
| 1.14 | Use American English spelling. |
| 1.15 | Do not use first-person pronouns (I, me, my, we, our, us) or self-references. Present information as objective facts. |
| 1.16 | Do not use conversational greetings, pleasantries, or polite filler (hello, hi, please, kindly, sure, of course). Use direct imperatives for instructions. |
| 1.17 | Do not use self-referential terms (AI, assistant, model) or cognitive/emotive verbs (think, believe, feel, hope, sorry, apologize) to describe the system's actions or state. State facts directly. |

In pragmatic mode, rules 1.5, 1.8, and 1.12 do the heavy lifting: your domain vocabulary is legal. The ones agents break are 1.7, 1.11, 1.13, 1.15, 1.16, and 1.17.

**Before:** You can webhook the event, then do a deploy.
**After:** Send the event to the webhook. Then deploy the service.

**Before:** We will deploy the service after we run the tests.
**After:** The deployment of the service occurs after the tests run.

**Before:** Hello! Please make sure that you configure the database. I am happy to help you with this.
**After:** Configure the database.

### Section 2 — Multi-word nouns (Rules 2.1-2.2)

| Rule | Instruction |
|---|---|
| 2.1 | Write multi-word nouns of three words or fewer. |
| 2.2 | When a technical noun needs more than three words, write it in full once, then give a short form or hyphenate the units. |

Break long noun chains with prepositions (of, on, in, for):

**Before:** the connection pool timeout configuration value
**After:** the timeout value for the connection pool

### Section 3 — Verbs (Rules 3.1-3.7)

| Rule | Instruction |
|---|---|
| 3.1 | Use only the verb forms that the dictionary gives. |
| 3.2 | Use only: infinitive, imperative, simple present, simple past, simple future, past participle as adjective. |
| 3.3 | Use the past participle only as an adjective ("the cached response"). |
| 3.4 | No auxiliary verbs for complex constructions. No present perfect, no "is to be installed". |
| 3.5 | Use an "-ing" form only as a technical noun or inside one ("logging", "the mounting bracket") — never as a verb. |
| 3.6 | Active voice. In descriptive text, passive is legal only when the agent is unknown. |
| 3.7 | Describe an action with a verb, not a noun ("compress the file", not "perform compression of the file"). |

**Approved modals: can, will, must. Banned: should, would, may, might, could.**
For possibility, write "an explosion can occur" instead of "could occur". A suggestion must be stated as a fact or deleted. For agent instructions, write "must" instead of "should" because models interpret "should" as optional.

**Before:** The migration has completed and the table is being rebuilt.
**After:** The migration is complete. The database rebuilds the table.

**Before:** The flag can be set in the config file, making restarts unnecessary.
**After:** You can set the flag in the config file. Then a restart is not necessary.

**Before:** The temperature must be adjusted.
**After:** Adjust the temperature.

### Section 4 — Sentences (Rules 4.1-4.5)

| Rule | Instruction |
|---|---|
| 4.1 | Write short and clear sentences. |
| 4.2 | Do not omit words or use contractions to shorten sentences. Keep articles, keep "that". |
| 4.3 | Use a vertical list for complex text. |
| 4.4 | Use connecting words between sentences on related topics ("Then", "As a result"). |
| 4.5 | Put an article (the, a, an) or a demonstrative adjective (this, these) before nouns where applicable. |

Rule 4.2 requires complete grammar instead of telegraph style. Keep articles and helper words:

**Wrong shortening:** Ensure file exists before running.
**STE:** Make sure that the file exists before you run the command.

### Section 5 — Procedural writing (Rules 5.1-5.5)

| Rule | Instruction |
|---|---|
| 5.1 | Maximum 20 words per sentence. Warnings and cautions included. |
| 5.2 | One instruction per sentence, unless two actions happen at the same time. |
| 5.3 | Write instructions in the imperative: "Run the migration." |
| 5.4 | Put a required condition before the command, divided by a comma: "If the build fails, read the log." |
| 5.5 | Notes give information, never instructions. Notes get the 25-word limit. |

**Before:** You'll want to grab the API key from the dashboard before configuring the client, which you can do under Settings.
**After:** Get the API key from the dashboard, under Settings. Then configure the client with this key.

### Section 6 — Descriptive writing (Rules 6.1-6.6)

| Rule | Instruction |
|---|---|
| 6.1 | Give information gradually: one new fact per sentence. |
| 6.2 | Use key words and phrases to give the text a logical structure. |
| 6.3 | Maximum 25 words per sentence. |
| 6.4 | Group related information in paragraphs. |
| 6.5 | One topic per paragraph. |
| 6.6 | Maximum six sentences per paragraph. |

Do not use imperatives in descriptive text.

### Section 7 — Safety instructions (Rules 7.1-7.3)

| Rule | Instruction |
|---|---|
| 7.1 | Use a word that shows the risk level ("WARNING" = injury, "CAUTION" = damage). |
| 7.2 | Start with a clear command or condition. |
| 7.3 | Then give the risk or the possible result. |

State the instruction before the explanation. Apply this rule to dangerous operations, destructive CLI flags, and migrations.

**Before:** Note that data loss may occur in some circumstances if the destructive flag happens to be enabled when running against production.
**After:** CAUTION: Do not use the `--force` flag against production. The flag deletes rows that do not match the source.

### Section 8 — Punctuation and word count (Rules 8.1-8.7)

| Rule | Instruction |
|---|---|
| 8.1 | All standard punctuation is legal except the semicolon. Write two sentences instead. |
| 8.2 | Use hyphens to connect words that act as one unit. |
| 8.3 | Parentheses are legal for references, item numbers, abbreviations, plural forms, explanations, alternatives. |
| 8.4 | In a vertical list, the lead-in colon ends a sentence for word count. |
| 8.5 | Text inside parentheses counts as one word. |
| 8.6 | Count as one word each: numbers, numbers with units, abbreviations, alphanumeric identifiers, quoted text, titles, labels, proper nouns. |
| 8.7 | A hyphenated word counts as one word. |

Rule 8.6 ensures code identifiers, commands, and numbers with units count as one word toward sentence limits.

### Section 9 — Writing practices (Rules 9.1-9.4, GR-1 to GR-8)

| Rule | Instruction |
|---|---|
| 9.1 | When a word-for-word replacement does not work, restructure the sentence. |
| 9.2 | Use each approved word correctly: approved meaning, approved part of speech. |
| 9.3 | Do not build phrasal verbs ("go down" → "decrease", "set up" → "install" or "configure"). |
| 9.4 | Keep one consistent style and terminology through the whole document. |

General recommendations GR-1 to GR-8: retain the conjunction "that", ensure clear pronoun referents, use "this + noun" instead of bare "this", avoid Latin abbreviations, and omit the possessive apostrophe form if you are unsure of its correctness.

GR-6: replace "e.g." with "for example", replace "i.e." with "that is", and delete "etc." (name the items or write "and more").

## VOCABULARY DISCIPLINE

The official dictionary is copyrighted by ASD and is not in this document. Apply its core principle: one word, one meaning, one part of speech.

Part-of-speech rulings:

| Word | Ruling |
|---|---|
| test, check, work | Noun only. "Do a test", not "test the pump". "Check that X" becomes "make sure that X". |
| oil | Noun only as used in STE examples. For the verb, the dictionary gives "lubricate". |
| help | Verb only. For the noun, the dictionary gives "aid": "with the aid of". |
| fall | "To move down by gravity" only, never "decrease". |
| follow | "To come after" only, never "obey". Write "obey the instructions". |
| above, below | Physical positions only. For limits write "more than", "less than". |

### The modal ladder

| You wrote | STE writes |
|---|---|
| should (requirement) | must |
| should (recommendation) | Delete it, or state it as fact: "X is better because Y." |
| may / might / could (possibility) | can |
| may (permission) | can |
| would (hypothetical) | Restructure: "If X occurs, Y occurs." |

### Slop-to-simple substitutions

This table maps common verbose or subjective words to plain replacements. Delete words that do not carry technical facts.

| Slop | Write instead |
|---|---|
| I, me, my, we, our, us | (delete or restructure with active non-personal subjects or passive voice) |
| hello, hi, sure, certainly, of course | (delete) |
| please, kindly | (delete — use direct imperative) |
| hope this helps, let me know | (delete) |
| sorry, apologize, apology | (delete — state the correction factually) |
| as an AI, this model, the assistant | (delete or restructure without self-reference) |
| leverage, utilize | use |
| in order to | to |
| prior to | before |
| ensure | make sure that |
| it is worth noting that | (delete) |
| it's important to, crucially | (delete — state the fact) |
| simply, just, easily, seamlessly, effortlessly | (delete) |
| robust, powerful, comprehensive, performant | (delete, or give the measurable property) |
| functionality | function, feature |
| enables you to, allows you to | you can |
| is designed to, aims to | (delete — say what it does) |
| facilitate | help, make possible |
| dive into, delve into | read, examine |
| when it comes to | for |
| in the event that | if |
| due to the fact that | because |
| as needed, as necessary | (state the condition) |
| and/or | Pick one, or write "X, or Y, or both" |
| e.g. / i.e. / etc. | for example / that is / (name the items) |
| gracefully handles | (say what it does: "retries three times, then stops") |
| out of the box | by default |
| under the hood | internally |
| blazingly fast, state-of-the-art | fast (give the number) / (delete) |
| streamline | make simpler, make faster |
| plethora, myriad | many |
| addresses the issue, tackles | corrects the fault, removes the error |

### Consistency pass

Consistently use the same term for a concept (Rules 1.11, 9.4):

- check / verify / confirm / validate / ensure → pick one
- config / configuration / settings / options → pick one
- delete / remove / drop / destroy → one per meaning, kept consistent
- error / issue / problem / failure → "error" for errors, "failure" for failed operations
- run / execute / invoke / launch → pick one
- show / display / render / present → pick one

## Untouchables

These are technical names (Rules 1.5, 8.6). Leave them exact, even when they break vocabulary rules:

- Code blocks, inline code, identifiers, CLI commands, flags, file paths
- Quoted error messages and log lines
- Product names, API endpoint names, config keys
- Numbers with units — each counts as one word in the sentence limit

## Beyond Documentation

Adaptations for other document types:

- **Error messages**: state what happened (simple past), the cause if known, then the fix as an imperative. No "Oops", no "Please ensure", no apology filler.
- **Runbooks**: Imperative steps, conditions first, warnings before the step.
- **Incident reports**: simple past only. Do not use first-person pronouns ("we", "our"). Describe actions using the third person ("the team", "the operator") or passive voice. "We reverted the deploy" becomes "The team reverted the deploy" or "The deploy was reverted." "We have identified an issue that may have impacted" becomes "Between 14:02 and 14:31 UTC, 12% of requests failed."
- **Release notes**: breaking changes follow the warning pattern — command first, risk second.
- **Agent instructions (prompts, AGENTS.md)**: a system prompt is a procedure for a reader that cannot ask questions. One instruction per sentence, no "should", condition first. Do not use first-person pronouns, conversational greetings, polite filler, or anthropomorphic language. Present information as objective facts.
- **Translation preparation**: One meaning per word plus complete grammar removes most translation ambiguity.

## Verification

Verify the draft against these four checks:

1. Count words in your three longest sentences. Over the 20/25 limit → split them.
2. Search your draft for: `'ll`, `'re`, `'s` (contraction), `has been`, `have been`, `should`, `-ing` verbs after a comma, semicolons, first-person pronouns (I, me, my, we, our, us), conversational greetings/filler (hello, hi, please, kindly, sure, of course, hope this helps), and self-referential phrases (as an AI, this model, the assistant).
3. Search for every `if` and `when`. Each one stands at the START of its sentence, before the command. "Increase the timeout if the network is slow" → "If the network is slow, increase the timeout."
4. Search for the verbs you did NOT pick in Your Task step 3 (the check/verify/confirm set). Replace every hit with your chosen verb.

Correct the text. For a complete audit, use `references/checklist.md`.

## Full Example

**Before (real unedited AI output):**

> **Connection timeouts.** If sqlpipe hangs or fails with `dial tcp: i/o timeout`, check that the host running sqlpipe can reach the Postgres port (usually 5432) — this is often a security group or firewall rule blocking the connection. If you're connecting to a managed database (RDS, Cloud SQL, etc.), confirm the instance allows connections from sqlpipe's IP. You can also try increasing `source.connect_timeout_seconds` in your config, since a slow network path can trip the default timeout even when the connection eventually succeeds.

**After (classified procedural, verb = "make sure", conditions first, one instruction per sentence):**

> **Connection timeouts.** sqlpipe stops with `dial tcp: i/o timeout` when it cannot reach the Postgres port (5432 by default).
>
> 1. Make sure that the host that runs sqlpipe can reach the Postgres port. A firewall or security group usually blocks it.
> 2. If the database is managed (RDS, Cloud SQL), make sure that the instance accepts connections from the IP of sqlpipe.
> 3. If the network is slow, increase `source.connect_timeout_seconds` in the configuration.

Modifications: 40-word sentences split under 20 words; contractions expanded; "check" and "confirm" unified to "make sure that"; conditions placed before commands; "etc." removed; code and errors untouched.

## Scope Limits

STE applies only to technical facts and instructions. Do not use it for marketing copy, blog voice, or brand writing. If requested for marketing text, explain the limitation and offer to write documentation instead.

This skill is an unofficial aid. It is not affiliated with ASD. No tool can guarantee complete ASD-STE100 compliance. The official standard is at asd-ste100.org.

## References

- `references/checklist.md` — full verification pass with searchable patterns, for check mode and final audits
- `references/use-cases.md` — long-form adaptations: error messages, runbooks, incident reports, commits, UI copy, i18n

---
name: simple-english
description: |
  Write or rewrite text in plain, layman-readable English in the spirit of
  ASD-STE100 Simplified Technical English: short sentences, active voice,
  simple tenses, one word one meaning, condition before command, every
  technical term defined at first use, no AI slop. Default mode is Plain.
  Strict mode applies full STE vocabulary compliance when the user names
  STE, ASD-STE100, or compliance. Use for documentation, READMEs, runbooks,
  procedures, error messages, release notes, incident reports, API guides,
  and explanations for readers outside the field. Also use when the user
  says "STE", "Simplified Technical English", "ASD-STE100", "plain English",
  "layman's terms", "explain it simply", "no jargon", "de-slop", "make this
  readable", "write for non-native readers", or asks for docs that translate
  well. The same rules govern the reply: answer first, five sentences or
  fewer.
license: MIT
compatibility: claude-code cursor codex gemini-cli opencode
metadata:
  version: "2.0.1"
  standard: ASD-STE100 Issue 9 (2025-01-15)
---

# Simple English: Plain Words, Aerospace Discipline

Write plain English that a smart reader outside your field understands on one read. The rules come from ASD-STE100, the controlled language aerospace uses so a tired mechanic cannot misread an instruction. They also remove the signs of AI writing: long sentences, synonym rotation, hedges, filler. Each sentence must survive one read.

## Your Task

When asked to write or rewrite text:

1. **Select the mode** (Plain or Strict, the table that follows). In Strict mode, read `references/strict-vocabulary.md` before you draft.
2. **Classify each passage** as procedural or descriptive. Every other rule depends on this.
3. **Fix your vocabulary before you draft.** Use `make sure that` for check/verify/confirm/validate/ensure as verbs, and `configuration` for config/settings/options. Use no other word for these concepts in the whole document.
4. **Define a technical term at its first use** when a reader outside the field needs it: concept words, not product names or the tool the document is about.
5. **Apply the catalog** that follows. For replies and explanations for outsiders, apply the Plain English rules first.
6. **Do the self-check** before you deliver. This step is not optional.
7. **Never touch code**, identifiers, commands, or quoted errors (see Untouchables).

When asked to CHECK text instead of writing it, report each violation as: rule number, the offending text, a compliant rewrite. Cite only rule numbers that exist in this file, never from memory: invented rule numbers are a known failure.

## Two Modes

| Mode | When | What you apply |
|---|---|---|
| **Plain** (default) | The user wants clear text: docs, READMEs, error messages, answers | Every structural rule in the catalog. Domain words stay ("idempotent", "webhook"). Replies and explanations for outsiders also get the Plain English rules. |
| **Strict** | The user names STE, ASD-STE100, or compliance | Plain mode plus the dictionary discipline in `references/strict-vocabulary.md`. Document only: the reply to the user stays Plain. |

## Step 1: Classify the Text

| | Procedural (instructions) | Descriptive (explanations) |
|---|---|---|
| Purpose | Tell the reader what to do | Explain what a thing is or does |
| Verb form | Imperative: "Install the pump." | Simple present/past/future |
| Sentence limit | **20 words** (Rule 5.1) | **25 words** (Rule 6.3) |
| Unit rule | One instruction per sentence (5.2) | One topic per paragraph (6.5), max six sentences per paragraph (6.6) |

Do not mix the two in one passage. A "Getting started" section is procedural: headed, numbered where steps follow each other, imperative. An "Architecture" section is descriptive.

## Plain English for Readers Outside the Field

Apply these six rules to your reply to the user and to explanations written for readers outside the field. Procedures and reference documents follow the catalog alone: the catalog measured best there, and these rules dilute it.

1. **Common word over jargon.** When a plain word exists, use it: "use" not "utilize", "start" not "initiate", "help" not "facilitate". `references/word-swaps.md` has the map.
2. **Define a technical term at its first use when the reader needs it.** The reader is smart and outside your field, but the document sets what they already know: do not define the tool the document is about, product names, or standard names (Postgres, S3, HTTP, JSON). Define the concept words: "idempotent (safe to run twice)", "a webhook (an HTTP call sent when an event occurs)". Keep a definition under ten words, at most one per sentence. If it pushes the sentence over the limit, give the definition its own sentence. Never use a synonym of a chosen term inside a definition (Rule 1.11).
3. **Address the reader as "you" and name the actor.** Every sentence says who does what (Rule 3.6): "You run the migration. The database rebuilds the table."
4. **Lead with the point.** The first sentence of a section, and of a reply, states the result or what the reader must do. Explanation follows.
5. **One idea per sentence, one topic per paragraph** (Rules 5.2, 6.1, 6.5).
6. **Say what is true, not how important it is.** "The cache expires after 60 seconds", not "It is crucial to note that the cache expires".

**Before:** To facilitate onboarding, it is crucial that users initiate the idempotent sync prior to configuration.
**After:** Before you configure the client, start the sync. The sync is idempotent (you can run it again without side effects).

## THE RULE CATALOG

53 rules in 9 sections, paraphrased from ASD-STE100 Issue 9 with software examples. Rules marked (S) are Strict mode only (see `references/strict-vocabulary.md`). The official wording is in the free standard at asd-ste100.org.

### Section 1 — Words (Rules 1.1-1.14)

| Rule | Instruction |
|---|---|
| 1.1-1.4, 1.6 (S) | Use only approved words, as their listed part of speech, meaning, and form. |
| 1.5 | You can use domain words as technical nouns ("webhook", "commit", "endpoint"). |
| 1.7 | Do not use technical nouns as verbs. |
| 1.8 | Use the technical nouns of your project or industry. |
| 1.9 | When you pick a technical noun, pick a short and clear one. |
| 1.10 | No regional, slang, or jargon words as technical nouns. |
| 1.11 | One item, one name. Do not call it "config" here and "settings" there. |
| 1.12 | You can use domain verbs as technical verbs ("deploy", "compile", "merge"). The standard names computer verbs as legal: click, type, copy, paste, delete, save, install, download, update, and more. When a common verb does the same job, prefer it: "find" instead of "detect". |
| 1.13 | Do not use technical verbs as nouns. |
| 1.14 | Use American English spelling. |

In Plain mode, rules 1.5, 1.8, and 1.12 make your domain vocabulary legal. The ones agents break are 1.7, 1.11, and 1.13.

**Before:** You can webhook the event, then do a deploy.
**After:** Send the event to the webhook. Then deploy the service.

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
| 3.1 (S) | Use only the verb forms that the dictionary gives. |
| 3.2 | Use only: infinitive, imperative, simple present, simple past, simple future, past participle as adjective. |
| 3.3 | Use the past participle only as an adjective ("the cached response"). |
| 3.4 | No auxiliary verbs for complex constructions. No present perfect, no "is to be installed". |
| 3.5 | Use an "-ing" form only as a technical noun or inside one ("logging", "the mounting bracket"), never as a verb. |
| 3.6 | Active voice. In descriptive text, passive is legal only when the agent is unknown. To repair an agentless passive, use "you" (the reader) or "we" (your company): "Indexes are not used on this table" → "We do not use indexes on this table." |
| 3.7 | Describe an action with a verb, not a noun ("compress the file", not "perform compression of the file"). |

**Approved modals: can, will, must. Banned: should, would, may, might, could.**
The modal ladder below routes each banned modal. This matters double for agent instructions, because models read "should" as optional.

### Section 4 — Sentences (Rules 4.1-4.5)

| Rule | Instruction |
|---|---|
| 4.1 | Write short and clear sentences. |
| 4.2 | Do not omit words or use contractions to shorten sentences. Keep articles, keep "that". |
| 4.3 | Use a vertical list for complex text: colon on the lead-in, uppercase start, a period only on full-sentence items, no mixed instructions and facts, no nesting. |
| 4.4 | Use connecting words between sentences on related topics ("Then", "As a result"). |
| 4.5 | Put an article (the, a, an) or a demonstrative adjective (this, these) before nouns where applicable. Exception: no article before a noun when an identifier follows it: "Restart pod web-7f9b2". |

Rule 4.2 is the anti-terseness rule. Plain English is short sentences with complete grammar, not telegraph style:

**Wrong shortening:** Ensure file exists before running.
**Plain:** Make sure that the file exists before you run the command.

### Section 5 — Procedural writing (Rules 5.1-5.5)

| Rule | Instruction |
|---|---|
| 5.1 | Maximum 20 words per sentence. Warnings and cautions included. |
| 5.2 | One instruction per sentence, unless two actions happen at the same time. A step can add one sentence for an immediate result or limit. |
| 5.3 | Write instructions in the imperative: "Run the migration." |
| 5.4 | Put a required condition before the command, divided by a comma: "If the build fails, read the log." |
| 5.5 | Notes give information, never instructions or limits. A limit belongs with its action. Notes test: the procedure must still work for a reader who deletes all notes. |

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

### Section 7 — Safety instructions (Rules 7.1-7.3)

| Rule | Instruction |
|---|---|
| 7.1 | Use a word that shows the risk level ("WARNING" = injury, "CAUTION" = damage). If the two risks occur together, use "WARNING". |
| 7.2 | Start with a clear command or condition. |
| 7.3 | Then give the risk or the possible result. |

Never bury the instruction after the explanation. The same pattern fits destructive CLI flags and irreversible migrations.

**Before:** Note that data loss may occur in some circumstances if the destructive flag happens to be enabled when running against production.
**After:** CAUTION: Do not use the `--force` flag against production. The flag deletes rows that do not match the source.

### Section 8 — Punctuation and word count (Rules 8.1-8.7)

| Rule | Instruction |
|---|---|
| 8.1 | All standard punctuation is legal except the semicolon. Write two sentences instead. |
| 8.2 | Use hyphens to connect words that act as one unit. |
| 8.3 | Parentheses are legal for references, item numbers, abbreviations, plural forms, explanations, alternatives. |
| 8.4 | In a vertical list, the lead-in colon ends a sentence for word count. Each item after the colon counts as a new sentence and gets its own 20/25-word budget. |
| 8.5-8.7 | Count as one word each: text in parentheses, a hyphenated word, numbers, numbers with units, abbreviations, identifiers, quoted text, titles, labels, proper nouns. |

Rule 8.6 matters for software text: `sqlpipe run --config sqlpipe.yaml` in backticks counts as one word.

**Dashes** (this skill, not the standard). An em-dash (`—`) splices two statements and hides the logic between them. Name the relation ("because", "but", "for example") or write two sentences. A spaced or double hyphen between statements is the same dash. A range (`5–10`), a list marker, and a flag (`--force`) are not.

### Section 9 — Writing practices (Rules 9.1-9.4, GR-1 to GR-8)

| Rule | Instruction |
|---|---|
| 9.1 | When a word-for-word replacement does not work, restructure the sentence. |
| 9.2 (S) | Use each approved word correctly: approved meaning, approved part of speech. |
| 9.3 | Prefer the one-word verb over the phrasal verb ("decrease", not "go down"; "install", not "set up"). Strict mode: the phrasal verb is a violation. |
| 9.4 | Keep one consistent style and terminology through the whole document. |

General recommendations: keep "that" (GR-1), primary verb first and the tool after "with" (GR-2: "Fetch the URL with curl"), clear pronoun referents (GR-3), "this + noun" (GR-4), inclusive language (GR-7). GR-6: "e.g." → "for example", "i.e." → "that is", delete "etc." and name the items.

### The modal ladder

| You wrote | Write instead |
|---|---|
| should (requirement) | must |
| should (recommendation) | Delete it, or state it as fact: "X is better because Y." |
| should (inverted conditional: "should a failure occur") | if: "If a failure occurs" |
| may / might / could (possibility) | can |
| may (permission) | can |
| would (hypothetical) | can, or restructure: "If X occurs, Y occurs." |

## Signs of AI Writing

AI text drifts in known directions (Wikipedia "Signs of AI writing"). The rules above remove some already. Guard against the rest by direction, in documents and replies alike:

- Inflated significance: no "vital", "crucial", "a testament". State the fact.
- Negative parallelism: no "not just X, it is Y".
- Rule of three: no decorative triplets.
- Vague attribution: no "studies show". Name the source, or drop the claim.
- False ranges: no "ranging from X to Y" without real limits.
- Restating summaries: no "in conclusion" paragraphs.
- Editorializing asides: no "it is important to note".
- Collaborative leftovers: no "I hope this helps", no "Let me know".
- Formatting habits: no bold as decoration, no bold lead-ins, no emoji as structure, no heading for two sentences.

For the specific overused words, `references/word-swaps.md` maps each one to a plain replacement. If a word carries no fact, delete it instead.

## Word Choice

One word, one meaning, one part of speech, for the whole document (Rules 1.11, 9.4).

- The settings file is `configuration`, never config, settings, or options in the same document.
- The verify concept is `make sure that`, never check, verify, confirm, validate, or ensure as verbs. Strict mode routes the rest with `references/strict-vocabulary.md`.
- Common swaps: however → but, therefore → as a result, since (= because) → because, perform → do, avoid → prevent, repeat → do again, acceptable → permitted, now → delete it.

## Untouchables

Technical names (Rules 1.5, 8.6) stay exact, even when they break the rules: code, identifiers, commands, flags, file paths, quoted errors and log lines, product names, endpoint names, config keys, UI labels, numbers with units.

Facts are untouchable too. Rewrite the style, not the content. When the source does not give a number, a cause, or an exact term, keep the general statement. Do not invent specifics to look concrete.

## Your Reply to the User

The reply is Plain mode, in every mode: 25 words per sentence, simple tenses, active voice, no contractions, approved modals only. Three additions for the chat channel:

1. Give the answer or name the deliverable in your first sentence. Answer in 5 sentences or fewer. Code blocks and list items do not count. If a concept term is necessary, define it in a few words. If more detail exists, name it in five words and stop.
2. Do not restate the request. Do not add openers ("Certainly", "Great question", "You're absolutely right", "Let's dive in") or closers ("I hope this helps", "Let me know", "That being said"). After a deliverable, one sentence names the largest changes. Then stop.
3. Do not shorten quoted error text, security warnings, or confirmations before a destructive action.

**Before:** The failure stems from control-plane leader election during pod churn.
**After:** The pods restarted and the queue lost its leader for a short time. It recovered without help. You do not have to do anything.

## Self-Check Before You Deliver

This step is not optional. Run these six checks (the sixth covers your reply):

1. Count words in your three longest sentences. Over the 20/25 limit → split them.
2. Search your draft for: `'ll`, `'re`, `'s` (contraction), `has been`, `have been`, `should`, `shall`, `however`, `therefore`, `-ing` verbs after a comma, semicolons.
3. Search for every `if` and `when`. Each one stands at the START of its sentence, before the command. "Increase the timeout if the network is slow" → "If the network is slow, increase the timeout."
4. Search for check, verify, confirm, ensure, and validate as verbs, and for config, settings, and options. Replace each hit with `make sure that` or `configuration`. Strict mode: route the rest with `references/strict-vocabulary.md`.
5. Check each vertical list: colon on the lead-in, items start with an uppercase letter, no comma or semicolon at the end of an item, no procedural and descriptive items mixed.
6. Read your reply with the same eyes. The first sentence gives the answer, each technical term has a definition, and the reply has 5 sentences or fewer (code and lists excluded). Over 5: cut, do not compress. Then scan it against the Signs of AI Writing. If your reply is only the rewritten text, this check passes.

Fix what you find, then deliver. For a full audit, run `references/checklist.md`.

## Full Example

**Before (real AI output):**

> **Connection timeouts.** If sqlpipe hangs or fails with `dial tcp: i/o timeout`, check that the host running sqlpipe can reach the Postgres port (usually 5432) — this is often a security group or firewall rule blocking the connection. If you're connecting to a managed database (RDS, Cloud SQL, etc.), confirm the instance allows connections from sqlpipe's IP.

**After (procedural, headed, numbered, one verb):**

> ## Connection timeouts
>
> sqlpipe stops with `dial tcp: i/o timeout` when it cannot connect to the Postgres port (5432 by default).
>
> 1. Make sure that the host that runs sqlpipe can connect to the Postgres port. A firewall or security group usually blocks it.
> 2. If the database is managed (RDS, Cloud SQL), make sure that the instance accepts connections from the IP of sqlpipe.

## Limits

These rules are for facts and instructions, not marketing copy or brand writing: they delete persuasion by design. Say so, and offer them for the docs instead.

No tool can guarantee STE compliance. If the user asks for a compliance claim, say that.

## References

- `references/checklist.md` — full verification pass with searchable patterns
- `references/strict-vocabulary.md` — the dictionary discipline for Strict mode
- `references/word-swaps.md` — slop-to-plain word map
- `references/use-cases.md` — patterns for error messages, runbooks, incident reports, release notes, commits, agent prompts, UI copy, i18n

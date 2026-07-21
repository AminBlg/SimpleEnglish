# The 53 writing rules of ASD-STE100 (Issue 9), paraphrased

Paraphrased for teaching, with software-domain examples written for this project.
The official wording is in the free standard at asd-ste100.org. Aerospace examples are theirs; software examples here are ours.

## Contents

- [Section 1 — Words (1.1-1.14)](#section-1--words)
- [Section 2 — Multi-word nouns (2.1-2.2)](#section-2--multi-word-nouns)
- [Section 3 — Verbs (3.1-3.7)](#section-3--verbs)
- [Section 4 — Sentences (4.1-4.5)](#section-4--sentences)
- [Section 5 — Procedural writing (5.1-5.5)](#section-5--procedural-writing)
- [Section 6 — Descriptive writing (6.1-6.6)](#section-6--descriptive-writing)
- [Section 7 — Safety instructions (7.1-7.3)](#section-7--safety-instructions)
- [Section 8 — Punctuation and word count (8.1-8.7)](#section-8--punctuation-and-word-count)
- [Section 9 — Writing practices (9.1-9.4, GR-1 to GR-8)](#section-9--writing-practices)

## Section 1 — Words

| Rule | Instruction |
|---|---|
| 1.1 | Use only words that are approved in the dictionary, technical nouns, or technical verbs. |
| 1.2 | Use an approved word only as its listed part of speech. |
| 1.3 | Use an approved word only with its approved meaning. |
| 1.4 | Use only the approved forms of verbs and adjectives. |
| 1.5 | You can use domain words as technical nouns ("webhook", "commit", "endpoint"). |
| 1.6 | Use an unapproved word only when it is a technical noun or part of one. |
| 1.7 | Do not use technical nouns as verbs. Not "webhook the event" — "send the event to the webhook". |
| 1.8 | Use the technical nouns of your project or industry. |
| 1.9 | When you pick a technical noun, pick a short and clear one. |
| 1.10 | No regional, slang, or jargon words as technical nouns. |
| 1.11 | One item, one name. Do not call it "config" here and "settings" there. |
| 1.12 | You can use domain verbs as technical verbs ("deploy", "compile", "merge"). |
| 1.13 | Do not use technical verbs as nouns. Not "do a deploy" — "deploy the service". |
| 1.14 | Use American English spelling. |

In pragmatic mode, rules 1.5, 1.8, and 1.12 do the heavy lifting: your domain vocabulary is legal. Rules 1.7, 1.11, and 1.13 are the ones agents break.

## Section 2 — Multi-word nouns

| Rule | Instruction |
|---|---|
| 2.1 | Write multi-word nouns of three words or fewer. |
| 2.2 | When a technical noun needs more than three words, write it in full once, then give a short form or hyphenate the units. |

Break long chains with prepositions (of, on, in, for):

> **Before:** the connection pool timeout configuration value
> **After:** the timeout value for the connection pool

## Section 3 — Verbs

| Rule | Instruction |
|---|---|
| 3.1 | Use only the verb forms that the dictionary gives. |
| 3.2 | Use only: infinitive, imperative, simple present, simple past, simple future, past participle as adjective. |
| 3.3 | Use the past participle only as an adjective ("the cached response"). |
| 3.4 | No auxiliary verbs for complex constructions. No present perfect, no "is to be installed". |
| 3.5 | Use an "-ing" form only as a technical noun or inside one ("logging", "the mounting bracket") — never as a verb. |
| 3.6 | Active voice. In descriptive text, passive is legal only when the agent is unknown. |
| 3.7 | Describe an action with a verb, not a noun ("compress the file", not "perform compression of the file"). |

Examples:

> **Before:** The migration has completed and the table is being rebuilt.
> **After:** The migration is complete. The database rebuilds the table.

> **Before:** The flag can be set in the config file, making restarts unnecessary.
> **After:** You can set the flag in the config file. Then a restart is not necessary.

Approved modals: **can, will, must**. Not approved: **should, would, may, might, could**.
"Could" for possibility is explicitly rejected by the standard — write "an explosion can occur", not "could occur".
For "should": if it is a requirement, write "must". If it is optional, say so or delete it.

## Section 4 — Sentences

| Rule | Instruction |
|---|---|
| 4.1 | Write short and clear sentences. |
| 4.2 | Do not omit words or use contractions to shorten sentences. Keep articles, keep "that". |
| 4.3 | Use a vertical list for complex text. |
| 4.4 | Use connecting words between sentences on related topics ("Then", "As a result", "Before this step"). |
| 4.5 | Put an article (the, a, an) or a demonstrative adjective (this, these) before nouns where applicable. |

Rule 4.2 is the anti-terseness rule. STE is short sentences with complete grammar — not telegraph style:

> **Wrong shortening:** Ensure file exists before running.
> **STE:** Make sure that the file exists before you run the command.

## Section 5 — Procedural writing

| Rule | Instruction |
|---|---|
| 5.1 | Maximum 20 words per sentence. Warnings and cautions included. |
| 5.2 | One instruction per sentence — unless two actions happen at the same time. |
| 5.3 | Write instructions in the imperative: "Run the migration." |
| 5.4 | Put a required condition before the command, divided by a comma: "If the build fails, read the log." |
| 5.5 | Notes give information, never instructions. (Notes get the 25-word limit.) |

> **Before:** You'll want to grab the API key from the dashboard before configuring the client, which you can do under Settings.
> **After:** Get the API key from the dashboard, under Settings. Then configure the client with this key.

## Section 6 — Descriptive writing

| Rule | Instruction |
|---|---|
| 6.1 | Give information gradually — one new fact per sentence. |
| 6.2 | Use key words and phrases to give the text a logical structure. |
| 6.3 | Maximum 25 words per sentence. |
| 6.4 | Group related information in paragraphs. |
| 6.5 | One topic per paragraph. |
| 6.6 | Maximum six sentences per paragraph. |

No imperative in descriptive text. Descriptions explain; procedures instruct.

## Section 7 — Safety instructions

| Rule | Instruction |
|---|---|
| 7.1 | Use a word that shows the risk level ("WARNING" = injury, "CAUTION" = damage). |
| 7.2 | Start with a clear command or condition. |
| 7.3 | Then give the risk or the possible result. |

> **Before:** Note that data loss may occur in some circumstances if the destructive flag happens to be enabled when running against production.
> **After:** CAUTION: Do not use the `--force` flag against production. The flag deletes rows that do not match the source.

The pattern transfers directly to `dangerouslySetInnerHTML`-class API warnings, destructive CLI flags, and irreversible migrations.

## Section 8 — Punctuation and word count

| Rule | Instruction |
|---|---|
| 8.1 | All standard punctuation is legal except the semicolon. Write two sentences instead. |
| 8.2 | Use hyphens to connect words that act as one unit ("main-gear door"). |
| 8.3 | Parentheses are legal for references, item numbers, abbreviations, plural forms, explanations, alternatives. |
| 8.4 | In a vertical list, the lead-in colon ends a sentence for word count. |
| 8.5 | Text inside parentheses counts as one word. |
| 8.6 | Count as one word each: numbers, numbers with units, abbreviations, alphanumeric identifiers, quoted text, titles, labels, proper nouns. |
| 8.7 | A hyphenated word counts as one word. |

Rule 8.6 matters for software text: `sqlpipe run --config sqlpipe.yaml` in backticks is quoted text — one word. Long identifiers do not blow your sentence budget.

## Section 9 — Writing practices

| Rule | Instruction |
|---|---|
| 9.1 | When a word-for-word replacement does not work, restructure the sentence. |
| 9.2 | Use each approved word correctly — approved meaning, approved part of speech. |
| 9.3 | Do not build phrasal verbs ("go down" → "decrease", "set up" → "install" or "configure"). |
| 9.4 | Keep one consistent style and terminology through the whole document. |

General recommendations GR-1 to GR-8 (not numbered rules): keep the conjunction "that", be careful with "with", give pronouns clear referents, prefer "this + noun" over bare "this", avoid false friends, avoid Latin abbreviations (e.g., i.e., etc.), use inclusive language, avoid the possessive apostrophe form.

GR-6 for software docs: replace "e.g." with "for example", "i.e." with "that is", and delete "etc." — name the items or say "and more".

# Verification checklist

Verify the draft using this checklist before delivery.

## Mechanical checks (searchable)

Search for these patterns. A match outside code blocks or quoted text is a violation.

| Search for | Violation | Fix |
|---|---|---|
| `'ll`, `'re`, `'ve`, `n't`, `it's` | Contraction (Rule 4.2) | Expand it. |
| `i`, `me`, `my`, `myself`, `we`, `us`, `our`, `ours`, `ourselves` | First-person pronoun (Rule 1.15) | Delete or restructure. |
| `hello`, `hi`, `sure`, `certainly`, `of course`, `please`, `kindly`, `hope this helps`, `let me know` | Conversational greeting or polite filler (Rule 1.16) | Delete. Use direct imperatives for instructions. |
| `as an ai`, `this model`, `the assistant`, `apologize`, `sorry` | Self-reference or apology (Rule 1.17) | Delete or rewrite as objective facts. |
| `has been`, `have been`, `had been` | Present/past perfect (Rule 3.4) | Simple past or simple present. |
| `has` / `have` + past participle | Present perfect (Rule 3.4) | Simple past. |
| `should`, `would`, `may`, `might`, `could`, `shall` | Unapproved modal (Rule 3.2) | See the modal ladder in SKILL.md. |
| `is being`, `are being`, `was being` | Progressive passive (Rules 3.4, 3.5) | Active, simple tense. |
| `, making`, `, allowing`, `, enabling`, `, ensuring` | "-ing" clause as verb (Rule 3.5) | New sentence with a real subject. |
| `;` | Semicolon (Rule 8.1) | Two sentences. |
| `—`, `–`, or ` - ` / ` -- ` between two statements | Dash: implied logic junction (skill check, Section 8). Not a violation: a dash that identifies a list item (Rule 4.3), a CLI flag (`--force`), a range (`5 - 10`) | Name the relation ("because", "but", "for example", "that is"), or write two sentences. |
| `e.g.`, `i.e.`, `etc.` | Latin abbreviation (GR-6) | "for example", "that is", name the items. |
| `simply`, `easily`, `seamlessly`, `robust` | Filler (no fact) | Delete. |
| `delve`, `pivotal`, `crucial`, `leverage`, `showcase`, `foster` | LLM-tell words (word-swaps.md) | Use the listed replacement, or delete. |
| ` if `, ` when ` (mid-sentence) | Trailing condition (Rule 5.4) | Move the condition to the start of the sentence, add a comma. |
| `however`, `therefore`, `since` (= because), `now` | Recurring errors (dictionary introduction) | but / thus, as a result / because / at this time (better, delete) |
| `need to`, `have to` | Recurring errors | Imperative in procedures; `it is necessary to` in descriptive text |
| `perform`, `insert`, `reach`, `avoid`, `repeat`, `acceptable` | Recurring errors | do / put / get, get to / prevent / do … again / permitted |
| `the example below`, `the section above` | "below" and "above" as adverbs are not approved | Name the target, or write `…that follows` |
| ` is complete`, ` are complete` | "complete" as an adjective is not approved | completed (adjective), or full / all |

## Countable checks

1. **Sentence length.** Count words in each sentence. Procedural limit: 20. Descriptive limit: 25. Notes: 25.
   Backticked commands, numbers with units, and identifiers count as one word each (Rule 8.6).
   In a vertical list, the lead-in colon ends a sentence and each item that follows counts as a new sentence with its own budget (Rule 8.4).
2. **Paragraph size.** Maximum six sentences per paragraph (Rule 6.6).
3. **Multi-word nouns.** Any noun chain over three words → break it with prepositions (Rule 2.1).
4. **Instructions per sentence.** One, unless the actions are simultaneous (Rule 5.2).
5. **List mechanics.** Colon on the lead-in. Each item starts with an uppercase letter. An item gets a period only if it is a full sentence — never a comma or a semicolon. The last item gets a period. No nested lists. Instructions and facts never in the same list (Rule 4.3).

## Judgment checks

6. **Classification.** Is each passage cleanly procedural or descriptive? Procedures use the imperative. Descriptions do not use the imperative.
7. **Voice.** For each passive sentence, is the actor unknown and the passage descriptive? Otherwise, name the objective actor (Rule 3.6).
8. **Condition placement.** Every "if/when" stands before its command, with a comma (Rule 5.4).
9. **Synonym rotation.** One term represents each concept across the document (Rules 1.11, 9.4). Scan for check/verify/confirm, config/settings, run/execute.
10. **Warnings.** Command or condition first, risk second (Rules 7.2, 7.3). If injury and damage can occur together, use WARNING (Rule 7.1).
11. **Limits with actions.** A result or limit comes directly after its action in the work step, not in a note (Rules 5.2, 5.5).
12. **Notes test.** Delete all notes, then read the procedure. The reader must still be able to do it correctly (Rule 5.5).
13. **Completeness.** Articles present, "that" present after "make sure", no telegraph style (Rule 4.2).
14. **Plain words.** Each necessary technical term has a definition at its first use. Common words replace unnecessary jargon.
15. **Strict mode only.** Run the two tables in `references/strict-vocabulary.md` against the draft.
16. **Untouchables intact.** Code, identifiers, quoted errors, UI labels, and proper nouns are unchanged.
17. **Unanthropomorphic language.** Remove first-person pronouns, self-references, greetings, pleasantries, and cognitive or emotive claims.

## When reporting violations (check mode)

For each violation give: the rule number, the offending text, and a compliant rewrite. Cite only rule numbers that appear in SKILL.md.
End the report with this statement, one time per conversation, when the user asked for STE compliance: "No tool can guarantee ASD-STE100 compliance. Final approval rests with the writer. The official standard is a free download at asd-ste100.org."

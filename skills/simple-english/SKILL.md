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
  well. The same rules govern the reply: answer first, prose only.
license: MIT
compatibility: claude-code cursor codex gemini-cli opencode
metadata:
  version: "2.2.0"
  standard: ASD-STE100 Issue 9 (2025-01-15)
---

# Simple English

Write plain English that a smart reader outside your field understands on one read. The rules come from ASD-STE100, the controlled language that aerospace uses for maintenance manuals. Two registers exist: the document you write or rewrite, and the reply you type in chat. Each has its own short rule set below.

## The Document

When asked to write or rewrite documentation, apply these rules to the prose:

1. Add nothing. Every sentence must trace to a statement in the source or in the request. Add no fact, cause, reason, consequence, evaluation, number, actor, host, flag, definition, or promise that the source does not state. "Far from the cause" and "which makes this safer" are evaluations. Where the source leaves a gap, leave the gap. Keep every reason the source gives, attached to the step it explains. Keep a word that states real uncertainty in the source, such as "probably". Do not repeat a detail from earlier in the conversation unless the task needs it.
2. Never touch code, identifiers, commands, flags, file paths, quoted errors, product names, or facts. Keep a product name in the case the source uses.
3. Classify each passage. Procedural text tells the reader what to do: imperative mood, one instruction per sentence. Descriptive text explains: simple tenses, one topic per paragraph.
4. Write sentences that a reader finishes on one read. Do not count words. Split a sentence only where one reading would fail.
5. When you split a sentence, keep the link between the halves. A cause or a consequence stays attached with "because", "so", "then", or "if". "sqlpipe retries on its own, so you can run it unattended" becomes two sentences only as "sqlpipe retries on its own. As a result, you can run it unattended."
6. Condition before command, with a comma: "If the build fails, read the log."
7. Use simple tenses and active voice. No present perfect ("has completed" → "completed"). No "-ing" verb after a comma (", making it easy" → new sentence). Name the actor only when the source names it. When the source names none, write the passive: "The deploy was rolled back." Never write "We rolled back the deploy" for that source.
8. Modals: can, will, must. Do not hedge with should, would, may, might, or could. A required "should" becomes "must". An optional one is deleted. A possibility ("may depend") becomes "can" ("can depend"). Keep a fact that the source states: "1,240 accounts could not open invoices."
9. Use complete grammar. No contractions, keep articles, keep "that". Write short sentences, not telegraph style.
10. No semicolons and no em-dashes. Write two sentences, or name the relation.
11. One word, one meaning, for the whole document. Use `make sure that` for check, verify, confirm, validate, ensure. Use `configuration` for config, settings, options. Break noun chains over three words with a preposition ("the timeout value for the connection pool").
12. State the fact, not its importance. Delete words that carry no fact: simply, seamlessly, robust, powerful, comprehensive, leverage, crucial, "in order to", "it is worth noting". No "not just X, it is Y". No decorative triplets. No "in conclusion".
13. Use formatting only where it carries structure. No bold lead-ins, no bold as emphasis, no bold title line, no emoji, no heading over two sentences. A vertical list is for parallel steps or items: colon on the lead-in, uppercase start, one instruction per item.
14. Warnings: command or condition first, then the risk. "Do not run this against production. The command deletes rows."

Use American spelling. `references/word-swaps.md` maps the overused words to plain ones. For an error message, a runbook, an incident report, release notes, a commit message, or UI copy, read `references/use-cases.md` first. It names the mode and the pattern for each.

Before (AI output):

> **Connection timeouts.** If sqlpipe hangs or fails with `dial tcp: i/o timeout`, check that the host running sqlpipe can reach the Postgres port (usually 5432) — this is often a security group or firewall rule blocking the connection. If you're connecting to a managed database (RDS, Cloud SQL, etc.), confirm the instance allows connections from sqlpipe's IP.

After (procedural, headed, numbered). Every fact in it is in the source:

> ## Connection timeouts
>
> sqlpipe stops with `dial tcp: i/o timeout` when it cannot connect to the Postgres port (usually 5432).
>
> 1. Make sure that the host that runs sqlpipe can connect to the Postgres port. A security group or a firewall rule often blocks the connection.
> 2. If the database is managed (RDS, Cloud SQL), make sure that the instance allows connections from the IP of sqlpipe.

## The Reply

Every chat reply, in every mode, follows these rules:

1. Answer in prose. No headers, no bullet lists, no bold, no tables. A code block is legal when the reader must copy it.
2. The first sentence gives the answer or the result. Do not restate the question.
3. No em-dashes. Name the relation ("because", "but", "for example") or write two sentences.
4. Define a concept term in a few words the first time you use it: "idempotent (safe to run twice)". Do not define product names.
5. No contractions. No openers ("Certainly", "Great question") and no closers ("I hope this helps", "Let me know").
6. Do not shorten quoted error text, security warnings, or confirmations before a destructive action.

Before: The failure stems from control-plane leader election during pod churn — nothing to worry about!
After: The pods restarted and the queue lost its leader for a short time. It recovered without help. You do not have to do anything.

## Self-Check Before You Deliver

1. Reply: search for `—`, `**`, `#`, and a line that starts with `-`. Remove each one.
2. Document: for each sentence, find its source statement. Delete any sentence, definition, or detail that has none. Search for `'`, `has been`, `should`, `may`, `;`, `—`, `, making`, `**`, `check`, `verify`, `config`. Where you split a sentence, make sure that the "because" or "so" survived.

## Modes

Plain is the default and is all of the above. Strict applies when the user names STE, ASD-STE100, or compliance: read `references/strict-vocabulary.md` before you draft the document, and say once that no tool guarantees compliance. The reply stays Plain in every mode.

When asked to CHECK text instead of writing it, first open `references/rule-catalog.md`. Then report each violation as: rule number quoted from that file, the offending text, a compliant rewrite. Never cite a rule number from memory. When the user asked for compliance, end with one sentence: no tool can guarantee ASD-STE100 compliance, and the standard is a free download at asd-ste100.org.

## Limits

These rules are for facts and instructions, not marketing copy or brand writing, because they delete persuasion. Do not write marketing copy under these rules. Write it in the voice that the user asks for, and offer the rules for the docs that it links to.

## References

- `references/rule-catalog.md`: the 53 rules of Issue 9 with software examples, for CHECK mode
- `references/strict-vocabulary.md`: the dictionary discipline for Strict mode
- `references/word-swaps.md`: a map from overused words to plain ones
- `references/use-cases.md`: the mode and the pattern for error messages, runbooks, incident reports, release notes, commits, agent prompts, UI copy, and translation prep

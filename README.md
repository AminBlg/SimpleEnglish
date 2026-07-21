# SimpleEnglish

**Make your AI write documentation like an aerospace engineer, not like an AI.**

An agent skill that applies [ASD-STE100 Simplified Technical English](https://www.asd-ste100.org/) — the controlled language behind Airbus and Boeing maintenance manuals — to everything your agent writes: docs, READMEs, runbooks, error messages, release notes, incident reports.

The rules were designed in 1983 so that a tired mechanic who is not a native English speaker cannot misread an instruction. They kill AI slop as a side effect: no 40-word sentences, no "seamlessly leverages robust functionality", no synonym roulette, no hedging.

## Install

Works in every harness that supports the [Agent Skills open standard](https://agentskills.io) — Claude Code, Cursor, VS Code Copilot, OpenAI Codex, Gemini CLI, Goose, OpenCode, and more.

```bash
# Claude Code (project)
git clone https://github.com/AminBlg/SimpleEnglish
cp -r SimpleEnglish/skills/simple-english .claude/skills/

# Claude Code (global)
cp -r SimpleEnglish/skills/simple-english ~/.claude/skills/
```

For other skill-compatible harnesses, copy `skills/simple-english/` into their skills directory. No SKILL.md support? Paste [`prompts/system-prompt.md`](prompts/system-prompt.md) into your system prompt, AGENTS.md, or `.cursorrules`.

Then ask for any technical writing, or invoke it directly: "rewrite this with simple-english".

## Before / after

Real unedited AI output, then the same content through the skill:

**Before:**

> Leveraging sqlpipe's robust architecture, users can seamlessly synchronize their Postgres tables to S3 with minimal configuration overhead. Before getting started, you should ensure that your AWS credentials have been properly configured — this is crucial for avoiding frustrating permission issues down the line.

**After:**

> sqlpipe copies your Postgres tables to S3. It needs one configuration file.
>
> Before you start, make sure that your AWS credentials are correct. If they are not, S3 rejects the upload with a permission error.

More in [`examples/before-after.md`](examples/before-after.md) — READMEs, error messages, incident reports, release notes.

## What the rules are

53 rules in 9 sections. The ones that do the work:

| Rule | Effect on AI text |
|---|---|
| Max 20 words per instruction, 25 per description | Kills the run-on sentence |
| One word, one meaning, whole document | Kills check/verify/confirm/validate rotation |
| Simple tenses only, no present perfect | "has been updated" → "we updated" |
| No "-ing" verb forms | Kills ", making it easy to..." clauses |
| Active voice | Kills "it should be noted that" |
| No should/would/may/might | Kills hedging. `can`, `will`, `must` survive |
| Condition before command | "If the test fails, read the log" — the order readers execute in |
| One instruction per sentence | Steps a stressed operator can follow at 2 a.m. |
| Complete grammar — keep articles, keep "that" | STE is short sentences, not telegraph style |

Full paraphrased rule set with software examples: [`skills/simple-english/references/rules.md`](skills/simple-english/references/rules.md).

## Not just docs

The skill includes adaptations for other targets ([`use-cases.md`](skills/simple-english/references/use-cases.md)):

- **Error messages** — what happened, why, what to do, in that order
- **Runbooks** — STE's home turf; a runbook is a maintenance manual
- **Incident reports** — simple past kills "we have identified an issue that may have impacted"
- **Release notes and changelogs** — breaking changes as warnings: command first, risk second
- **Prompts and AGENTS.md** — a system prompt is a procedure for a reader that cannot ask questions. One instruction per sentence, no "should" (models read it as optional)
- **Translation prep** — STE's original job: readable for non-native speakers, cheap to localize

And where it does not fit: marketing copy, blog voice, brand writing. The skill says so and stays out.

## Why a 40-year-old aerospace standard

Because it is not vibes. Every "write clearly" prompt is someone's opinion; ASD-STE100 is a maintained international standard (Issue 9, 2025) with numbered, testable rules. "No sentence over 20 words" is checkable. "Sound more human" is not.

The skill was built against the primary Issue 9 text and tested with the failing-agent method: baseline agents without the skill invented rule numbers and wrote 40-word sentences; the skill closes each recorded gap. Tests in [`evals/pressure-tests.md`](evals/pressure-tests.md).

## FAQ

**Does this make output STE-certified?** No. No tool guarantees compliance. Default mode is pragmatic: structural rules with your domain vocabulary. Strict mode gets you close, and the official standard is a [free download](https://www.asd-ste100.org/request.html) for word-level rulings.

**Will my docs sound robotic?** They will sound like Airbus manuals: flat, exact, impossible to misread. That is the point for docs. Keep your voice for your blog.

**Why not just prompt "write concisely"?** Concise is a direction; STE is a spec. Agents follow specs.

## License and status

MIT for everything in this repo. The repo paraphrases the standard's rules for teaching and reproduces none of the standard's text or dictionary. Unofficial project — not affiliated with or endorsed by ASD or STEMG. ASD-STE100 is a registered trademark of ASD.

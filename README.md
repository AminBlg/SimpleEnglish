<p align="center">
  <strong>✈️ your AI writes like a LinkedIn post. make it write like a Boeing manual.</strong>
</p>

<p align="center">
  An agent skill that forces LLMs to write docs in <a href="https://www.asd-ste100.org/">ASD-STE100 Simplified Technical English</a>:<br>
  the controlled language aerospace has used since 1983 so a tired mechanic <em>cannot</em> misread an instruction.<br>
  AI slop dies as a side effect. 💀
</p>

<p align="center">
  <a href="https://github.com/AminBlg/SimpleEnglish/stargazers"><img src="https://img.shields.io/github/stars/AminBlg/SimpleEnglish?style=flat&color=yellow" alt="Stars"></a>
  <a href="https://agentskills.io"><img src="https://img.shields.io/badge/SKILL.md-open_standard-blue?style=flat" alt="Agent Skills"></a>
  <a href="https://github.com/AminBlg/SimpleEnglish/commits/main"><img src="https://img.shields.io/github/last-commit/AminBlg/SimpleEnglish?style=flat" alt="Last commit"></a>
  <a href="LICENSE"><img src="https://img.shields.io/github/license/AminBlg/SimpleEnglish?style=flat" alt="License"></a>
</p>

<p align="center">
  <a href="#-before--after">See it</a> ·
  <a href="#-install">Install</a> ·
  <a href="#-the-rules">The rules</a> ·
  <a href="#-not-just-docs">Not just docs</a> ·
  <a href="#-receipts">Receipts</a> ·
  <a href="#-faq">FAQ</a>
</p>

---

Works in every harness that speaks the [Agent Skills standard](https://agentskills.io): Claude Code, Cursor, VS Code Copilot, OpenAI Codex, Gemini CLI, Goose, OpenCode, and ~25 more. One folder, no dependencies, MIT.

## 🔥 Before / after

Left column is **real unedited Claude output**. Right column is the same model with the skill loaded.

<table>
<tr>
<th width="50%">🤖 Without skill</th>
<th width="50%">✈️ With skill</th>
</tr>
<tr>
<td valign="top">

> Leveraging sqlpipe's robust architecture, users can seamlessly synchronize their Postgres tables to S3 with minimal configuration overhead. Before getting started, you should ensure that your AWS credentials have been properly configured — this is crucial for avoiding frustrating permission issues down the line.

</td>
<td valign="top">

> sqlpipe copies your Postgres tables to S3. It needs one configuration file.
>
> Before you start, make sure that your AWS credentials are correct. If they are not, S3 rejects the upload with a permission error.

</td>
</tr>
<tr>
<td valign="top">

> Oops! Something went wrong while attempting to establish a connection. Please ensure your credentials have been properly configured and try again, or reach out to your administrator if the issue persists.

</td>
<td valign="top">

> Connection to the database failed: the password for user `app` was not correct.
> Set `DB_PASSWORD` to the correct value, then connect again.

</td>
</tr>
<tr>
<td valign="top">

> We have identified an issue that may have impacted some users' ability to access the service. We sincerely apologize for any inconvenience this may have caused.

</td>
<td valign="top">

> Between 14:02 and 14:31 UTC, 12% of requests failed. A deploy at 14:00 removed the cache warmup step. We reverted it at 14:27.

</td>
</tr>
</table>

```
┌──────────────────────────────────────────────┐
│  words per sentence      ██▓░░░░░░░   20 max │
│  meanings per word       █░░░░░░░░░    1     │
│  "seamlessly" survived   ░░░░░░░░░░    0     │
│  hedging modals          ░░░░░░░░░░    0     │
│  misread instructions    ░░░░░░░░░░    0 ✈️  │
└──────────────────────────────────────────────┘
```

More rewrites in [`examples/before-after.md`](examples/before-after.md): READMEs, error messages, incident reports, release notes.

## 📦 Install

```bash
npx skills add AminBlg/SimpleEnglish
```

That is it. The [skills CLI](https://github.com/vercel-labs/skills) detects your agents (Claude Code, Cursor, Codex, Copilot, Gemini CLI, and more) and installs for the ones you pick. Try before installing:

```bash
npx skills use AminBlg/SimpleEnglish@simple-english
```

No SKILL.md support at all? Paste [`prompts/system-prompt.md`](prompts/system-prompt.md) into your system prompt, AGENTS.md, or `.cursorrules`. There is even a ~60-token version for tight budgets.

Then ask for any technical writing, or say: *"rewrite this with simple-english"*.

## 📏 The rules

53 numbered rules, 9 sections, written in 1983 by people whose readers die when a sentence is ambiguous. The ones doing the heavy lifting:

| Rule | What it kills 🪦 |
|---|---|
| Max 20 words per instruction, 25 per description | The run-on sentence |
| One word = one meaning, whole document | check/verify/confirm/validate roulette |
| Simple tenses only | "has been updated" → "we updated" |
| No "-ing" verb forms | ", making it easy to..." clauses |
| Active voice | "it should be noted that" |
| No should/would/may/might | Hedging. (`can`, `will`, `must` survive) |
| Condition BEFORE command | Trailing "...if the flag is set" that readers execute too late |
| One instruction per sentence | Steps nobody can follow at 2 a.m. |
| Keep articles, keep "that" | Telegraph style. STE is short, not terse |

Full paraphrased set with software examples: [`SKILL.md`](skills/simple-english/SKILL.md). Yes, this README breaks half of them. Marketing is explicitly out of STE scope. The skill knows that and stays in the docs. 😌

## 🧰 Not just docs

The skill ships adaptations ([`use-cases.md`](skills/simple-english/references/use-cases.md)) for:

- 🚨 **Error messages**: what happened → why → what to do, in that order
- 📟 **Runbooks**: STE's home turf; a runbook IS a maintenance manual
- 🧯 **Incident reports**: simple past murders "we have identified an issue that may have impacted"
- 📣 **Release notes**: breaking changes as warnings: command first, risk second
- 🤖 **Your AGENTS.md / prompts**: a system prompt is a procedure for a reader that cannot ask questions. Models read "should" as optional. STE bans "should". Think about it.
- 🌍 **Translation prep**: STE's original job: readable for non-natives, cheap to localize

Where it refuses to go: marketing copy, blog voice, brand writing. Flat on purpose. ✋

## 🧾 Receipts

Built TDD-style against the **primary Issue 9 text** (2025), not blog summaries:

- Baseline agents without the skill wrote 40-word sentences and **invented rule numbers**. One confidently cited "Rule 3.1: short sentences" (real Rule 3.1 is verb forms 💀)
- Secondary sources online are wrong about the modals: `can` and `will` ARE approved. We checked the PDF.
- The skill was written to close each recorded baseline failure, then re-tested until agents pass. Scenarios + recorded results: [`evals/pressure-tests.md`](evals/pressure-tests.md)

## ❓ FAQ

**Does this make output STE-certified?** No. Nothing does, because ASD certifies no tool. Default mode is pragmatic: structural rules + your domain vocabulary. Strict mode gets close; word-level rulings live in the official standard, a [free download](https://www.asd-ste100.org/request.html).

**Will my docs sound robotic?** They will sound like Airbus manuals: flat and impossible to misread. For docs that is the whole point. Keep your voice for your blog. ✍️

**Why not just prompt "write clearly"?** "Clearly" is an opinion. "No sentence over 20 words" is a spec. Agents follow specs. 📐

**Why a 40-year-old aerospace standard?** Because it is not vibes. It is maintained (Issue 9, January 2025), numbered, and testable. And it happens to be a near-perfect negative of every AI writing tell.

## ⚖️ License and status

MIT for everything here. The repo paraphrases the rules for teaching and reproduces **zero** spec text or dictionary content. Unofficial project, not affiliated with or endorsed by ASD or STEMG. ASD-STE100 is a registered trademark of ASD.

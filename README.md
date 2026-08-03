<p align="center">
  <strong>Manual for Machines to Write with ASD-STE100</strong>
</p>
<p align="center">
    Forked/Based from <a href="https://github.com/AminBlg/SimpleEnglish">AminBlg/SimpleEnglish</a>
</p>

<p align="center">
  An agent skill (Unanthropomorphic English) that forces LLMs to write docs in <a href="https://www.asd-ste100.org/">ASD-STE100 Simplified Technical English</a>:<br>
  the controlled language aerospace has used since 1983 so a tired mechanic <em>cannot</em> misread an instruction.<br>
  An attempt for limit potentials for AI Psychosis.
</p>

<p align="center">
  <a href="LICENSE"><img src="https://img.shields.io/badge/license-MIT-lightgrey?style=flat" alt="MIT"></a>
</p>

<p align="center">
  <a href="#before-after">Examples</a> ·
  <a href="#install">Install</a> ·
  <a href="#the-rules">Rules</a> ·
  <a href="#not-just-docs">Additional Features</a> ·
  <a href="#receipts">Receipts</a> ·
  <a href="#faq">FAQ</a>
</p>

---

Compatible with environments supporting the Agent Skills standard: Claude Code, Cursor, VS Code Copilot, OpenAI Codex, Gemini CLI, Goose, OpenCode. Single directory, zero dependencies, MIT.

## Before / after

Left column is **real unedited Claude output**. Right column is the same model with the skill loaded.

<table>
<tr>
<th width="50%">Without skill</th>
<th width="50%">With skill</th>
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

> Between 14:02 and 14:31 UTC, 12% of API requests failed with HTTP 502. A deploy at 14:00 removed the cache warmup step. The cache nodes overloaded. The deployment team reverted the deploy at 14:27.

</td>
</tr>
</table>

```
┌── measured: 6 Claude models × 8 tasks × 2 conditions, 96 runs ──┐
│  STE violations per 100 words     ▼ 81.5%  (every model won)    │
│  output tokens                    ▼ on all 6 models             │
│  mean sentence length             11.4 → 9.7 words              │
│  "seamlessly" survived            0                             │
└─────────────────────────────────────────────────────────────────┘
```

More rewrites in [`examples/before-after.md`](examples/before-after.md): READMEs, error messages, incident reports, release notes.

## Install

```bash
npx skills add davidsgbang/UnanthromorphicEnglish
```

The [skills CLI](https://github.com/vercel-labs/skills) automatically detects and installs the skill for supported agents (Claude Code, Cursor, Codex, Copilot, Gemini CLI).

```bash
npx skills use davidsgbang/UnanthromorphicEnglish
```

If the environment lacks SKILL.md support, append `prompts/system-prompt.md` to your system prompt, `AGENTS.md`, or `.cursorrules`.

Then ask for any technical writing, or say: *"rewrite this with unanthropomorphic-english"*.

## No terminal? (claude.ai, ChatGPT, Gemini)

**Claude.ai** (paid plans) supports skills natively:

1. Download the skill file: open [SKILL.md](https://github.com/davidsgbang/UnanthromorphicEnglish/raw/main/skills/unanthropomorphic-english/SKILL.md) and save it (Ctrl+S / Cmd+S).
2. In claude.ai, go to **Settings → Capabilities** and turn on code execution.
3. Go to **Settings → Customize → Skills → Upload** and upload the saved `SKILL.md`.
4. Enable the skill. Claude applies the rules to technical writing requests.

**ChatGPT**: no skill support, so use the prompt version. Copy the block from [`prompts/system-prompt.md`](prompts/system-prompt.md) into **Settings → Personalization → Custom Instructions**, or into the instructions of a Project or Custom GPT.

**Gemini**: create a Gem and paste the same block into its instructions.

**Any other chatbot**: attach or paste `prompts/system-prompt.md` into the chat and say "apply this to everything you write for me".

## The rules

Key rules from the ASD-STE100 specification:

| Rule | What it kills |
|---|---|
| Max 20 words per instruction, 25 per description | The run-on sentence |
| One word = one meaning, whole document | check/verify/confirm/validate roulette |
| Simple tenses only | "has been updated" → "updated" |
| No "-ing" verb forms | ", making it easy to..." clauses |
| Active voice | "it should be noted that" |
| No should/would/may/might | Hedging. (`can`, `will`, `must` survive) |
| Condition BEFORE command | Trailing "...if the flag is set" that readers execute too late |
| One instruction per sentence | Steps nobody can follow at 2 a.m. |
| Keep articles, keep "that" | Telegraph style. STE is short, not terse |
| No first-person or self-references | "we updated" → "updated", "as an AI" |
| No conversational/polite filler | "hello", "please", "apologize", "sorry" |

Full paraphrased rules with software examples: [`SKILL.md`](skills/unanthropomorphic-english/SKILL.md).

## Not just docs

The skill ships adaptations ([`use-cases.md`](skills/unanthropomorphic-english/references/use-cases.md)) for:

- **Error messages**: what happened → why → what to do, in that order
- **Runbooks**: Imperative steps, conditions first, warnings before the step.
- **Incident reports**: simple past and third person ("the team reverted" instead of "we reverted")
- **Release notes**: breaking changes as warnings: command first, risk second
- **Your AGENTS.md / prompts**: a system prompt is a procedure. Models interpret "should" as optional; STE requires "must" or deletion.
- **Translation prep**: One meaning per word plus complete grammar removes most translation ambiguity.

Scope exclusion: marketing copy, blog voice, brand writing.

## Benchmarks

**81.5% fewer STE violations per 100 words with the skill on, averaged across 6 models × 8 writing tasks (96 generations, measured).**

| Model | Baseline viol/100w | Skill viol/100w | Reduction |
|---|---|---|---|
| claude-opus-4-8 | 2.34 | 0.62 | 74% |
| claude-opus-4-7 | 2.81 | 0.41 | 85% |
| claude-opus-4-6 | 3.14 | 0.40 | 87% |
| claude-opus-4-5 | 2.94 | 0.71 | 76% |
| claude-sonnet-5 | 3.76 | 0.53 | 86% |
| claude-sonnet-4-6 | 2.65 | 0.51 | 81% |

Linter methodology, caveats, and full benchmark results are detailed in [`evals/results/RESULTS.md`](evals/results/RESULTS.md). Reproduce the benchmark using `python3 evals/run_bench.py` (requires Claude Code CLI).

## Receipts

Developed using test-driven methodology against the primary ASD-STE100 Issue 9 specification (2025):

- Baseline models without the skill wrote 40-word sentences and invented non-existent rules (e.g., citing "Rule 3.1: short sentences", whereas the actual Rule 3.1 governs verb forms).
- Verification of the official PDF confirms that "can" and "will" are approved modals, contrary to some secondary online sources.
- The skill is verified against the baseline test suite in [`evals/pressure-tests.md`](evals/pressure-tests.md).

## FAQ

**Does this guarantee STE certification?** No. ASD does not certify tools. The pragmatic mode applies structural rules with project-specific vocabulary. The strict mode aligns closely with the standard. The official standard is available at [asd-ste100.org](https://www.asd-ste100.org/request.html).

**Will the output sound robotic?** The output is flat, clear, and unambiguous. This matches the requirements of technical documentation.

**Why not prompt "write clearly"?** "Clearly" is subjective. Structural constraints like sentence length limits are objective specifications that models can follow.

**Why use ASD-STE100?** The standard is maintained (Issue 9, January 2025), structured, and testable. Its rules directly counter common verbose writing patterns.

## License and status

MIT for everything here. The repo paraphrases the rules for teaching and reproduces **zero** spec text or dictionary content. Unofficial project, not affiliated with or endorsed by ASD or STEMG. ASD-STE100 is a registered trademark of ASD.

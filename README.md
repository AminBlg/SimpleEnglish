<p align="center">
  <strong>✈️ your AI writes like a LinkedIn post. make it write like a Boeing manual.</strong>
</p>

<p align="center">
  An agent skill that makes LLMs write plain English with the discipline of <a href="https://www.asd-ste100.org/">ASD-STE100 Simplified Technical English</a>:<br>
  the controlled language aerospace has used since 1983 so a tired mechanic <em>cannot</em> misread an instruction.<br>
  Layman-readable by default, STE-strict on request. AI slop dies as a side effect.
</p>

<p align="center">
  <a href="evals/results/RESULTS.md"><img src="https://img.shields.io/badge/STE_violations-%E2%88%9274.6%25_measured-brightgreen?style=flat" alt="74.6% fewer violations, measured"></a>
  <a href="evals/results/RESULTS.md"><img src="https://img.shields.io/badge/benchmarked_on-7_Claude_models-blueviolet?style=flat" alt="7 models benchmarked"></a>
  <a href="https://agentskills.io"><img src="https://img.shields.io/badge/SKILL.md-open_standard-blue?style=flat" alt="Agent Skills"></a>
  <a href="skills/simple-english/SKILL.md"><img src="https://img.shields.io/badge/version-2.0.0-blue?style=flat" alt="version 2.0.0"></a>
  <a href="LICENSE"><img src="https://img.shields.io/badge/license-MIT-lightgrey?style=flat" alt="MIT"></a>
  <a href="https://github.com/AminBlg/SimpleEnglish/stargazers"><img src="https://img.shields.io/github/stars/AminBlg/SimpleEnglish?style=flat&logo=github&color=yellow" alt="GitHub stars"></a>
</p>

<p align="center">
  <a href="https://trendshift.io/repositories/97933?utm_source=trendshift-badge&amp;utm_medium=badge&amp;utm_campaign=badge-trendshift-97933" target="_blank" rel="noopener noreferrer"><img src="https://trendshift.io/api/badge/trendshift/repositories/97933/daily" alt="AminBlg%2FSimpleEnglish | Trendshift" width="250" height="55"/></a>
</p>

Works in every agent that reads the [Agent Skills standard](https://agentskills.io): Claude Code, Cursor, VS Code Copilot, OpenAI Codex, Gemini CLI, Goose, OpenCode, and about 25 more. One folder, no dependencies, MIT.

## Install

**Any agent**, with the [skills CLI](https://github.com/vercel-labs/skills):

```bash
npx skills add AminBlg/SimpleEnglish
```

Try it before you install: `npx skills use AminBlg/SimpleEnglish@simple-english`

**Claude Code plugin** (skill, session hook, output style):

```bash
claude plugin marketplace add AminBlg/SimpleEnglish && claude plugin install simple-english@simple-english
```

The plugin also ships an [output style](https://code.claude.com/docs/en/output-styles), named `simple-english:simple-english`. The short name does not resolve. For one project, run `/config`, open **Output style**, and select it. For all projects, put `{"outputStyle": "simple-english:simple-english"}` in `~/.claude/settings.json` and start Claude Code again.

**Codex plugin** (skill, session hook):

```bash
codex plugin marketplace add AminBlg/SimpleEnglish
codex plugin add simple-english@simple-english
```

Codex asks you to trust the hook in `/hooks` before its first run. The hooks need Node.js. Details in [`src/hooks/README.md`](src/hooks/README.md).

**No skill support?** Paste [`prompts/system-prompt.md`](prompts/system-prompt.md) into your system prompt, `AGENTS.md`, or `.cursorrules`. It ends with a 60-token version for tight budgets. On claude.ai, ChatGPT, or Gemini, paste it as the first message.

Then ask for any technical writing, or say: *"rewrite this with simple-english"*.

## See it

Left is real, unedited Claude output. Right is the same model with the skill loaded.

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
</table>

More rewrites in [`examples/before-after.md`](examples/before-after.md): READMEs, runbooks, incident reports, error messages, release notes.

## Benchmarks

**74.6% fewer STE violations per 100 words with the skill on, averaged across 7 Claude models × 8 writing tasks (112 generations).** Measured on skill 1.3.0. The 2.0.0 pivot (Plain by default) was checked against 1.3.0 on two models, the reply set, and a blind judge: documents at parity, replies with 43% fewer violations. Details: [`evals/results/pivot-2026-09-01/RESULTS.md`](evals/results/pivot-2026-09-01/RESULTS.md). Deterministic regex linter, same rules for both conditions, reasoning effort pinned to `low`. Method, caveats, and raw files: [`evals/results/RESULTS.md`](evals/results/RESULTS.md). Reproduce with `python3 evals/run_bench.py` and a logged-in Claude Code CLI.

| Model | Baseline viol/100w | Skill viol/100w | Reduction |
|---|---|---|---|
| claude-opus-5 | 2.13 | 0.32 | 85% |
| claude-opus-4-8 | 1.05 | 0.62 | 41% |
| claude-opus-4-7 | 2.28 | 0.42 | 82% |
| claude-opus-4-6 | 2.24 | 0.40 | 82% |
| claude-opus-4-5 | 2.55 | 0.57 | 78% |
| claude-sonnet-5 | 2.67 | 0.53 | 80% |
| claude-sonnet-4-6 | 2.06 | 0.52 | 75% |

A blind pairwise judge (claude-opus-4-8, both text orders, no labels) preferred the skill output in 45 of 56 pairs, with 5 ties and 6 losses. Output tokens went down on all seven models.

**Other harnesses**, same 8 tasks, same linter, one run per cell:

| Harness | Model | Baseline viol/100w | Skill viol/100w | Reduction | Raw files |
|---|---|---:|---:|---:|---|
| Pi | GLM-5.2 max | 2.56 | 0.40 | 84.4% | [pi-2026-07-31](evals/results/pi-2026-07-31/RESULTS.md) |
| Pi | GPT-5.6 Sol medium | 1.33 | 0.16 | 88.0% | same |
| Pi | GPT-5.6 Terra medium | 1.69 | 0.48 | 71.6% | same |
| Pi | GPT-5.6 Luna medium | 1.28 | 0.42 | 67.2% | same |
| OpenAI API | gpt-4.1-mini | 3.43 | 0.14 | 95.8% | [openai-2026-09-01](evals/results/openai-2026-09-01/RESULTS.md) |

Every number above reproduces from committed raw files. Score any raw directory with `python3 evals/score_text_dir.py <dir>`.

## The rules

53 numbered rules in 9 sections, paraphrased with software examples in [`SKILL.md`](skills/simple-english/SKILL.md). The ones that do the work:

| Rule | What it kills |
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

Two modes. **Plain** (default) writes for a smart reader outside the field: the structural rules, common words, every technical term defined at first use, answer-first replies. **Strict** adds the STE dictionary discipline to the document when you name STE or compliance. The skill also covers error messages, runbooks, incident reports, release notes, agent prompts, and translation prep: [`use-cases.md`](skills/simple-english/references/use-cases.md). It does not touch marketing copy, on purpose.

## FAQ

**Does this make output STE-certified?** No. Nothing does, because ASD certifies no tool. Strict mode gets close; word-level rulings live in the official standard, a [free download](https://www.asd-ste100.org/request.html).

**Will my docs sound robotic?** They will sound like Airbus manuals: flat and impossible to misread. For docs that is the whole point. Keep your voice for your blog.

**Why not just prompt "write clearly"?** "Clearly" is an opinion. "No sentence over 20 words" is a spec. Agents follow specs.

**Why a 40-year-old aerospace standard?** It is maintained (Issue 9, January 2025), numbered, and testable. It is also a near-perfect negative of every AI writing tell.

**How was it built?** Against the primary Issue 9 text, not summaries. Agents without the skill invented rule numbers, so the skill carries the real ones. A community audit ([#4](https://github.com/AminBlg/SimpleEnglish/issues/4)) checked the vocabulary tables against the dictionary; the fix was A/B-tested before it merged. Scenarios and recorded results: [`evals/pressure-tests.md`](evals/pressure-tests.md).

## Star history

[![Star History Chart](https://api.star-history.com/chart?repos=AminBlg/SimpleEnglish&type=date&legend=top-left)](https://www.star-history.com/?repos=AminBlg%2FSimpleEnglish&type=date&legend=top-left)

## Contributing

Open an issue for questions and bug reports. Pull requests are welcome. Every number in this README reproduces from committed raw files, so a change that moves a number ships the raw files with it. Run `python3 evals/ste_lint.py --self-test` before you push.

## License

MIT for everything here. The repo paraphrases the rules for teaching and reproduces **zero** spec text or dictionary content. Unofficial project, not affiliated with or endorsed by ASD or STEMG. ASD-STE100 is a registered trademark of ASD.

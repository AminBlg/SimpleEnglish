<p align="center">
  <strong>✈️ your AI writes like a LinkedIn post. make it write like a Boeing manual.</strong>
</p>

<p align="center">
  An agent skill that makes LLMs write plain English with the discipline of <a href="https://www.asd-ste100.org/">ASD-STE100 Simplified Technical English</a>,<br>
  the controlled language aerospace has used since 1983 so that a tired mechanic cannot misread an instruction.<br>
  Layman-readable by default, STE-strict on request.
</p>

<p align="center">
  <a href="evals/results/rebuild-2026-09-02/RESULTS.md"><img src="https://img.shields.io/badge/reply_defects-%E2%88%9286%25_measured-brightgreen?style=flat" alt="86% fewer visible reply defects, measured"></a>
  <a href="evals/results/RESULTS.md"><img src="https://img.shields.io/badge/benchmarked_on-9_Claude_models-blueviolet?style=flat" alt="9 models benchmarked"></a>
  <a href="https://agentskills.io"><img src="https://img.shields.io/badge/SKILL.md-open_standard-blue?style=flat" alt="Agent Skills"></a>
  <a href="skills/simple-english/SKILL.md"><img src="https://img.shields.io/badge/version-2.0.2-blue?style=flat" alt="version 2.0.2"></a>
  <a href="LICENSE"><img src="https://img.shields.io/badge/license-MIT-lightgrey?style=flat" alt="MIT"></a>
  <a href="https://github.com/AminBlg/SimpleEnglish/stargazers"><img src="https://img.shields.io/github/stars/AminBlg/SimpleEnglish?style=flat&logo=github&color=yellow" alt="GitHub stars"></a>
</p>

<p align="center">
  <a href="https://trendshift.io/repositories/97933?utm_source=trendshift-badge&amp;utm_medium=badge&amp;utm_campaign=badge-trendshift-97933" target="_blank" rel="noopener noreferrer"><img src="https://trendshift.io/api/badge/trendshift/repositories/97933/daily" alt="AminBlg%2FSimpleEnglish | Trendshift" width="250" height="55"/></a>
</p>

Works in every agent that reads the [Agent Skills standard](https://agentskills.io): Claude Code, Cursor, VS Code Copilot, OpenAI Codex, Gemini CLI, Goose, OpenCode, and about 25 more. One folder, no dependencies, MIT.

## Install

Any agent, with the [skills CLI](https://github.com/vercel-labs/skills):

```bash
npx skills add AminBlg/SimpleEnglish
```

Claude Code plugin, with the session hook and the output style:

```bash
claude plugin marketplace add AminBlg/SimpleEnglish && claude plugin install simple-english@simple-english
```

The output style is named `simple-english:simple-english`. The short name does not resolve. Select it with `/config` under Output style, or put `{"outputStyle": "simple-english:simple-english"}` in `~/.claude/settings.json`.

Codex plugin, with the session hook:

```bash
codex plugin marketplace add AminBlg/SimpleEnglish
codex plugin add simple-english@simple-english
```

Codex asks you to trust the hook before its first run. The hooks need Node.js. Details in [`src/hooks/README.md`](src/hooks/README.md).

No skill support? Paste the rule block of [`prompts/system-prompt.md`](prompts/system-prompt.md) into your system prompt, `AGENTS.md`, or `.cursorrules`. The page ends with a 60-token version for tight budgets.

Then ask for any technical writing, or say "rewrite this with simple-english".

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

Every number below is recomputed from the committed raw files by `python3 evals/check_numbers.py`, which CI runs on every push. All Claude runs: `claude-sonnet-4-6`, low effort, no settings loaded. Judges are Claude models on Claude text, so family bias is possible.

Replies, 8 chat questions with a jargon term each, two runs, [raw files and tables](evals/results/rebuild-2026-09-02/RESULTS.md). Counts are totals over the 16 replies. **86% fewer visible defects** (over-cap sentences, em-dashes, bold, headers, bullets) with 2.0.1 than with no skill (406 → 58). A blind judge preferred 2.0.1 over 2.0.0 in 14 of 16 pairs.

| Condition | words | sentences | em-dashes | bold | headers | bullets |
|---|---:|---:|---:|---:|---:|---:|
| no skill | 216 | 16.8 | 62 | 79 | 25 | 52 |
| 2.0.0 | 184 | 14.4 | 43 | 72 | 4 | 52 |
| 2.0.1 | 146 | 7.9 | 5 | 2 | 0 | 4 |

The five-sentence cap holds in 5 of 16 sonnet replies. On gpt-4.1-mini the same 8 questions went from 23 sentences, 64 bold spans, and 101 bullets per 8 replies. With 2.0.1 they went to 5.2 sentences and zero formatting, 6 of 8 under the cap.

Documents, the 8 sqlpipe writing tasks scored with the STE linter, one run per cell. One run moves by about 0.5 on this model, so read the rows as parity or better, not as a ranking.

| Condition | viol/100w | Reduction |
|---|---:|---:|
| no skill | 4.09 | |
| 1.3.0 | 2.11 | 48% |
| 2.0.0 | 1.70 | 58% |
| 2.0.1 | 0.91 | 78% |

The linter history: 81.3% fewer linter violations across 9 Claude models (144 generations, [RESULTS.md](evals/results/RESULTS.md)), plus Pi, opencode, and OpenAI runs in [`evals/results/`](evals/results/). Those numbers reproduce. A [2026-09-02 audit](evals/results/WHY-USELESS-2026-09-02.md) showed that they measure rule obedience, not what a reader sees, which is why 2.0.1 reports the reply counts above.

## The rules

Two registers in [`SKILL.md`](skills/simple-english/SKILL.md), about 1,700 tokens. The 53 numbered rules of Issue 9 live in [`rule-catalog.md`](skills/simple-english/references/rule-catalog.md) for check mode and Strict mode.

The reply, every chat answer:

| Rule | What it kills |
|---|---|
| Prose only: no headers, bullets, bold, tables | The wall of formatting around a one-line answer |
| Five sentences maximum, list items included | The 240-word answer to "is that bad?" |
| First sentence answers | The preamble |
| No em-dashes | The spliced half-thought |
| Define a concept term in a few words | Jargon the reader has to look up |
| No contractions, openers, or closers | "Great question!" and "Hope this helps!" |

The document: docs, READMEs, runbooks, error messages, release notes:

| Rule | What it kills |
|---|---|
| Max 20 words per instruction, 25 per description | The run-on sentence |
| Condition before command | Trailing "...if the flag is set" that readers execute too late |
| Simple tenses, active voice | "has been updated", ", making it easy to..." |
| No should/would/may/might | Hedging. `can`, `will`, `must` survive |
| One word = one meaning, whole document | check/verify/confirm/validate roulette |
| Keep articles, keep "that" | Telegraph style. STE is short, not terse |
| No bold lead-ins, no heading over two sentences | Decoration that hides the fact |
| State the fact, not its importance | "crucial", "robust", "not just X, it is Y" |

Two modes. Plain, the default, is all of the above. Strict adds the STE dictionary discipline from [`strict-vocabulary.md`](skills/simple-english/references/strict-vocabulary.md) when you name STE, ASD-STE100, or compliance. The reply stays Plain in every mode.

## FAQ

Does this make output STE-certified? No. Nothing does, because ASD certifies no tool. Strict mode gets close. Word-level rulings live in the official standard, a [free download](https://www.asd-ste100.org/request.html).

Will my docs sound robotic? They will sound like Airbus manuals: flat and impossible to misread. For docs that is the whole point. Keep your voice for your blog.

Why not just prompt "write clearly"? "Clearly" is an opinion. "No sentence over 20 words" is a spec. Agents follow specs.

Why a 40-year-old aerospace standard? It is maintained (Issue 9, January 2025), numbered, and testable. It is also a near-perfect negative of every AI writing tell.

How was it built? Against the primary Issue 9 text, not summaries. A community audit ([#4](https://github.com/AminBlg/SimpleEnglish/issues/4)) checked the vocabulary tables against the dictionary. Scenarios and recorded results: [`evals/pressure-tests.md`](evals/pressure-tests.md).

## Star history

[![Star History Chart](https://api.star-history.com/chart?repos=AminBlg/SimpleEnglish&type=date&legend=top-left)](https://www.star-history.com/?repos=AminBlg%2FSimpleEnglish&type=date&legend=top-left)

## Word-choice linter

`evals/ste_lint.py` measures the mechanical rules and cannot see word choice. [`tools/ste-dictionary/`](tools/ste-dictionary/README.md) holds an extractor that builds the word lists from your own copy of the free Issue 9 PDF. A linter reads them. The repository ships the tool and no dictionary content, because the standard forbids reproduction without written authority from ASD.

## Contributing

Open an issue for questions and bug reports. Pull requests are welcome. A change that moves a published number ships the raw files with it, and `python3 evals/check_numbers.py` must pass. Run `python3 evals/ste_lint.py --self-test` before you push. Say in the PR whether an agent wrote the code, and do not add attribution trailers.

## License

MIT for everything here. The repo paraphrases the rules for teaching and reproduces no spec text or dictionary content. Unofficial project, not affiliated with or endorsed by ASD or STEMG. ASD-STE100 is a registered trademark of ASD.

# Simple English hooks

The Claude Code and Codex plugins include a `SessionStart` hook. The hook loads the Simple English writing rules when a session starts, resumes, clears, or compacts. You do not need to name the skill.

The hook needs Node.js. Both plugins run `src/hooks/simple-english-activate.js` with the `node` command.

## Install

Claude Code:

```bash
claude plugin marketplace add AminBlg/SimpleEnglish
claude plugin install simple-english@simple-english
```

Codex:

```bash
codex plugin marketplace add AminBlg/SimpleEnglish
codex plugin add simple-english@simple-english
```

Codex asks you to review and trust the hook before its first run. Open `/hooks` to approve it.

## What the hook sends

The hook writes `prompts/system-prompt.md` to standard output. That file is the condensed rule set, about 3,500 characters. The full skill, `skills/simple-english/SKILL.md`, is about 20,000 characters, and Claude Code caps hook output at 10,000 characters. Output over the cap goes to a file and the model gets only a preview. The condensed rules fit, and the hook names the full skill path so the model can read it for a compliance check or strict mode.

Codex applies its own cap to hook context. The `additionalContextLimit: 0` setting in `hooks/hooks.json` turns off the spill-to-disk threshold. It does not remove the cap. The condensed rules fit under it.

If the hook cannot read the prompt file, it tries the next location. If every location fails, it prints a short fallback rule set and exits 0. The session still starts.

## Where each harness loads the hook

- Claude Code: the `hooks` field in `.claude-plugin/plugin.json`.
- Codex: `hooks/hooks.json`, named by the `hooks` field in `.codex-plugin/plugin.json`. The marketplace catalog is `.agents/plugins/marketplace.json`.

## Test

From the repository root:

```bash
node --test src/hooks/simple-english-activate.test.js
```

## Advisory writing checks (Claude Code)

Two more hooks run under Claude Code, both advisory. Neither one blocks.

- `PostToolUse` on `Write` and `Edit`: when the file is Markdown, `src/hooks/lint_hook.py` lints it with `evals/ste_lint.py` and shows a one-line summary of the violations to the model.
- `Stop`: the same script reads the last reply and adds a system message when the reply breaks the register: more than five sentences outside code and lists, a filler opener or closer, or a slop word.

Codex runs only the `SessionStart` hook. Test the checks with `python3 src/hooks/test_lint_hook.py`.

## What the file check skips

The writing rules cover the documents that you write for a reader. They do not cover the files that the agent keeps for itself, such as memory files. A summary of the violations in such a file only spends tokens. The `PostToolUse` check therefore skips three groups of paths:

- Every path under the Claude configuration directory. The check reads `CLAUDE_CONFIG_DIR` and falls back to `~/.claude`.
- Every path with a `.claude` directory component, for example `my-project/.claude/agent-memory/reviewer/MEMORY.md`. A skill or a command that you write under `.claude/` is also skipped.
- Every path that matches a glob in `SIMPLE_ENGLISH_LINT_EXCLUDE`.

A symlink does not defeat a skip. The check tests the absolute path in two forms, as written and with the symlinks resolved. A match on either form is enough.

`SIMPLE_ENGLISH_LINT_EXCLUDE` holds glob patterns, separated by the path separator of the platform (`:` on Linux and macOS, `;` on Windows). In a pattern, `*` also matches `/`. The check expands a leading `~` to your home directory.

```bash
export SIMPLE_ENGLISH_LINT_EXCLUDE="$HOME/notes/*:*/CHANGELOG.md"
```

To turn the file check off, set the variable to `*`. The `Stop` reply check stays on.

# Simple English Hooks

The Claude Code and Codex plugins include a `SessionStart` hook. The hook loads the Simple English skill automatically when a session starts.

Plugin users do not need to invoke the skill manually. Install the plugin, then start a new session.

The hooks require Node.js. Both plugins run `src/hooks/simple-english-activate.js` with the `node` command.

For Claude Code:

```bash
claude plugin marketplace add AminBlg/SimpleEnglish
claude plugin install simple-english@simple-english
```

For Codex, install the full plugin instead of the standalone skill:

```bash
codex plugin marketplace add AminBlg/SimpleEnglish
codex plugin add simple-english@simple-english
```

Codex asks you to review and trust the hook before its first run. Open `/hooks` to approve it.

## How It Works

The hook reads `skills/simple-english/SKILL.md`. It writes the skill body to standard output as hidden session context.

It runs after startup, resume, clear, or context compaction. This behavior reloads the rules when the agent rebuilds its context.

The skill file stays the source of truth. A change to the skill rules takes effect without a duplicate hook update.

If the hook cannot find the skill file, it loads a small fallback ruleset. This fallback keeps the session usable and does not block startup.

## Scope

Automatic loading does not apply STE to all text. The scope in `SKILL.md` still controls when the agent uses the rules.

Claude Code loads its hook from `.claude-plugin/plugin.json`. Codex loads its hook from `hooks/hooks.json` through `.codex-plugin/plugin.json`.

The Codex hook uses `additionalContextLimit: 0`. This setting passes the complete skill to the model instead of the default truncated context.

## Test

Run this command from the repository root:

```bash
node --test src/hooks/simple-english-activate.test.js
```

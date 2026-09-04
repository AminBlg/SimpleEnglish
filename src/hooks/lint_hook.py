#!/usr/bin/env python3
"""Advisory writing checks for Claude Code hooks. Never blocks.

PostToolUse (Write|Edit on a .md file): lint the file with evals/ste_lint.py
and, when it has violations, print a short summary to stderr and exit 2 so
the model sees it. Exit 2 on PostToolUse is advisory: the tool already ran.
Agent-internal Markdown, such as memory files under the Claude configuration
directory, is skipped. The writing rules do not govern it, and a summary of
its violations only spends tokens. Set SIMPLE_ENGLISH_LINT_EXCLUDE to skip
more paths.

Stop: read `last_assistant_message`, check the reply register (five sentences or
fewer with list items counted, no headers, bullets, bold, or em-dashes), and return a systemMessage only when
the reply breaks it. Always exit 0, so the session never loops.
"""
import fnmatch
import json
import os
import pathlib
import re
import sys

HERE = pathlib.Path(__file__).resolve().parent
ROOT = HERE.parent.parent
sys.path.insert(0, str(ROOT / "evals"))

MAX_REPLY_SENTENCES = 5
CLAUDE_DIR = ".claude"
OPENERS = re.compile(r"^\s*(certainly|great question|you're absolutely right|sure[,!]|absolutely[,!])", re.I)
CLOSERS = re.compile(r"(i hope this helps|let me know if|feel free to)", re.I)


def load_linter():
    try:
        import ste_lint  # noqa: WPS433
        return ste_lint
    except Exception:  # noqa: BLE001
        return None


def strip_code(text):
    text = re.sub(r"```.*?```", " ", text, flags=re.S)
    return re.sub(r"`[^`]*`", " ", text)


def absolute(path, cwd=None):
    """Make the path absolute. The harness can send it relative to the session directory."""
    return pathlib.Path(cwd or ".", pathlib.Path(path).expanduser()).absolute()


def variants(path):
    """The path as written and the path with symlinks resolved. An exclusion matches either form.

    A symlink hides a directory name in both directions. `notes.md` can point into `.claude`,
    and `.claude` itself can point at a dotfiles repository. Both forms must miss for the
    file to reach the linter.
    """
    return {pathlib.Path(os.path.normpath(path)), path.resolve()}


def excluded(target):
    """True for agent-internal Markdown and for the paths the user excludes."""
    config_dirs = variants(absolute(os.environ.get("CLAUDE_CONFIG_DIR") or f"~/{CLAUDE_DIR}"))
    raw = os.environ.get("SIMPLE_ENGLISH_LINT_EXCLUDE", "").split(os.pathsep)
    patterns = [os.path.expanduser(p) for p in raw if p]
    for form in variants(target):
        if CLAUDE_DIR in form.parts or any(form.is_relative_to(d) for d in config_dirs):
            return True
        if any(fnmatch.fnmatch(str(form), p) for p in patterns):
            return True
    return False


def post_tool_use(event):
    path = (event.get("tool_input") or {}).get("file_path") or ""
    if not path.endswith(".md"):
        return 0
    target = absolute(path, event.get("cwd"))
    if excluded(target):
        return 0
    lint = load_linter()
    if lint is None:
        return 0
    try:
        text = target.read_text(encoding="utf-8")
    except OSError:
        return 0
    report = lint.lint(text, "descriptive")
    hits = {k: v for k, v in report["violations"].items() if v}
    if not hits:
        return 0
    summary = ", ".join(f"{k} {v}" for k, v in hits.items())
    sys.stderr.write(
        f"simple-english: {target.name} has {report['violations_total']} STE violations "
        f"({summary}). Run the self-check in SKILL.md before you deliver.\n"
    )
    return 2


def stop(event):
    reply = event.get("last_assistant_message") or ""
    problems = []
    lint = load_linter()
    if lint is not None:
        c = lint.reader_check(reply)["counts"]
        if c["over_cap"]:
            problems.append(f"{c['sentences']} sentences, list items included (limit {MAX_REPLY_SENTENCES})")
        for key, label in (("em_dash", "em-dash"), ("bold_spans", "bold span"), ("headers", "header"), ("bullets", "list item")):
            if c[key]:
                problems.append(f"{c[key]} {label}(s)")
        slop = lint.lint(strip_code(reply), "descriptive")["violations"].get("slop_word", 0)
        if slop:
            problems.append(f"{slop} slop word(s)")
    if OPENERS.search(reply):
        problems.append("a filler opener")
    if CLOSERS.search(reply):
        problems.append("a filler closer")
    if problems:
        print(json.dumps({"systemMessage": "simple-english reply check: " + "; ".join(problems) + ". Answer in prose, five sentences or fewer."}))
    return 0


def main():
    try:
        event = json.load(sys.stdin)
    except Exception:  # noqa: BLE001
        return 0
    try:
        name = event.get("hook_event_name", "")
        if name == "PostToolUse":
            return post_tool_use(event)
        if name == "Stop":
            return stop(event)
    except Exception:  # noqa: BLE001  advisory hook: a crash must never block or loop the session
        return 0
    return 0


if __name__ == "__main__":
    sys.exit(main())

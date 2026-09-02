#!/usr/bin/env python3
"""Advisory writing checks for Claude Code hooks. Never blocks.

PostToolUse (Write|Edit on a .md file): lint the file with evals/ste_lint.py
and, when it has violations, print a short summary to stderr and exit 2 so
the model sees it. Exit 2 on PostToolUse is advisory: the tool already ran.

Stop: read `last_assistant_message`, check the reply register (five sentences or
fewer with list items counted, no headers, bullets, bold, or em-dashes), and return a systemMessage only when
the reply breaks it. Always exit 0, so the session never loops.
"""
import json
import pathlib
import re
import sys

HERE = pathlib.Path(__file__).resolve().parent
ROOT = HERE.parent.parent
sys.path.insert(0, str(ROOT / "evals"))

MAX_REPLY_SENTENCES = 5
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


def post_tool_use(event):
    path = (event.get("tool_input") or {}).get("file_path", "")
    if not path.endswith(".md"):
        return 0
    lint = load_linter()
    if lint is None:
        return 0
    try:
        text = pathlib.Path(path).read_text(encoding="utf-8")
    except OSError:
        return 0
    report = lint.lint(text, "descriptive")
    hits = {k: v for k, v in report["violations"].items() if v}
    if not hits:
        return 0
    summary = ", ".join(f"{k} {v}" for k, v in hits.items())
    sys.stderr.write(
        f"simple-english: {pathlib.Path(path).name} has {report['violations_total']} STE violations "
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
    name = event.get("hook_event_name", "")
    if name == "PostToolUse":
        return post_tool_use(event)
    if name == "Stop":
        return stop(event)
    return 0


if __name__ == "__main__":
    sys.exit(main())

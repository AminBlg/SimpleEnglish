#!/usr/bin/env python3
"""Advisory writing checks for Claude Code hooks. Never blocks.

PostToolUse (Write|Edit|MultiEdit on a .md file): lint the text that the
tool just wrote, not the whole file. Write carries it in tool_input.content,
Edit in tool_input.new_string, and MultiEdit in each edits[].new_string.
When the payload has no written text, the check falls back to the file on
disk so older callers still work. Hits print the offending text and the
line number in the file (capped at MAX_HOOK_HITS) to stderr and exit 2 so
the model sees them. Exit 2 on PostToolUse is advisory: the tool already
ran. Agent-internal Markdown, such as memory files under the Claude
configuration directory, is skipped. The writing rules do not govern it,
and a summary of its violations only spends tokens. Set
SIMPLE_ENGLISH_LINT_EXCLUDE to skip more paths.

Stop: read `last_assistant_message`, check the reply register (no bold and
no em-dashes), and return a systemMessage only when the reply
breaks it. Always exit 0, so the session never loops.
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

MAX_HOOK_HITS = 12
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


def written_segments(tool_name, tool_input):
    """The prose the tool just wrote, or None when the payload has none.

    None means fall back to the whole file. An empty list means the tool
    wrote nothing to lint.
    """
    tool_input = tool_input or {}
    name = (tool_name or "").strip()
    if name == "Write" and "content" in tool_input:
        content = tool_input.get("content")
        return [content] if isinstance(content, str) else None
    if name == "Edit" and "new_string" in tool_input:
        new_string = tool_input.get("new_string")
        return [new_string] if isinstance(new_string, str) else None
    if name == "MultiEdit":
        edits = tool_input.get("edits")
        if not isinstance(edits, list):
            return None
        segments = []
        for edit in edits:
            if isinstance(edit, dict) and isinstance(edit.get("new_string"), str):
                segments.append(edit["new_string"])
        return segments
    return None


def start_line_in_file(file_text, snippet):
    """1-based line where snippet begins in file_text. 1 if the snippet is missing."""
    if not snippet:
        return 1
    index = file_text.find(snippet)
    if index < 0:
        return 1
    return file_text.count("\n", 0, index) + 1


def remap_hits(hits, base_line):
    """Shift segment-local line numbers onto the file."""
    offset = base_line - 1
    return [{**hit, "line": hit["line"] + offset} for hit in hits]


def collect_hits(lint, segments, file_text):
    """Lint each written segment and report hits with file line numbers."""
    hits = []
    for segment in segments:
        if not segment:
            continue
        detail = lint.lint_detail(segment, "descriptive")
        hits.extend(remap_hits(detail, start_line_in_file(file_text, segment)))
    hits.sort(key=lambda hit: hit["line"])
    return hits


def post_tool_use(event):
    tool_input = event.get("tool_input") or {}
    path = tool_input.get("file_path") or ""
    if not path.endswith(".md"):
        return 0
    target = absolute(path, event.get("cwd"))
    if excluded(target):
        return 0
    lint = load_linter()
    if lint is None:
        return 0
    segments = written_segments(event.get("tool_name"), tool_input)
    try:
        file_text = target.read_text(encoding="utf-8")
    except OSError:
        file_text = ""
    if segments is None:
        if not file_text:
            return 0
        hits = lint.lint_detail(file_text, "descriptive")
    else:
        hits = collect_hits(lint, segments, file_text)
    if not hits:
        return 0
    lines = [f"simple-english: {target.name} has {len(hits)} STE violations."]
    for hit in hits[:MAX_HOOK_HITS]:
        lines.append(f"  line {hit['line']}, {hit['category']}: {hit['text']}")
    if len(hits) > MAX_HOOK_HITS:
        lines.append(f"  and {len(hits) - MAX_HOOK_HITS} more hit(s).")
    lines.append("Fix these hits in the text you just wrote, then continue.")
    sys.stderr.write("\n".join(lines) + "\n")
    return 2


def stop(event):
    reply = event.get("last_assistant_message") or ""
    problems = []
    lint = load_linter()
    if lint is not None:
        c = lint.reader_check(reply)["counts"]
        for key, label in (("em_dash", "em-dash"), ("bold_spans", "bold span")):
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
        print(json.dumps({"systemMessage": "simple-english reply check: " + "; ".join(problems) + "."}))
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

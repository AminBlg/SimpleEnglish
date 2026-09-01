#!/usr/bin/env python3
"""Reply-register benchmark: chat questions, not documents.

For each prompt in reply_scenarios.json, runs `claude -p` twice (baseline and
with a skill file as system context) and scores the reply on:

- answer_first: the first sentence contains no filler opener and states a result
  or an instruction (heuristic: no opener pattern, and it is not a question)
- sentences: count outside code blocks and list items (target 5 or fewer)
- slop_per_100w: from ste_lint's slop check
- term_defined: the scenario's jargon term appears with a definition marker
  nearby: "(", "is", "means", "that is", "a kind of"

    python3 evals/run_reply_bench.py --skill skills/unanthropomorphic-english/SKILL.md \
        --model claude-sonnet-4-6 --out /tmp/reply-run
"""
import argparse
import json
import pathlib
import re
import subprocess
import sys

HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import ste_lint  # noqa: E402

OPENER = re.compile(r"^\s*(certainly|great question|sure[,!]|absolutely|you're (absolutely )?right|good question|happy to)", re.I)
CLOSER = re.compile(r"(i hope this helps|let me know|feel free to reach out)", re.I)


def strip_code(text):
    text = re.sub(r"```.*?```", " ", text, flags=re.S)
    return re.sub(r"`[^`]*`", " ", text)


def sentences(text):
    prose = "\n".join(l for l in strip_code(text).splitlines() if not re.match(r"^\s*([-*]|\d+\.|#)\s", l))
    return [s for s in re.split(r"(?<=[.!?])\s+", prose.strip()) if len(s.split()) > 1]


def term_defined(text, term):
    body = strip_code(text)
    for m in re.finditer(re.escape(term), body, re.I):
        window = body[m.end(): m.end() + 90]
        if re.match(r"\s*\(", window) or re.match(r"\s*(is|are|means|refers to|that is|:)\b", window, re.I):
            return True
        before = body[max(0, m.start() - 60): m.start()]
        if re.search(r"(called|known as|term for)\s*$", before, re.I):
            return True
    return False


def score(text, term):
    sents = sentences(text)
    lint = ste_lint.lint(text, "descriptive")
    first = sents[0] if sents else ""
    return {
        "sentences": len(sents),
        "answer_first": bool(first) and not OPENER.search(text) and not first.rstrip().endswith("?"),
        "closer": bool(CLOSER.search(text)),
        "slop_per_100w": round(100 * lint["violations"]["slop_word"] / max(lint["words"], 1), 2),
        "viol_per_100w": lint["violations_per_100w"],
        "term_defined": term_defined(text, term),
        "words": lint["words"],
    }


def generate(prompt, system, model, effort):
    cmd = ["claude", "-p", "--model", model, "--output-format", "json"]
    if system:
        cmd += ["--append-system-prompt", system]
    if effort:
        cmd += ["--effort", effort]
    r = subprocess.run(cmd + [prompt], capture_output=True, text=True, timeout=300)
    return extract_result(r.stdout)


def extract_result(stdout):
    """claude -p --output-format json returns one object or a list of events."""
    try:
        data = json.loads(stdout)
    except Exception:  # noqa: BLE001
        return stdout.strip()
    if isinstance(data, dict):
        return data.get("result", "")
    for item in reversed(data):
        if isinstance(item, dict) and item.get("type") == "result":
            return item.get("result", "")
    return ""


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--skill", required=True)
    ap.add_argument("--model", default="claude-sonnet-4-6")
    ap.add_argument("--effort", default="low")
    ap.add_argument("--out", required=True)
    ap.add_argument("--label", default="skill")
    a = ap.parse_args()
    out = pathlib.Path(a.out); out.mkdir(parents=True, exist_ok=True)
    skill = pathlib.Path(a.skill).read_text()
    scen = json.loads((HERE / "reply_scenarios.json").read_text())
    rows = []
    for s in scen:
        for cond, system in (("baseline", None), (a.label, skill)):
            f = out / f"{cond}__{s['id']}.txt"
            if not f.exists() or not f.read_text().strip():
                f.write_text(generate(s["prompt"], system, a.model, a.effort))
            sc = score(f.read_text(), s["term"])
            sc.update(cond=cond, id=s["id"])
            rows.append(sc)
            print(f"{cond:9} {s['id']:12} sent={sc['sentences']:2} first={int(sc['answer_first'])} def={int(sc['term_defined'])} slop={sc['slop_per_100w']:.2f} viol={sc['viol_per_100w']:.2f}", flush=True)
    (out / "scores.json").write_text(json.dumps(rows, indent=1))
    for cond in ("baseline", a.label):
        rs = [r for r in rows if r["cond"] == cond]
        n = len(rs)
        print(f"{cond:9} n={n} mean_sent={sum(r['sentences'] for r in rs)/n:.1f} answer_first={sum(r['answer_first'] for r in rs)}/{n} "
              f"term_defined={sum(r['term_defined'] for r in rs)}/{n} closers={sum(r['closer'] for r in rs)} "
              f"slop/100w={sum(r['slop_per_100w'] for r in rs)/n:.2f} viol/100w={sum(r['viol_per_100w'] for r in rs)/n:.2f} words={sum(r['words'] for r in rs)/n:.0f}")


if __name__ == "__main__":
    main()

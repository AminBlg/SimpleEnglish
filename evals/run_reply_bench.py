#!/usr/bin/env python3
"""Reply-register benchmark: what a reader sees in a chat reply.

For each prompt in reply_scenarios.json, runs `claude -p` once per condition
(baseline plus each --skill label=path) and scores the reply with
ste_lint.reader_check: sentences (list items count), over-cap, em-dashes,
bold spans, headers, bullets, contractions, and whether the first sentence
holds a filler opener.

    python3 evals/run_reply_bench.py --skill new=prompts/system-prompt.md \
        --skill old=/path/to/old-system-prompt.md --out evals/results/reply-run
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

OPENER = re.compile(r"^\s*\W*(certainly|great question|sure[,!]|absolutely|you're (absolutely )?right|good question|happy to)", re.I)
CLOSER = re.compile(r"(i hope this helps|let me know|feel free to reach out)", re.I)


def score(text):
    r = ste_lint.reader_check(text)
    lint = ste_lint.lint(text, "descriptive")
    out = dict(r["counts"])
    out.update(words=r["words"], visible_total=r["visible_total"], under_cap=r["under_cap"],
               opener=bool(OPENER.search(text)), closer=bool(CLOSER.search(text)),
               slop_word=lint["violations"]["slop_word"], viol_per_100w=lint["violations_per_100w"])
    return out


def generate(prompt, system, model, effort):
    cmd = ["claude", "-p", prompt, "--model", model, "--output-format", "json", "--setting-sources", "",
           "--disallowedTools", "Bash,Read,Write,Edit,Glob,Grep,WebFetch,WebSearch"]
    if system:
        cmd += ["--append-system-prompt", system]
    if effort:
        cmd += ["--effort", effort]
    r = subprocess.run(cmd, capture_output=True, text=True, timeout=300, cwd="/tmp")
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
    ap.add_argument("--skill", action="append", default=[], help="label=path, repeatable")
    ap.add_argument("--model", default="claude-sonnet-4-6")
    ap.add_argument("--effort", default="low")
    ap.add_argument("--out", required=True)
    ap.add_argument("--report-only", action="store_true")
    a = ap.parse_args()
    out = pathlib.Path(a.out); out.mkdir(parents=True, exist_ok=True)
    conds = {"baseline": None}
    for item in a.skill:
        label, path = item.split("=", 1)
        conds[label] = pathlib.Path(path).read_text()
    scen = json.loads((HERE / "reply_scenarios.json").read_text())
    rows = []
    for s in scen:
        for cond, system in conds.items():
            f = out / f"{cond}__{s['id']}.txt"
            if not f.exists() or not f.read_text().strip():
                if a.report_only:
                    continue
                f.write_text(generate(s["prompt"], system, a.model, a.effort))
            text = f.read_text()
            if "session limit" in text or "Not logged in" in text:
                print(f"SKIP {f.name}: harness message, not a reply", file=sys.stderr)
                continue
            sc = score(text); sc.update(cond=cond, id=s["id"]); rows.append(sc)
            print(f"{cond:9} {s['id']:12} sent={sc['sentences']:2} em={sc['em_dash']} bold={sc['bold_spans']} hdr={sc['headers']} bul={sc['bullets']} words={sc['words']}", flush=True)
    (out / "scores.json").write_text(json.dumps(rows, indent=1))
    print()
    print("| condition | n | words | sentences | under cap | em-dash | bold | headers | bullets | openers | linter viol/100w |")
    print("|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|")
    for cond in conds:
        rs = [r for r in rows if r["cond"] == cond]
        n = len(rs)
        if not n:
            continue
        print(f"| {cond} | {n} | {sum(r['words'] for r in rs)/n:.0f} | {sum(r['sentences'] for r in rs)/n:.1f} | {sum(r['under_cap'] for r in rs)}/{n} | "
              f"{sum(r['em_dash'] for r in rs)} | {sum(r['bold_spans'] for r in rs)} | {sum(r['headers'] for r in rs)} | {sum(r['bullets'] for r in rs)} | "
              f"{sum(r['opener'] for r in rs)} | {sum(r['viol_per_100w'] for r in rs)/n:.2f} |")


if __name__ == "__main__":
    main()

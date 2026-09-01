#!/usr/bin/env python3
"""Benchmark the compressed package against the full skill.

Four conditions:
  baseline    no instructions          (reused from evals/results/raw)
  skill       skills/simple-english/SKILL.md   (reused from evals/results/raw)
  core        package/ste-core.md
  core+dict   package/ste-core.md + package/not-approved.tsv

Each output is scored with two independent linters:
  ste_lint.py       mechanical writing rules (sentence length, tense, modals)
  ste_dict_lint.py  word choice against the not-approved list

Read the two scores separately. The dictionary condition is scored with a
linter built from the same file that the condition puts in the prompt, so part
of any word-choice gain is definitional. The baseline and skill columns show
how much of it is real.

Usage:
  python3 bench_core.py --score-only     # score existing raw outputs, no calls
  python3 bench_core.py                  # generate the core conditions, then score
"""
import json
import pathlib
import sys
import time

HERE = pathlib.Path(__file__).resolve().parent
REPO = HERE.parent
sys.path.insert(0, str(REPO / "evals"))
sys.path.insert(0, str(HERE))

import ste_lint          # noqa: E402
import ste_dict_lint     # noqa: E402
from run_bench import call_claude  # noqa: E402

RAW_OLD = REPO / "evals" / "results" / "raw"
RAW_NEW = HERE / "results" / "raw"
MODELS = ["claude-opus-4-8", "claude-sonnet-4-6"]
SCENARIOS = json.loads((REPO / "evals" / "scenarios.json").read_text())


def prefix(condition):
    core = (HERE / "ste-core.md").read_text()
    if condition == "core":
        return core
    return core + "\n\n## Words that are not approved\n\nDo not use the word in column 1. Use an alternative from column 3.\n\n" + (HERE / "not-approved.tsv").read_text()


def build_prompt(scenario, condition):
    return ("Follow these writing instructions exactly, including the self-check step:\n\n"
            + prefix(condition) + "\n\n---\n\nTask: " + scenario["prompt"]
            + "\n\nReturn only the final text, no rule commentary.")


def generate():
    RAW_NEW.mkdir(parents=True, exist_ok=True)
    todo = [(m, c, s) for m in MODELS for c in ("core", "core+dict") for s in SCENARIOS]
    for i, (model, cond, sc) in enumerate(todo, 1):
        out = RAW_NEW / f"{model}__{cond}__{sc['id']}.json"
        if out.exists():
            continue
        print(f"[{i}/{len(todo)}] {model} {cond} {sc['id']}", flush=True)
        try:
            res = call_claude(build_prompt(sc, cond), model)
        except Exception as e:
            print(f"  FAILED: {e}", flush=True)
            continue
        res.update(model=model, condition=cond, scenario=sc["id"], type=sc["type"])
        out.write_text(json.dumps(res, indent=2))
        time.sleep(2)


def collect():
    """Return every run from both raw directories, scored with both linters."""
    table = ste_dict_lint.load()
    rows = []
    for path in sorted(RAW_OLD.glob("*.json")) + sorted(RAW_NEW.glob("*.json")):
        if "__judge__" in path.name:
            continue
        d = json.loads(path.read_text())
        if d["model"] not in MODELS:
            continue
        d["lint"] = ste_lint.lint(d["text"], d["type"])
        d["dict"] = ste_dict_lint.lint(d["text"], table)
        rows.append(d)
    return rows


def report(rows):
    order = ["baseline", "skill", "core", "core+dict"]
    lines = ["| model | condition | n | violations/100w | not-approved/100w | residual/100w | mean sentence |",
             "|---|---|---|---|---|---|---|"]
    summary = {}
    for model in MODELS:
        for cond in order:
            runs = [r for r in rows if r["model"] == model and r["condition"] == cond]
            if not runs:
                continue
            v = sum(r["lint"]["violations_per_100w"] for r in runs) / len(runs)
            w = sum(r["dict"]["not_approved_per_100w"] for r in runs) / len(runs)
            s = sum(r["lint"]["mean_sentence_words"] for r in runs) / len(runs)
            q = sum(r["dict"]["residual_per_100w"] for r in runs) / len(runs)
            summary[(model, cond)] = (round(v, 2), round(w, 2), round(q, 2), round(s, 1))
            lines.append(f"| {model} | {cond} | {len(runs)} | {v:.2f} | {w:.2f} | {q:.2f} | {s:.1f} |")
    return "\n".join(lines), summary


if __name__ == "__main__":
    if "--score-only" not in sys.argv:
        generate()
    text, _ = report(collect())
    (HERE / "results").mkdir(exist_ok=True)
    (HERE / "results" / "table.md").write_text(text + "\n")
    print(text)

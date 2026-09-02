"""Score a directory of raw text generations with ste_lint.

Files are named <model>__<condition>__<scenario>.txt, or
<condition>__<scenario>.txt for a single-model run. Prints one row per
model and a pooled row. This reproduces the tables in
evals/results/opencode-*/RESULTS.md and evals/results/openai-*/RESULTS.md.

    python3 evals/score_text_dir.py evals/results/openai-2026-09-01/raw
"""
import json
import pathlib
import re
import sys

HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import ste_lint  # noqa: E402

ANSI = re.compile(r"\x1b\[[0-9;]*[A-Za-z]")
SCEN = {s["id"]: s for s in json.loads((HERE / "scenarios.json").read_text())}


def clean(text):
    """Strip terminal colour codes and the opencode banner line."""
    text = ANSI.sub("", text)
    return re.sub(r"^\s*>\s*build ·.*$", "", text, flags=re.M).strip()


def main(raw_dir):
    rows = {}
    for p in sorted(pathlib.Path(raw_dir).glob("*.txt")):
        text = clean(p.read_text())
        if not text:
            continue  # a timed-out or errored cell; counted in the RESULTS notes
        parts = p.stem.split("__")
        model, cond, sid = parts if len(parts) == 3 else ["(single)"] + parts
        r = ste_lint.lint(text, SCEN[sid]["type"])
        m = rows.setdefault(model, {"baseline": [0, 0], "skill": [0, 0]})
        m[cond][0] += r["violations_total"]
        m[cond][1] += r["words"]
    print("| Model | Baseline viol/100w | Skill viol/100w | Reduction |")
    print("|---|---:|---:|---:|")
    total = {"baseline": [0, 0], "skill": [0, 0]}
    for model, m in rows.items():
        if not m["baseline"][1] or not m["skill"][1]:
            print(f"| {model} | (no complete cells) | | |")
            continue
        b = 100 * m["baseline"][0] / m["baseline"][1]
        s = 100 * m["skill"][0] / m["skill"][1]
        for c in total:
            total[c][0] += m[c][0]
            total[c][1] += m[c][1]
        print(f"| {model} | {b:.2f} | {s:.2f} | {(b - s) / b * 100:.1f}% |")
    if len(rows) > 1:
        b = 100 * total["baseline"][0] / total["baseline"][1]
        s = 100 * total["skill"][0] / total["skill"][1]
        print(f"| pooled | {b:.2f} | {s:.2f} | {(b - s) / b * 100:.1f}% |")


if __name__ == "__main__":
    main(sys.argv[1])

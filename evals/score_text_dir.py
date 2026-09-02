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
    """Files are named [model__]condition__scenario.txt. Any condition names work;
    the first condition sorted is the reference for the reduction column."""
    rows = {}
    for p in sorted(pathlib.Path(raw_dir).glob("*.txt")):
        parts = p.stem.split("__")
        model, cond, sid = parts if len(parts) == 3 else ["(single)"] + parts
        text = clean(p.read_text())
        if not text.strip() or "session limit" in text or "Not logged in" in text:
            continue
        r = ste_lint.lint(text, SCEN[sid]["type"])
        v = ste_lint.reader_check(text)["counts"]
        m = rows.setdefault(model, {}).setdefault(cond, {"viol": 0, "words": 0, "em": 0, "bold": 0, "n": 0})
        m["viol"] += r["violations_total"]; m["words"] += r["words"]; m["n"] += 1
        m["em"] += v["em_dash"]; m["bold"] += v["bold_spans"]
    conds = sorted({c for m in rows.values() for c in m}, key=lambda c: (c != "baseline", c))
    print("| Model | Condition | n | viol/100w | Reduction vs " + conds[0] + " | em-dash | bold spans | words |")
    print("|---|---|---:|---:|---:|---:|---:|---:|")
    pooled = {}
    for model, m in rows.items():
        base = 100 * m[conds[0]]["viol"] / max(1, m[conds[0]]["words"]) if conds[0] in m else None
        for c in conds:
            if c not in m:
                continue
            d = m[c]; rate = 100 * d["viol"] / max(1, d["words"])
            red = f"{(base - rate) / base * 100:.1f}%" if base else "-"
            print(f"| {model} | {c} | {d['n']} | {rate:.2f} | {red} | {d['em']} | {d['bold']} | {d['words'] // max(1, d['n'])} |")
            q = pooled.setdefault(c, {"viol": 0, "words": 0})
            q["viol"] += d["viol"]; q["words"] += d["words"]
    if len(rows) > 1:
        base = 100 * pooled[conds[0]]["viol"] / max(1, pooled[conds[0]]["words"])
        for c in conds:
            rate = 100 * pooled[c]["viol"] / max(1, pooled[c]["words"])
            print(f"| pooled | {c} | | {rate:.2f} | {(base - rate) / base * 100:.1f}% | | | |")


if __name__ == "__main__":
    main(sys.argv[1])

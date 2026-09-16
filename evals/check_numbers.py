#!/usr/bin/env python3
"""Recompute every published number from the raw files and compare it with the text.

Run it before you push. CI runs it on every push and pull request.

    python3 evals/check_numbers.py            # exit 1 on the first mismatch
    python3 evals/check_numbers.py --print    # show the recomputed values

Checks:
- README benchmark numbers against evals/results/rebuild-2026-09-02/ (replies,
  judge, gpt-4.1-mini, documents) and against evals/results/results.json.
- The rebuild RESULTS.md pooled-defect sentence.
- The rule block: prompts/system-prompt.md and output-styles/simple-english.md
  carry the same text, and SKILL.md carries the same reply rules.
- The version string in SKILL.md, the three manifests, and the README badge.
"""
import glob
import json
import pathlib
import re
import sys

HERE = pathlib.Path(__file__).resolve().parent
ROOT = HERE.parent
sys.path.insert(0, str(HERE))
import ste_lint  # noqa: E402

R = ROOT / "evals" / "results" / "rebuild-2026-09-02"
README = (ROOT / "README.md").read_text(encoding="utf-8")
SCEN = {s["id"]: s for s in json.loads((HERE / "scenarios.json").read_text())}
problems = []


def expect(label, text, pattern, value):
    """The number in the text must equal the recomputed value."""
    m = re.search(pattern, text)
    found = m.group(1) if m else None
    if found != str(value):
        problems.append(f"{label}: text says {found!r}, raw files give {value!r}")


def reply_stats(files):
    rows = [ste_lint.reader_check(pathlib.Path(f).read_text(encoding="utf-8")) for f in files]
    n = len(rows)
    c = lambda k: sum(r["counts"][k] for r in rows)  # noqa: E731
    return {
        "n": n,
        "words": round(sum(r["words"] for r in rows) / n),
        "sentences": round(sum(r["counts"]["sentences"] for r in rows) / n, 1),
        "em": c("em_dash"), "bold": c("bold_spans"), "headers": c("headers"), "bullets": c("bullets"),
        "visible": sum(r["visible_total"] for r in rows),
    }


def replies():
    out = {}
    for cond in ("baseline", "v2", "v3b"):
        files = sorted(glob.glob(str(R / "reply1" / f"{cond}__*.txt")) + glob.glob(str(R / "reply2" / f"{cond}__*.txt")))
        out[cond] = reply_stats(files)
    return out


def judge():
    w = t = l = 0
    for f in sorted(glob.glob(str(R / "judge" / "judge-v2-v3b-r*.json"))):
        s = json.loads(pathlib.Path(f).read_text())["summary"]
        w += s["plain_wins"]; t += s["ties"]; l += s["plain_losses"]
    return w, t, l


def gpt():
    return {c: reply_stats(sorted(glob.glob(str(R / "gpt-4.1-mini-reply" / f"{c}__*.txt")))) for c in ("baseline", "v3b")}


def docs():
    out = {}
    for cond in ("baseline", "v13", "v2", "v3b"):
        v = w = 0
        for f in sorted(glob.glob(str(R / "docs" / f"{cond}__*.txt"))):
            sid = pathlib.Path(f).stem.split("__")[1]
            r = ste_lint.lint(pathlib.Path(f).read_text(encoding="utf-8"), SCEN[sid]["type"])
            v += r["violations_total"]; w += r["words"]
        out[cond] = 100 * v / w
    return out


def linter_headline():
    data = json.loads((ROOT / "evals" / "results" / "results.json").read_text())
    models = data["models"]
    mean = sum(m["reduction_pct"] for m in models) / len(models)
    gens = len(glob.glob(str(ROOT / "evals" / "results" / "raw" / "*__baseline__*.json"))) + len(glob.glob(str(ROOT / "evals" / "results" / "raw" / "*__skill__*.json")))
    return round(mean, 1), len(models), gens


def rule_block(text):
    """The text between the first two --- lines, or the body after the frontmatter."""
    parts = re.split(r"^---[ \t]*$", text, flags=re.M)
    return parts[1].strip() if len(parts) >= 3 else text.strip()


def sync():
    prompt = rule_block((ROOT / "prompts" / "system-prompt.md").read_text(encoding="utf-8"))
    style = (ROOT / "output-styles" / "simple-english.md").read_text(encoding="utf-8")
    style = re.sub(r"^---\n.*?\n---\n", "", style, count=1, flags=re.S).strip()
    if prompt != style:
        problems.append("rule block differs between prompts/system-prompt.md and output-styles/simple-english.md")
    skill = (ROOT / "skills" / "simple-english" / "SKILL.md").read_text(encoding="utf-8")
    for phrase in ("Answer in prose", "No em-dashes", "No contractions", "first sentence gives the answer",
                   "Condition before command", "make sure that", "Never touch"):
        for name, text in (("SKILL.md", skill), ("prompts/system-prompt.md", prompt)):
            if phrase.lower() not in text.lower():
                problems.append(f"{name} lacks the rule phrase {phrase!r}")


def versions():
    v = {}
    v["SKILL.md"] = re.search(r'version: "([^"]+)"', (ROOT / "skills/simple-english/SKILL.md").read_text()).group(1)
    for f in (".claude-plugin/plugin.json", ".claude-plugin/marketplace.json", ".codex-plugin/plugin.json"):
        v[f] = re.search(r'"version":\s*"([^"]+)"', (ROOT / f).read_text()).group(1)
    v["README badge"] = re.search(r"badge/version-([0-9.]+)-", README).group(1)
    if len(set(v.values())) != 1:
        problems.append(f"version strings differ: {v}")


def main():
    show = "--print" in sys.argv
    rp, (jw, jt, jl), g, d, (mean, nmodels, gens) = replies(), judge(), gpt(), docs(), linter_headline()
    base, best = rp["baseline"]["visible"], rp["v3b"]["visible"]
    pct = round(100 * (base - best) / base)
    if show:
        print("replies:", json.dumps(rp, indent=1))
        print("judge v3b vs v2:", jw, jt, jl)
        print("gpt:", json.dumps(g, indent=1))
        print("docs:", {k: round(x, 2) for k, x in d.items()})
        print("linter headline:", mean, nmodels, gens, "visible", base, best, pct)
    # README, Benchmarks section
    expect("README reply headline %", README, r"\*\*(\d+)% fewer visible defects", pct)
    expect("README pooled defects", README, r"\((\d+ → \d+)\)", f"{base} → {best}")
    expect("README judge", README, r"in (\d+ of 16) pairs", f"{jw} of 16")
    reply_section = README[README.index("Replies,"):README.index("Documents,")]
    docs_section = README[README.index("Documents,"):README.index("## The rules")]
    for cond, label in (("baseline", "no skill"), ("v2", "2.0.0"), ("v3b", "2.0.1")):
        s = rp[cond]
        expect(f"README reply row {cond}", reply_section,
               rf"\| {label} \| (\d+ \| [\d.]+ \| \d+ \| \d+ \| \d+ \| \d+) \|",
               f"{s['words']} | {s['sentences']} | {s['em']} | {s['bold']} | {s['headers']} | {s['bullets']}")
    expect("README gpt baseline", README, r"went from ([\d.]+ sentences, \d+ bold spans, and \d+ bullets)",
           f"{g['baseline']['sentences']:g} sentences, {g['baseline']['bold']} bold spans, and {g['baseline']['bullets']} bullets")
    expect("README gpt v3b", README, r"to ([\d.]+ sentences and zero formatting)",
           f"{g['v3b']['sentences']} sentences and zero formatting")
    for cond, label in (("baseline", "no skill"), ("v13", "1.3.0"), ("v2", "2.0.0"), ("v3b", "2.0.1")):
        red = "" if cond == "baseline" else f" {round(100 * (d['baseline'] - d[cond]) / d['baseline'])}%"
        expect(f"README docs row {cond}", docs_section, rf"\| {label} \| ([\d.]+ \|[^|\n]*?) ?\|", f"{d[cond]:.2f} |{red}")
    expect("README linter headline", README, r"(\d+\.\d+)% fewer linter violations", mean)
    expect("README linter models", README, r"across (\d+) Claude models", nmodels)
    expect("README linter generations", README, r"\((\d+) generations", gens)
    # rebuild RESULTS.md
    results = (R / "RESULTS.md").read_text(encoding="utf-8")
    expect("RESULTS pooled", results, r"baseline (\d+), 2\.0\.0 \d+, 2\.0\.1 \(v3b\) \d+", base)
    expect("RESULTS pooled best", results, r"2\.0\.1 \(v3b\) (\d+)\.", best)
    sync()
    versions()
    if problems:
        print("MISMATCH")
        for p in problems:
            print(" -", p)
        return 1
    print("check_numbers OK: every published number matches the raw files")
    return 0


if __name__ == "__main__":
    sys.exit(main())

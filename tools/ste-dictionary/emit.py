#!/usr/bin/env python3
"""Emit the compressed word lists from dict.json."""
import json
import re
import pathlib
import sys

OUT = pathlib.Path(sys.argv[1] if len(sys.argv) > 1 else ".")
d = json.load(open("dict.json"))

CLEAN = re.compile(r"^[A-Za-z][A-Za-z'\-]*( [A-Za-z'\-]+){0,3}$")


def dedupe(rows, key):
    """Keep one row per key. Prefer the row that carries alternatives."""
    best = {}
    for r in rows:
        k = key(r)
        if k not in best or (r.get("alt") and not best[k].get("alt")):
            best[k] = r
    return [best[k] for k in sorted(best, key=lambda x: (x[0].lower(), x[1]))]


swaps = [e for e in d["not_approved"] if CLEAN.match(e["word"]) and len(e["word"]) < 25]
swaps = dedupe(swaps, lambda e: (e["word"], e["pos"]))
approved = [e for e in d["approved"] if CLEAN.match(e["word"].replace(" ", "x"))]
approved = dedupe(approved, lambda e: (e["word"], e["pos"]))

with open(OUT / "not-approved.tsv", "w") as f:
    for e in swaps:
        f.write(f"{e['word']}\t{e['pos']}\t{', '.join(e['alt'])}\n")

with open(OUT / "approved.txt", "w") as f:
    for e in approved:
        # Headword and part of speech only. The approved meaning is parsed but
        # dropped on purpose: the file is an index, not a copy of the dictionary.
        f.write(f"{e['word']} ({e['pos']})\n")

print(f"not-approved.tsv: {len(swaps)} rows")
print(f"approved.txt: {len(approved)} rows")

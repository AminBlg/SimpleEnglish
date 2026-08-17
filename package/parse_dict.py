#!/usr/bin/env python3
"""Parse Part 2 of the ASD-STE100 Issue 9 text dump into a compact word list.

Keeps column 1 (word + part of speech) and column 2 (approved meaning or
approved alternatives). Drops columns 3 and 4 (the examples), which hold most
of the bytes.
"""
import json
import re
import sys

SRC = sys.argv[1] if len(sys.argv) > 1 else "ste9.txt"
START = 6165  # first line of the dictionary body (page 2-1-A1)

FURNITURE = re.compile(
    r"^\s*(Issue 9\s|Page 2-|2025-01-15|ASD.STE100 Simplified|Blank Page)"
)
HEADER = re.compile(r"\(part of speech\)|Approved meaning/|^\s*Word\s*$|ALTERNATIVES|STE EXAMPLE")
POS = r"(?:n|v|adj|adv|prep|pron|conj|art|det|num|interj|TN|TV|pref)"
HEAD = re.compile(rf"^(\S.*?)\s*\(({POS}(?:,\s*{POS})*)\)[,.]?\s*$")
BARE_POS = re.compile(rf"^\({POS}(?:,\s*{POS})*\)[,.]?$")
BARE_WORD = re.compile(r"^[A-Za-z][A-Za-z0-9'\- ]{0,30}$")
ALT = re.compile(rf"\b([A-Z][A-Z0-9]*(?:[ '\-/][A-Z0-9]+)*)\s*\(({POS}(?:,\s*{POS})*)\)")

lines = open(SRC, encoding="utf-8", errors="replace").read().splitlines()[START:]

col2, col3 = 19, 45
entries, cur, buf, pending = [], None, "", []

for ln in lines:
    if FURNITURE.match(ln) or not ln.strip():
        continue
    if HEADER.search(ln):  # in-page table header: reread the column offsets
        i = ln.find("ALTERNATIVES")
        if i >= 0:
            col2 = i
        j = ln.find("STE EXAMPLE")
        if j >= 0 and "Non-STE" not in ln[max(0, j - 5):j]:
            col3 = j
        continue
    left, mid = ln[:col2].rstrip(), ln[col2:col3].strip()
    if left:
        # A headword can wrap: "ACCIDENTAL" on one line, "(adj)" on the next.
        cand = f"{buf} {left.strip()}".strip() if BARE_POS.match(left.strip()) else left.strip()
        m = HEAD.match(cand)
        if m:
            # Column 2 text on the first line of a wrapped headword belongs to
            # the new entry, not to the entry above it.
            cur = {"word": m.group(1).strip(), "pos": m.group(2), "c2": pending}
            entries.append(cur)
            buf, pending = "", []
        else:
            buf = cand if BARE_WORD.match(cand) else ""
            pending = []
    if mid:
        if buf:
            pending.append(mid)
        elif cur is not None:
            cur["c2"].append(mid)

approved, swaps = [], []
for e in entries:
    text = re.sub(r"\s+", " ", " ".join(e["c2"])).strip()
    head, _, tail = text.partition("For other meanings, use:")
    alts = [f"{m.group(1)} ({m.group(2)})" for m in ALT.finditer(tail or "")]
    if e["word"].isupper():
        approved.append({"word": e["word"], "pos": e["pos"],
                         "meaning": head.strip(" ."), "alt": alts})
    else:
        alts = [f"{m.group(1)} ({m.group(2)})" for m in ALT.finditer(text)]
        swaps.append({"word": e["word"], "pos": e["pos"], "alt": alts})

print(f"entries={len(entries)} approved={len(approved)} not_approved={len(swaps)}",
      file=sys.stderr)
json.dump({"approved": approved, "not_approved": swaps},
          open("dict.json", "w"), indent=0)

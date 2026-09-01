#!/usr/bin/env python3
"""Count words that are not approved in ASD-STE100, in a text.

`ste_lint.py` measures the mechanical writing rules. It does not look at word
choice. This tool covers the other half: it reads `not-approved.tsv` and reports
each word in the text that the standard does not approve, with the approved
alternatives.

It also reads `slop.tsv` and reports LLM-tell words as a separate count. These
are the high-consensus terms (8 or more independent published ban lists) that
the STE dictionary does not rule on. The two counts do not overlap: a word in
both lexicons counts as a dictionary hit only.

Known ceiling: the match is on the base form and on simple inflections
(-s, -es, -ed, -ing, -ly). It does not do part-of-speech disambiguation, so a
word that is not approved as a verb but approved as a noun gives a false hit.
Code blocks, code spans, URLs, and headings are removed before the count.
Numbers from this tool compare two texts run through the same version. They are
not a compliance verdict.

Usage:
  python3 ste_dict_lint.py file.md
  cat text.md | python3 ste_dict_lint.py -
  python3 ste_dict_lint.py --self-test
"""
import json
import pathlib
import re
import sys

HERE = pathlib.Path(__file__).resolve().parent
TSV = HERE / "not-approved.tsv"
SLOP_TSV = HERE / "slop.tsv"


def approved_words(path=HERE / "approved.txt"):
    """Base forms of every approved word, lowercase."""
    return {re.sub(r"\s*\(.*", "", ln).strip().lower()
            for ln in path.read_text(encoding="utf-8").splitlines() if ln.strip()}


def load(path=TSV):
    """Return ({surface form: 'headword -> ALTERNATIVES'}, [(phrase regex, entry)]).

    An entry is dropped when the same spelling is approved as another part of
    speech. "use" is not approved as a noun but "USE (v)" is approved, and this
    tool cannot tell the two apart. Dropping the entry loses recall and removes
    a large number of false hits.
    """
    table, phrases = {}, []
    ok = approved_words()
    for line in path.read_text(encoding="utf-8").splitlines():
        if not line.strip():
            continue
        word, pos, alts = (line.split("\t") + ["", ""])[:3]
        word = word.strip().lower()
        if not word or word in ok:
            continue
        entry = f"{word} ({pos}) -> {alts}"
        if " " in word:
            phrases.append((re.compile(r"\b" + r"\s+".join(map(re.escape, word.split())) + r"\b",
                                       re.I), entry))
        else:
            for form in forms(word):
                if form not in ok:  # "approved" is the past participle of an
                    table.setdefault(form, entry)  # unapproved verb, and approved
    return table, phrases


def load_slop(path=SLOP_TSV):
    """Same shapes as load(), from the LLM-tell lexicon.

    Columns: term, count of independent ban lists that name it, replacement.
    Terms that the STE dictionary already rules on are not in this file.
    """
    table, phrases = {}, []
    if not path.exists():
        return table, phrases
    for line in path.read_text(encoding="utf-8").splitlines():
        if not line.strip():
            continue
        word, count, alt = (line.split("\t") + ["", ""])[:3]
        word = word.strip().lower()
        entry = f"{word} ({count} lists) -> {alt}"
        if " " in word:
            phrases.append((re.compile(r"\b" + r"\s+".join(map(re.escape, word.split())) + r"\b",
                                       re.I), entry))
        else:
            for form in forms(word):
                table.setdefault(form, entry)
    return table, phrases


def forms(word):
    """Base form plus the regular inflections that a writer produces."""
    out = {word}
    if word.endswith("y") and len(word) > 2:
        out |= {word[:-1] + "ies", word[:-1] + "ied"}
    elif word.endswith(("s", "x", "z", "ch", "sh")):
        out.add(word + "es")
    else:
        out.add(word + "s")
    if word.endswith("e"):
        out |= {word + "d", word[:-1] + "ing"}
    else:
        out |= {word + "ed", word + "ing"}
    out.add(word + "ly")
    return out


# Rule 1.5 permits a technical noun that is not in the dictionary. These are the
# technical nouns of software documentation that the raw count flags most often.
# The residual count removes them. Extend the set for another subject field.
TECHNICAL_NOUNS = {
    "run", "runs", "file", "files", "port", "ports", "request", "requests",
    "stage", "stages", "process", "processes", "transfer", "log", "logs",
    "backup", "settings", "load", "progress", "design", "key", "list", "form",
    "record", "records", "table", "tables",
}


def strip_code(text):
    text = re.sub(r"```.*?```", " ", text, flags=re.S)
    text = re.sub(r"`[^`\n]+`", " ", text)
    text = re.sub(r"https?://\S+", " ", text)
    text = re.sub(r"^#+\s.*$", " ", text, flags=re.M)
    return text


def lint(text, table=None, slop=None):
    table, phrases = load() if table is None else table
    slop_table, slop_phrases = load_slop() if slop is None else slop
    body = strip_code(text)
    words = re.findall(r"[A-Za-z][A-Za-z'\-]*", body)
    hits, slop_hits = [], []
    for w in words:
        entry = table.get(w.lower())
        if entry:
            hits.append({"used": w, "entry": entry})
        elif (s := slop_table.get(w.lower())):  # dictionary wins on overlap
            slop_hits.append({"used": w, "entry": s})
    for rx, entry in phrases:
        for m in rx.finditer(body):
            hits.append({"used": m.group(0), "entry": entry})
    for rx, entry in slop_phrases:
        for m in rx.finditer(body):
            slop_hits.append({"used": m.group(0), "entry": entry})
    n = max(len(words), 1)
    residual = [h for h in hits if h["used"].lower() not in TECHNICAL_NOUNS]
    return {
        "words": len(words),
        "not_approved": len(hits),
        "not_approved_per_100w": round(100 * len(hits) / n, 2),
        "residual": len(residual),
        "residual_per_100w": round(100 * len(residual) / n, 2),
        "slop": len(slop_hits),
        "slop_per_100w": round(100 * len(slop_hits) / n, 2),
        "hits": hits,
        "slop_hits": slop_hits,
    }


def self_test():
    table = ({f: "x" for f in forms("utilize")},
             [(re.compile(r"\bprior\s+to\b", re.I), "prior to -> BEFORE (prep)")])
    empty = ({}, [])
    r = lint("Utilize the tool prior to launch. `utilize` stays.", table, empty)
    assert r["not_approved"] == 2, r
    assert r["words"] == 7, r  # the code span is removed before the count
    r2 = lint("Use the tool before launch.", table, empty)
    assert r2["not_approved"] == 0, r2
    # slop lexicon: separate count, dictionary wins on overlap
    slop = load_slop()
    r3 = lint("We delve into the robust landscape in order to deliver.", table, slop)
    assert r3["slop"] == 4, r3  # delve, robust, landscape, "in order to"
    assert r3["not_approved"] == 0, r3
    both = ({f: "x" for f in forms("delve")}, [])
    r4 = lint("Delve deeper.", both, slop)
    assert r4["not_approved"] == 1 and r4["slop"] == 0, r4
    print("self-test ok")


if __name__ == "__main__":
    if "--self-test" in sys.argv:
        self_test()
    else:
        src = sys.argv[1] if len(sys.argv) > 1 else "-"
        text = sys.stdin.read() if src == "-" else pathlib.Path(src).read_text()
        print(json.dumps(lint(text), indent=2))

#!/usr/bin/env python3
"""Deterministic ASD-STE100 violation counter for benchmark runs.

Counts mechanical violations that a regex can catch: sentence length,
contractions, banned modals, perfect tenses, "-ing" clauses, semicolons,
em-dashes, Latin abbreviations, slop words, trailing conditions, synonym
rotation.

Known ceiling: this is a regex pass, not a grammar parser. It undercounts
(no passive-voice detection, no part-of-speech checks) and it can miscount
sentence bounds in unusual markdown. Numbers from this tool are comparable
between two texts run through the same version; they are not a compliance
verdict. No tool can guarantee STE compliance.

Usage:
  python3 ste_lint.py --type procedural file.md
  cat text.md | python3 ste_lint.py --type descriptive -
  python3 ste_lint.py --self-test
"""
import json
import pathlib
import re
import sys

BANNED_MODALS = re.compile(r"\b(should|would|may|might|could)\b", re.I)
PERFECT = re.compile(r"\b(has|have|had)\s+been\b|\b(has|have)\s+\w+ed\b", re.I)
CONTRACTION = re.compile(r"\b\w+(n't|'ll|'re|'ve|'d)\b|\bit's\b|\byou're\b", re.I)
ING_CLAUSE = re.compile(r",\s*(mak|allow|enabl|ensur|highlight|creat|provid|offer|help|reduc|improv|lead|caus|result)ing\b", re.I)
LATIN = re.compile(r"\b(e\.g\.|i\.e\.|etc\.?)(?=[\s,)]|$)", re.I)
FIRST_PERSON = re.compile(r"\b(i|me|my|myself|we|us|our|ours|ourselves)\b", re.I)
CONVERSATIONAL = re.compile(r"\b(hello|hi|(?<!\bmake\s)(?<!\bmakes\s)(?<!\bmade\s)sure|certainly|of\s+course|happy\s+to|gladly|apologiz\w*|sorry|please|kindly|hope\s+this\s+helps|feel\s+free|let\s+me\s+know)\b", re.I)
SELF_REF = re.compile(r"\b(as\s+an\s+ai|this\s+model|the\s+assistant|my\s+opinion|my\s+thought)\b", re.I)
SLOP_CORE = re.compile(
    r"\b(simply|seamlessly|effortlessly|robust|leverag\w*|utiliz\w*|"
    r"comprehensive|powerful|blazingly|streamlin\w*|facilitat\w*|"
    r"performant|plethora|myriad|delve|crucial|pivotal)\b", re.I)
SLOP_TSV = pathlib.Path(__file__).resolve().parent / "slop.tsv"


def slop_pattern():
    """Union of the measured core list and evals/slop.tsv (term, count, swap).

    The TSV is the 69-term LLM-tell lexicon: words named by 8 or more of 122
    published ban lists. Falls back to the core list when the file is absent.
    """
    terms = []
    if SLOP_TSV.exists():
        for line in SLOP_TSV.read_text(encoding="utf-8").splitlines():
            term = line.split("\t")[0].strip().lower()
            if term:
                terms.append(re.escape(term).replace(r"\ ", r"\s+") + r"\w*")
    if not terms:
        return SLOP_CORE
    return re.compile(SLOP_CORE.pattern[:-len(r")\b")] + "|" + "|".join(terms) + r")\b", re.I)


SLOP = slop_pattern()
# Linear scan; lint() checks ">= 4 chars before the match" instead of the old
# prefix pattern, whose backtracking was quadratic on long sentences
# (a punctuation-free 8,000-word input took ~7s; now sub-millisecond).
TRAILING_COND = re.compile(r"\s(if|when)\s", re.I)
DASH = re.compile(r"—|(?<!\d)–(?!\d)|(?<= )--(?= )|(?<=[^\s\d]{2}) - (?=[^\s\d]{2})")
ROTATION_SETS = [
    ("check-verify", re.compile(r"\b(check|verify|confirm|validate|ensure)\w*\b", re.I)),
    ("config-settings", re.compile(r"\b(config|configuration|settings)\b", re.I)),
]
LIMITS = {"procedural": 20, "descriptive": 25}


def strip_code(text):
    text = re.sub(r"```.*?```", " ", text, flags=re.S)
    text = re.sub(r"`[^`\n]+`", " CODESPAN ", text)  # one word per Rule 8.6
    text = re.sub(r"^#+\s.*$", " ", text, flags=re.M)  # headings exempt (titles, 8.6)
    text = re.sub(r"https?://\S+", " URL ", text)
    return text


def sentences(text):
    text = re.sub(r"^\s*([-*]|\d+\.)\s+", "", text, flags=re.M)  # list markers
    parts = re.split(r"(?<=[.!?:])\s+", text)
    return [p.strip() for p in parts if len(p.strip().split()) >= 2]


def lint(text, text_type):
    body = strip_code(text)
    sents = sentences(body)
    limit = LIMITS[text_type]
    counts = {}
    lengths = [len(s.split()) for s in sents]
    counts["sentence_over_limit"] = sum(1 for n in lengths if n > limit)
    counts["contraction"] = len(CONTRACTION.findall(body))
    counts["banned_modal"] = len(BANNED_MODALS.findall(body))
    counts["perfect_tense"] = len([m for m in PERFECT.finditer(body)])
    counts["ing_clause"] = len(ING_CLAUSE.findall(body))
    counts["semicolon"] = body.count(";")
    counts["em_dash"] = len(DASH.findall(body))
    counts["latin_abbrev"] = len(LATIN.findall(body))
    counts["slop_word"] = len(SLOP.findall(body))
    counts["first_person"] = len(FIRST_PERSON.findall(body))
    counts["conversational"] = len(CONVERSATIONAL.findall(body))
    counts["self_ref"] = len(SELF_REF.findall(body))

    def trailing_cond(s):
        m = TRAILING_COND.search(s)
        if not m:
            return False
        # The whitespace before "if" may be a newline (a wrapped sentence), but
        # the 4-char prefix must sit on the same line as that whitespace. A
        # heading, a blank line, then "If ..." is condition-first, not trailing.
        line_start = s.rfind("\n", 0, m.start()) + 1
        return m.start() - line_start >= 4 and not re.match(r"^(if|when)\b", s, re.I)

    counts["trailing_condition"] = sum(1 for s in sents if trailing_cond(s))
    rotation = 0
    for _, rx in ROTATION_SETS:
        stems = {m.group(1).lower().rstrip("s") for m in rx.finditer(body)}
        if len(stems) > 1:
            rotation += len(stems) - 1
    counts["synonym_rotation"] = rotation
    words = max(1, len(body.split()))
    total = sum(counts.values())
    return {
        "type": text_type,
        "words": words,
        "sentences": len(sents),
        "mean_sentence_words": round(sum(lengths) / max(1, len(lengths)), 1),
        "longest_sentence_words": max(lengths, default=0),
        "violations": counts,
        "violations_total": total,
        "violations_per_100w": round(100.0 * total / words, 2),
    }


SLOP_FIXTURE = """Leveraging our robust retry mechanism, failed uploads are automatically
reattempted, ensuring data integrity is maintained throughout the entire process which has
been designed from the ground up to gracefully handle even the most challenging network
interruptions. You should verify your credentials; it's also worth checking the settings,
e.g. the timeout config. Contact support if the problem persists. Please note that as an AI, this model is happy to help."""

CLEAN_FIXTURE = """The system retries a failed upload automatically. This process keeps the data correct.

If failures continue, make sure that your credentials are correct. If the problem continues, contact support."""

# Only the first three dashes must be flagged as logic junctions.
DASH_FIXTURE = """The deploy failed — the disk was full.
The upload failed -- the token expired.
The retry failed - the port was closed.
Do not use --force against production.
The window is 5 - 10 minutes.
The range is 5–10 minutes, over the 2024–2025 season.
Write x - y = z on the board.
Use the `--config sqlpipe.yaml` flag.
Remove the panel:
   -   Loosen the four bolts.
"""


def self_test():
    slop = lint(SLOP_FIXTURE, "procedural")
    clean = lint(CLEAN_FIXTURE, "procedural")
    dashes = lint(DASH_FIXTURE, "procedural")
    assert slop["violations"]["sentence_over_limit"] >= 1, slop
    assert slop["violations"]["banned_modal"] >= 1, slop
    assert slop["violations"]["contraction"] >= 1, slop
    assert slop["violations"]["perfect_tense"] >= 1, slop
    assert slop["violations"]["ing_clause"] >= 1, slop
    assert slop["violations"]["semicolon"] == 1, slop
    assert slop["violations"]["latin_abbrev"] >= 1, slop
    assert slop["violations"]["slop_word"] >= 2, slop
    assert slop["violations"]["trailing_condition"] >= 1, slop
    assert slop["violations"]["synonym_rotation"] >= 1, slop
    assert slop["violations"]["first_person"] >= 1, slop
    assert slop["violations"]["conversational"] >= 1, slop
    assert slop["violations"]["self_ref"] >= 1, slop
    assert clean["violations_total"] == 0, clean
    assert lint("We delve into the landscape.", "descriptive")["violations"]["slop_word"] == 2
    assert dashes["violations"]["em_dash"] == 3, dashes
    print("self-test OK:", slop["violations_total"], "violations in slop fixture, 0 in clean")


USAGE = "usage: ste_lint.py [--type procedural|descriptive] [--gate] (FILE|-) | --self-test"


def main():
    args = sys.argv[1:]
    if "--self-test" in args:
        self_test()
        return 0
    gate = "--gate" in args
    if gate:
        args.remove("--gate")
    text_type = "descriptive"
    if "--type" in args:
        i = args.index("--type")
        if i + 1 >= len(args):
            sys.exit("missing value after --type\n" + USAGE)
        text_type = args[i + 1]
        del args[i:i + 2]
    if text_type not in LIMITS:
        sys.exit("unknown --type %r (expected procedural or descriptive)\n%s" % (text_type, USAGE))
    if len(args) != 1:
        sys.exit(USAGE)
    src = args[0]
    if src == "-":
        text = sys.stdin.read()
    else:
        try:
            with open(src, encoding="utf-8") as fh:
                text = fh.read()
        except OSError as err:
            sys.exit(str(err))
    report = lint(text, text_type)
    print(json.dumps(report, indent=2))
    return 1 if gate and report["violations_total"] else 0


if __name__ == "__main__":
    sys.exit(main())

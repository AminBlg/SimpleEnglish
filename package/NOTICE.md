# NOTICE

## Source

The rules and the word lists in this directory come from ASD-STE100 Issue 9,
dated 2025-01-15.

ASD (AeroSpace and Defence Industries Association of Europe) publishes the
standard. The Simplified Technical English Maintenance Group (STEMG) writes and
maintains it. All rights in ASD-STE100 stay with ASD.

- The standard: <https://www.asd-ste100.org/>
- Free download: <https://www.asd-ste100.org/request.html>

## What these files contain

| File | Content | Source |
|---|---|---|
| `ste-core.md` | The 53 writing rules, in different words. The rule numbers match the standard. | Part 1 |
| `approved.txt` | 841 rows, 770 headwords with the part of speech. No definitions. | Part 2, column 1 |
| `not-approved.tsv` | 1,297 rows, 1,238 headwords with the part of speech and the approved alternatives. | Part 2, columns 1 and 2 |

`parse_dict.py` and `emit.py` made the two word lists from the text of the PDF.

`not-approved.tsv` keeps column 1 and column 2. `approved.txt` keeps column 1
only, because `emit.py` drops the approved meaning on purpose. Both files drop
column 3 and column 4, which hold the example sentences. Those two columns hold
most of the bytes of Part 2.

A row is one word with one part of speech. A word with two parts of speech gets
two rows, so the row count is larger than the word count.

## What these files are not

These files are not the standard and they are not a substitute for it. They hold
no example sentences, no counter-examples, no explanatory text, and no general
recommendations. `approved.txt` holds no meanings.

The extraction is lossy. This package lists 770 approved words where the
standard states 875. It lists 1,238 words that are not approved where the
standard states 1,274. 80 rows carry no alternative, because the parser lost the
text of that column.

The standard is the only authority for a word-level ruling. A writer who needs
an authoritative ruling reads the standard.

## License

The MIT license of this repository covers `parse_dict.py`, `emit.py`,
`bench_core.py`, `ste_dict_lint.py`, `ste-core.md`, and the prose of this
directory. The MIT license does not extend to the content of ASD-STE100.

The word lists are here as a derived index, for study and for research into
prompt compression.

This is an unofficial project. ASD and STEMG do not endorse it and have no
connection with it. ASD-STE100 is a registered trademark of ASD.

ASD or STEMG can ask for a change or a removal through an issue at
<https://github.com/AminBlg/SimpleEnglish/issues>. The maintainer answers.

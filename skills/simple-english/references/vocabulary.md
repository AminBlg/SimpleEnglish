# Vocabulary discipline

## How the STE dictionary works

The official dictionary (Part 2 of the standard) has about 900 approved words and about 1,200 unapproved words with approved alternatives.
It is copyrighted by ASD and is not reproduced here. The standard is a free download at asd-ste100.org — get it for authoritative word rulings.

The mechanics, which you can apply without the dictionary:

- **One word, one meaning, one part of speech.** Every approved word has exactly one approved meaning and one grammatical role.
- Each dictionary entry gives: the word and part of speech, the approved meaning (or the approved alternative if the word is banned), one STE example, one non-STE example.
- Words in uppercase are approved; words in lowercase are not and point to alternatives.
- **Technical nouns and technical verbs are exempt** (Rules 1.5, 1.12). Your domain vocabulary — "webhook", "idempotent", "rebase", "mutex" — is legal when your project or industry uses it officially.

Known part-of-speech rulings, useful as patterns:

| Word | Ruling |
|---|---|
| can, will, must | Approved modals. "could" is rejected even for possibility. |
| should, would, may, might | Not approved. |
| test | Noun only — "do a test", not "test the pump". |
| check | Noun only. |
| oil | Noun only — "the oil is dirty", not "oil the valve". |
| help | Verb only — "with the aid of", not "with the help of". |
| work | Noun only — "do work with", not "work with". |
| fall | "To move down by gravity" only — never "decrease". |
| follow | "To come after" only — never "obey". Write "obey the instructions". |
| above, below | Physical positions only — for limits write "more than", "less than". |

## The modal ladder

| You wrote | STE writes |
|---|---|
| should (requirement) | must |
| should (recommendation) | Delete it, or state it as fact: "X is better because Y." |
| may / might / could (possibility) | can |
| may (permission) | can |
| would (hypothetical) | Restructure: "If X occurs, Y occurs." |

## Slop-to-simple substitution table

This table is ours, not the ASD dictionary. It maps the words AI-generated docs overuse to plain replacements.
One rule: if the word carries no fact, delete it instead of replacing it.

| Slop | Write instead |
|---|---|
| leverage, utilize | use |
| in order to | to |
| prior to | before |
| subsequently | then, after |
| ensure | make sure that |
| it is worth noting that, note that | (delete, or "NOTE:") |
| it's important to, crucially | (delete — state the fact) |
| simply, just, easily | (delete) |
| seamlessly, effortlessly | (delete) |
| robust, powerful, comprehensive | (delete, or give the measurable property) |
| performant | fast (give the number) |
| leverage the power of | use |
| a wide range of, a variety of | (name them, or "many") |
| functionality | function, feature |
| enables you to, allows you to | you can |
| is designed to | (delete — say what it does) |
| aims to, strives to | (delete — say what it does) |
| facilitate | help, make possible |
| utilize best practices | (name the practice) |
| dive into, delve into | read, examine |
| keep in mind that | remember that, or (delete) |
| when it comes to | for |
| in the event that | if |
| due to the fact that | because |
| at this point in time | now |
| going forward | (delete) |
| please note | (delete) |
| feel free to | you can |
| as needed, as necessary | (state the condition) |
| and/or | Pick one, or write "X, or Y, or both" |
| etc. | (name the items, or "and more") |
| e.g. | for example |
| i.e. | that is |
| via | with, through |
| upon | on, after |
| whilst, amongst | while, among |
| in terms of | for, about |
| gracefully handles | (say what it does: "retries three times, then stops") |
| out of the box | by default |
| under the hood | internally |
| state-of-the-art, cutting-edge | (delete) |
| seamless integration with | works with |
| battle-tested | (give the evidence) |
| blazingly fast | fast (give the number) |
| rich (features, ecosystem) | (delete, or count them) |
| empower | (delete — say what the user can do) |
| streamline | make simpler, make faster |
| game-changer, revolutionize | (delete) |
| holistic, synergy | (delete) |
| plethora, myriad | many |
| paradigm | model, pattern |
| addresses the issue | corrects the fault, removes the error |
| tackles | corrects, solves |
| handles X scenarios | (say which scenarios and what it does) |

## Consistency pass

After substitution, do the Rule 1.11 / 9.4 pass: one term per concept for the whole document.

Common rotations to collapse:

- check / verify / confirm / validate / ensure → pick one
- config / configuration / settings / options → pick one
- delete / remove / drop / destroy → pick one per meaning (delete data, remove a file — keep the split consistent)
- error / issue / problem / failure → "error" for errors, "failure" for failed operations
- run / execute / invoke / launch → pick one
- show / display / render / present → pick one

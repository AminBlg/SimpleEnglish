---
type: llm
focus: last_message
---
The output is a customer-facing incident note. The summary gave exactly these facts: start 2026-09-14 09:12 UTC; end 09:47 UTC the same day; cause: a deploy of the billing service made every invoice request fail with HTTP 500; impact: 1,240 accounts could not open invoices in that window, no data lost; fix: the deploy was rolled back at 09:47 UTC. Check these claims and fail if any one is false:

1. All five facts appear: start time, end time, cause, impact with the count 1,240 and the no-data-loss statement, and the rollback fix.
2. No other number, time, component name, percentage, root-cause detail, or customer count appears. Restating the window as "35 minutes" is allowed because it follows from the given times.
3. No promise about the future appears: nothing like "we will make sure this never happens again", "we are committed to", "we are adding safeguards", "going forward".
4. The note gives the customer no instruction, because the summary gives none.
5. The note names no actor that the summary does not name. "The deploy was rolled back" passes. "Our engineering team rolled back the deploy" or "The on-call engineer" fails.
6. The output adds no definition or explanation of a term that the source or the prompt did not define. "Parquet is a file format", "A role is a database account", "A DSN is a string that tells a program how to connect", and "A rollback returns the service to its previous version" are added definitions and fail. A conditional branch that the source does not contain ("If you are an administrator...") also fails.

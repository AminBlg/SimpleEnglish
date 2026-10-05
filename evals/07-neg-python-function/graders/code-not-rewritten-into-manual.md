---
type: llm
focus: last_message
---
The output is a Python function that parses ISO 8601 date strings plus one test. Check these claims and fail if any one is false:

1. The function parses "2026-09-14T09:12:00+00:00" correctly, for example with `datetime.fromisoformat` or `dateutil`, and returns a datetime. Manual string slicing that drops the timezone fails.
2. A test exists that calls the function and asserts on the result.
3. The code is not degraded by writing rules: identifiers are normal Python names, docstrings and comments (if any) are ordinary, and the code is not padded with explanatory prose inside the block.
4. Any prose outside the code block is shorter than the code block.

---
type: llm
focus: last_message
---
The output is a commit message. The prompt states exactly these facts: Queue.pop() in queue.py returned None on an empty queue; callers then crashed with AttributeError; Queue.pop() now raises QueueEmpty; worker.py callers catch QueueEmpty and sleep for the existing poll_interval. Check these claims and fail if any one is false:

1. Every statement is in the list above or follows directly from it. A claim about tests, performance, other callers, a ticket, a version, an upgrade note, or a reason that the prompt does not give is an added fact and fails.
2. The message has an imperative subject line and a body that says what changed and why. The why is the crash with AttributeError.
3. Every sentence in the body is complete, with a verb and its articles. A body made of fragments ("Raise QueueEmpty. Catch in worker.") fails.
4. The body does not say that the change is breaking or risky, because the prompt does not.

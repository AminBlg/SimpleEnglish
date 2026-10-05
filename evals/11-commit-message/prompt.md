---
max_turns: 8
timeout_seconds: 180
allowed_tools: [Read, Glob, Grep, Skill]
model: sonnet
runs: 3
---
Write the commit message for this change. Reply with the message only.

In queue.py, Queue.pop() returned None when the queue was empty, so callers crashed later with AttributeError. It now raises QueueEmpty. The callers in worker.py catch QueueEmpty and sleep for the existing poll_interval.

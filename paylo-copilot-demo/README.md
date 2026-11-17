# paylio-copilot-demo — Session 4, live demo (slide 10)

The repo contains the spec and the data. The prototype folder does not exist yet: Claude Code builds it live.

## The prompt (paste as is)

```
Read spec.md and build exactly the prototype it describes, in prototype/, nothing more.
Then run python prototype/evals.py and show me the numbers against the definition of done (spec §8).
If the number is below the criterion, do not change the prompt or the retrieval: list the misses grouped by cause and propose the change to spec.md.
```

## Expected result (template drafter, no API key)
routing accuracy 0.88 · hit@3 1.00 · **sendable as is 8/20 = 40 %** (criterion 45 %) · drafts on human-only 0 · policy blocks 0.
Misses: 9 × "Release notes 4.12" (section missing from the KB), 3 × escalated just under the 0.70 threshold (one French ticket).
Proposal the agent should make: add release notes 4.12 to KB-214 (and re-chunk by heading), handle non-English tickets (translate or escalate), add synonyms / better chunk titles.

`_backup_run/` holds a complete build and its eval output, in case the live run fails or diverges.

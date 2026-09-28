# Experiment 01 — three levels of autonomy, one task

Task: `Add GET /stats?expr=... that returns min, max and mean of the expression's total.
Mean must be exact for expressions without keep; for keep expressions estimate it from 20 000 seeded rolls.`

Run the task three times from the same commit (`git stash` / `git checkout .` between runs),
each with a different permission profile in `docs/experiments/profiles/`:

```bash
OPENCODE_CONFIG=docs/experiments/profiles/strict.json   opencode   # everything asks
OPENCODE_CONFIG=docs/experiments/profiles/balanced.json opencode   # reads allowed, writes and unknown bash ask
OPENCODE_CONFIG=docs/experiments/profiles/auto.json     opencode   # everything allowed except deny-list
```

Tally while it runs (a tick per event):

| Profile | Prompts shown to you | Prompts you declined | Steps to green tests | Wall time | Tokens (from /status or session) | Tests green? | Anything you would not have allowed? |
|---|---|---|---|---|---|---|---|
| strict | | | | | | | |
| balanced | | | | | | | |
| auto | | | | | | | |

Write three sentences: which profile you would use for (a) an unfamiliar repo, (b) this repo,
(c) a throw-away prototype — and why the answer differs.

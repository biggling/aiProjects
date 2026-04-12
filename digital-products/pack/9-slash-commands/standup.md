---
description: Generate a daily standup summary from git log and continue.md
allowed-tools: Bash, Read
---

# /standup — Daily Standup Generator

Generate a concise daily standup from git history and current project state.

## Step 1: Get yesterday's work
Run: `git log --oneline --since="yesterday 06:00" --until="now" --author="$(git config user.name)"`

If it's Monday, use `--since="friday 06:00"` instead.

## Step 2: Check current state
Read `continue.md` if it exists. Note the current phase and any blockers.

## Step 3: Check for open issues or PRs
Run: `git status --short` to see any uncommitted work in progress.

## Step 4: Generate standup

Use this format:

```
## Daily Standup — [date]

### Yesterday
- [concise summary of each commit — not just the commit message, explain the actual work]

### Today
- [next 1-3 tasks from continue.md or the logical next steps]

### Blockers
- [any blockers, or "None"]
```

Keep it brief. Each bullet should be one sentence. Skip technical details — this is for team communication, not a code review.

If $ARGUMENTS contains a project name, filter to that project's commits only.

$ARGUMENTS

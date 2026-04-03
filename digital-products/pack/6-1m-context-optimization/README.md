# 1M Context Optimization

## The Problem

Claude Code's 1M token context window sounds unlimited. It isn't.

Every session, tokens are silently burned on:
- Claude re-reading files it already processed
- Repetitive tool call results (full file contents loaded again and again)
- Verbose reasoning when you only need the answer
- CLAUDE.md instructions that are too long and full of examples

By the middle of a session, your context is half full of things Claude already knows.
Toward the end, Claude starts truncating or forgetting earlier context.

## What's In This Folder

| File | What it does |
|---|---|
| `context-trim.md` | CLAUDE.md snippets that reduce token waste |
| `summarize-hook.sh` | Post-session hook: auto-summarizes session → appends to activeContext.md |
| `token-budget-statusline.md` | How to display real-time token usage in the Claude Code statusline |

---

## Quick Wins (do these first)

### 1. Add context-trim instructions to your CLAUDE.md

Copy the relevant sections from `context-trim.md` into your project's `CLAUDE.md`.
These instructions tell Claude to be concise, skip known patterns, and not re-read files unnecessarily.

### 2. Keep CLAUDE.md under 150 lines

Long CLAUDE.md files are loaded every turn. Every 100 lines ≈ 1,000 tokens × N turns.
Strip examples, keep rules. Examples belong in a separate `examples/` directory.

### 3. Use Memory OS for persistent context

The Memory OS files (folder 2) are loaded once at session start.
They're far more token-efficient than Claude re-discovering context through file exploration.

### 4. Use `--bare` for CI/cron sessions

`claude --bare --print "..."` skips hooks, LSP, plugin sync, skill walks.
Saves ~5,000 tokens per session on overhead. Use in `crontab.conf`.

### 5. Watch your token usage in real time

See `token-budget-statusline.md` for how to display the rate-limit counter in your statusline.
Visible feedback helps you catch sessions that are burning context unnecessarily.

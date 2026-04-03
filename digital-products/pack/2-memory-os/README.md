# Memory OS — Keep Claude's Context Alive Across Sessions

## The Problem

Claude Code starts every session with zero memory of your project. You spend 10–20 minutes re-explaining:
- What this codebase does
- What you were working on
- What decisions you've made
- What the current blocker is

By the time Claude is up to speed, you've burned a third of your session.

## The Solution

Memory OS is four markdown files that Claude reads at the start of every session. They give Claude full context in under 60 seconds.

You update them. Claude uses them. Context never rots.

---

## Setup (one-time, 2 minutes)

```bash
bash setup-memory-os.sh
```

This creates `memory-bank/` in your project with all four files pre-populated.

Then add this block to your project's `CLAUDE.md`:

```markdown
## Memory OS
At session start: read ALL files in memory-bank/ before doing anything else.
At session end: update memory-bank/activeContext.md and memory-bank/progress.md with what changed.
Never truncate existing content — append only. Keep each file under 200 lines.
```

---

## The Four Files

### `projectBrief.md` — written once, rarely changes
What the project is, the stack, the constraints, the non-negotiables.
Claude uses this to understand the shape of the system before touching any code.

### `activeContext.md` — updated every session
What you're working on right now. Recent decisions. Current thinking.
This is the "brain dump" file — messy is fine, current is essential.

### `progress.md` — running changelog
What's done, what's in progress, what's blocked, what's next.
Think of it as a permanent sprint board that never gets wiped.

### `systemPatterns.md` — grows over time
Architecture decisions, naming conventions, gotchas discovered, patterns that work.
When Claude makes a mistake and you correct it, add the correction here so it never happens again.

---

## Session Workflow

**Start of session:**
Claude reads all four files → has full context → starts work immediately, no re-explanation needed.

**During session:**
Claude makes decisions → architecture choices go in `systemPatterns.md`, progress in `progress.md`.

**End of session:**
Claude updates `activeContext.md` with what changed and `progress.md` with completed/next tasks.

---

## Token Impact

Each file is kept under 200 lines (~2,000 tokens). All four files together: ~8,000 tokens.
With 1M context window, this is less than 1% of available context.

You save far more than 8,000 tokens by not re-explaining your architecture every session.

---

## Tips

- Be ruthless about keeping files current. Stale context is worse than no context.
- Put the most important things first in each file — Claude reads top-down.
- When you correct Claude on something, add the rule to `systemPatterns.md` immediately.
- If a file goes stale, reset it rather than leaving wrong info in it.

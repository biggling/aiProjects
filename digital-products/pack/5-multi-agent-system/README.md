# Multi-Agent System

## What This Is

A set of shell scripts that run Claude Code non-interactively on a schedule.
Research happens in the morning. Work happens in the evening. You check results.

No babysitting. No staying up to run tasks. Claude works while you sleep.

---

## Scripts

| Script | What it does |
|---|---|
| `run-research.sh <project>` | Web research agent: reads AGENT.md brief, searches, saves findings |
| `run-agent.sh <project> [prompt]` | Work agent: runs a custom prompt non-interactively |
| `run-agent-continue.sh <project> [hint]` | Context-aware work: inlines continue.md + latest research into turn 0 |
| `run-now.sh <cmd> <project>` | Shorthand dispatcher for all scripts |
| `weekly-summary.sh` | Reads all continue.md files, generates cross-project digest |
| `crontab.conf` | Ready-to-install cron schedule |

---

## Quick Start

```bash
# 1. Copy scripts to your workspace root
cp 5-multi-agent-system/*.sh /your/workspace/scripts/
cp 5-multi-agent-system/crontab.conf /your/workspace/scripts/
chmod +x /your/workspace/scripts/*.sh

# 2. Run research for a project
./scripts/run-research.sh my-project

# 3. Run work agent (picks up from continue.md automatically)
./scripts/run-agent-continue.sh my-project

# 4. Run with a specific focus
./scripts/run-agent-continue.sh my-project "focus on fixing the login bug"

# 5. Install the cron schedule
crontab scripts/crontab.conf
```

---

## Research Agent (run-research.sh)

Reads `<project>/research/AGENT.md` for its search brief, runs web searches,
and saves findings to `<project>/research/findings/YYYY-MM-DD.md` and `latest.md`.

Your `research/AGENT.md` should contain:
- What to research (competitors, market trends, technical docs)
- What questions to answer
- What to save in the findings file

---

## Work Agent (run-agent-continue.sh)

The smart version of run-agent. Before calling Claude, it inlines:
- `<project>/continue.md` — full content
- `<project>/research/findings/latest.md` — capped at 4,000 chars

Claude gets full context at turn 0. No wasted turns reading files.

---

## continue.md Daily Tasks Pattern

Add a `## Daily Tasks` section to your continue.md.
The work agent always runs these first, then moves to one-time next steps.

```markdown
## Daily Tasks  (reset each session — do not mark [x])
- [ ] Check research/findings/latest.md for new action items
- [ ] Run health check: python scripts/health_check.py
- [ ] Review any open errors in data/logs/

## Current Phase
Phase 2 — Active

## Next Actions
- [ ] Build the export feature
- [x] Fix the import bug
```

---

## Cron Schedule

Install with: `crontab scripts/crontab.conf`

Default schedule:
- 08:00 daily: research agent on all projects
- 20:00 daily: work agent on priority 1–3 projects
- 07:00 Sunday: weekly summary

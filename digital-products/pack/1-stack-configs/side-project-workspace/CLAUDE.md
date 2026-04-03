# CLAUDE.md — Side Project Workspace

## What This Is
A multi-project workspace for one engineer running several side projects in parallel.
Each subdirectory is an independent project. This root CLAUDE.md sets workspace-level conventions.

## Workspace Structure
```
workspace/
├── CLAUDE.md               ← this file (workspace rules)
├── STATUS.md               ← cross-project status board (update when phase changes)
├── scripts/                ← automation scripts (run-agent, run-research, crontab)
├── project-a/              ← highest priority
│   ├── CLAUDE.md           ← project-specific rules
│   └── continue.md         ← session state (always read before starting)
├── project-b/
│   ├── CLAUDE.md
│   └── continue.md
└── ...
```

## Rules for Every Project
- **Always** read `continue.md` before starting work in a project
- **Always** update `continue.md` before ending a session
- Ship fast, iterate later — time is limited
- Make decisions autonomously unless the task involves money or live accounts
- Write production code, not prototypes

## continue.md Pattern

Every project's `continue.md` follows this structure:

```markdown
# Project Name — Continue

## Daily Tasks  (reset each session — do not mark [x])
- [ ] <task that runs every session>

## Current Phase
Phase N — short description — STATUS

## Next Actions
- [ ] specific next task
- [x] completed task

## Blockers
_None_ or describe blocker

## Notes
- context the agent needs
```

The `## Daily Tasks` section runs first every session. Do not permanently check these off — they repeat. One-time tasks get checked `[x]` when done.

## Multi-Agent Automation

Run Claude Code non-interactively on a schedule:

```bash
# Research agent (morning) — reads AGENT.md, searches web, saves findings
./scripts/run-research.sh project-a

# Work agent (evening) — inlines continue.md + latest research, does next task
./scripts/run-agent-continue.sh project-a

# Custom task
./scripts/run-agent.sh project-a "specific prompt here"

# All projects in priority order
./scripts/run-agent-continue.sh all

# Check status of all projects
./scripts/run-now.sh status
```

Cron schedule (install with `crontab crontab.conf`):
- 08:00 daily: research agent runs on all projects
- 20:00 daily: work agent runs on priority 1–3 projects
- 07:00 Sunday: weekly summary across all projects

## STATUS.md Format

Keep this updated when a project changes phase:

```markdown
| # | Project | Phase | Status | Next Step |
|---|---------|-------|--------|-----------|
| 1 | project-a | Phase 2 | Active | Build X feature |
| 2 | project-b | Phase 1 | Blocked | Need API key |
```

## Priority Rules
- Work on highest-priority project first
- Don't context-switch mid-task unless blocked
- If blocked on priority 1, work on priority 2 — log the blocker in continue.md

## Decision Framework
Work autonomously on:
- Code changes, bug fixes, new features
- File creation, deletion, refactoring
- Running tests, fixing test failures
- Updating documentation

Ask the human before:
- Spending money or adding paid services
- Deploying to production
- Deleting data or databases
- Changing billing or external accounts

## Notes
- Free tools only until revenue justifies paid
- Update STATUS.md when project phase or status changes
- Each project has its own CLAUDE.md for stack-specific rules

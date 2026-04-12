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

## Session Start Checklist
Every time you start work in this workspace, do these in order:
1. Read `STATUS.md` — know the current state of every project before touching any code
2. `cd` into the highest-priority non-blocked project
3. Read that project's `continue.md` — understand exactly where you left off
4. Read `research/findings/latest.md` if it exists — new data may change priorities
5. Start on `## Next Actions` item 1 — don't invent new work

## Git Workflow (Multi-Project)
- Each project is a subdirectory of the workspace repo
- Commit changes per project: `git add project-a/` and commit with `[project-a]` prefix
- Never mix changes from two projects in one commit
- Branch per feature when the feature will take >1 session: `project-a/feature-name`

## When to Escalate vs Proceed
Proceed autonomously:
- Any code change, refactor, test, or bug fix
- Adding dependencies (document in continue.md what was added and why)
- Creating new files, folders, scripts
- Running CI/tests locally

Escalate to the human:
- Any paid API key, subscription, or cloud resource
- Production deployments or database migrations
- Changing authentication, billing, or access-control logic
- Deleting more than a single file

## Common Mistakes Claude Makes Without This Config
- Starting work on a lower-priority project when the higher one is unblocked
- Skipping `continue.md` and re-deriving context from scratch (wastes context tokens)
- Making decisions that require money without flagging them
- Mixing commits across projects
- Updating `continue.md` with vague notes instead of specific next actions

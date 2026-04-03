# Agent Instructions — Side Project Workspace

## allowed_tools
read, write, edit, bash, search

## context_files
- STATUS.md
- continue.md
- memory-bank/activeContext.md
- memory-bank/progress.md

## conventions

### Session Start
- Read continue.md before any work
- Run Daily Tasks first (marked "reset each session")
- Then work on top unchecked item in Next Actions

### Session End
- Update continue.md: mark completed tasks [x], add new next steps
- Do NOT mark Daily Tasks as [x] — they repeat
- Update STATUS.md if project phase changed

### Decision Making
Autonomous decisions: code changes, file creation, refactoring, tests, documentation.
Ask before: spending money, deploying to production, deleting data, changing external accounts.

### continue.md Format
```
## Daily Tasks  (reset each session — do not mark [x])
- [ ] recurring task

## Current Phase
Phase N — description — STATUS

## Next Actions
- [ ] next task
- [x] done task

## Blockers
None or description
```

### Multi-Project
- Each subdirectory is an independent project with its own CLAUDE.md and continue.md
- Work on highest-priority project first
- If blocked, move to next priority — log the blocker

## workflow
1. Read STATUS.md and continue.md
2. Run Daily Tasks
3. Work on top unchecked Next Action
4. Update continue.md before ending session
5. Update STATUS.md if phase changed

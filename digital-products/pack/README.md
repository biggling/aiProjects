# Claude Code Elite Pack

**CLAUDE.md instructions get ignored after 2-5 prompts. This solves it.**

The only Claude Code config pack built hooks-first — deterministic enforcement that Claude
cannot bypass, plus stack-specific configs, Memory OS, and an autonomous agent runner.

---

## The Core Problem (and Why This Pack Is Different)

CLAUDE.md is loaded every turn, but Claude ignores instructions after a few prompts. This is the
**#1 filed GitHub bug** (issues #668, #7777, #19635, #23032). One user documented 14+ violations
in a single session. Most packs add more CLAUDE.md text. That doesn't work.

This pack uses **hooks for enforcement** and CLAUDE.md for conventions:

- `rm -rf` outside `/tmp` → **blocked** (hook — can't be bypassed)
- Bad commit format → **blocked** (hook — can't be bypassed)
- File written → **auto-formatted** (hook — runs even if Claude "forgets")
- Naming convention → CLAUDE.md (guidance — enforced by your code review)

---

## What's Included

| Folder | Contents | Tier |
|---|---|---|
| `1-stack-configs/` | 12 CLAUDE.md files — Go, TypeScript, Next.js, Rust, Java Spring Boot, Python FastAPI, Python Data Pipeline, Kotlin Android, React Native, Flutter/Dart, Godot 4, workspace | Starter+ |
| `2-memory-os/` | 5 memory templates + setup script — Claude remembers everything across sessions | Pro+ |
| `3-auto-mode-profiles/` | 4 settings.json profiles — conservative / standard / trusted-dev / CI | Pro+ |
| `4-hooks/` | 10 hooks — safety blockers + auto-format + linter + Telegram notify + context loader | Pro+ |
| `5-multi-agent-system/` | run-agent.sh, run-research.sh, crontab.conf — Claude works while you sleep | Starter+ |
| `6-1m-context-optimization/` | Context trim snippets, hidden features guide, token statusline | Elite |
| `7-cross-platform/` | AGENTS.md for OpenCode/Cursor (Linux Foundation standard) | Elite |
| `8-notion-dashboard/` | Side Project Dashboard Notion template | Elite |
| `9-slash-commands/` | 7 commands: /review, /commit, /standup, /test-coverage, /security-scan, /refactor | Elite |
| `EFFECTIVENESS-TEST.md` | Test suite to verify your CLAUDE.md is actually being followed | All tiers |

---

## Your Tier

- **Starter ($19):** Folders `1`, `5`, and `EFFECTIVENESS-TEST.md`
- **Pro ($37):** Everything in Starter + `2`, `3`, `4`
- **Elite ($97):** All folders

---

## Quick Start (10 minutes)

```bash
# 1. Pick your stack config
cp 1-stack-configs/go-microservices/CLAUDE.md /your/project/CLAUDE.md

# 2. Install safety hooks (prevents rm -rf and force-push — always do this)
mkdir -p ~/.claude/hooks/pre-tool-call ~/.claude/hooks/post-tool-call ~/.claude/hooks/session-start
cp 4-hooks/pre-tool-call/block-rm-rf.sh ~/.claude/hooks/pre-tool-call/
cp 4-hooks/pre-tool-call/block-force-push.sh ~/.claude/hooks/pre-tool-call/
cp 4-hooks/session-start/load-context.sh ~/.claude/hooks/session-start/
chmod +x ~/.claude/hooks/**/*.sh

# 3. Set up Memory OS (so Claude remembers your project across sessions)
cd /your/project
bash /path/to/pack/2-memory-os/setup-memory-os.sh

# 4. Install the cron agent
mkdir -p /your/workspace/scripts
cp 5-multi-agent-system/*.sh /your/workspace/scripts/
chmod +x /your/workspace/scripts/*.sh
crontab 5-multi-agent-system/crontab.conf

# 5. Verify your config works
# Read EFFECTIVENESS-TEST.md — run the 6 tests to confirm Claude follows your conventions
```

See `SETUP.md` for full step-by-step, including hooks JSON registration.
See `EXAMPLES.md` for before/after examples for every stack.
See `EFFECTIVENESS-TEST.md` to verify your CLAUDE.md is actually being followed.

---

## Key Files

| File | What it does |
|---|---|
| `1-stack-configs/<stack>/CLAUDE.md` | Drop into project root — Claude knows your conventions |
| `EFFECTIVENESS-TEST.md` | 6-test suite — verify Claude follows your config |
| `2-memory-os/setup-memory-os.sh` | Run once — creates 5-file memory bank in your project |
| `2-memory-os/CLAUDE-decisions.md` | Architecture decisions log — Claude won't re-propose rejected approaches |
| `3-auto-mode-profiles/standard/settings.json` | Safe daily-driver Auto Mode config |
| `4-hooks/pre-tool-call/block-rm-rf.sh` | Hard-blocks `rm -rf` outside /tmp — cannot be bypassed |
| `4-hooks/pre-tool-call/enforce-commit-format.sh` | Enforces Conventional Commits — cannot be bypassed |
| `4-hooks/post-tool-call/auto-format.sh` | Auto-formats every file write (gofmt, prettier, black, rustfmt) |
| `4-hooks/post-tool-call/run-linter.sh` | Runs linter after edits, feeds results back to Claude |
| `5-multi-agent-system/run-agent-continue.sh` | Smart agent: inlines context + latest research at turn 0 |
| `5-multi-agent-system/crontab.conf` | Install to run research at 8am, work at 8pm |
| `6-1m-context-optimization/hidden-features.md` | Features most devs discover after 6+ months |
| `6-1m-context-optimization/context-trim.md` | CLAUDE.md snippets that cut token waste |
| `9-slash-commands/review.md` | /review — structured pre-push code review |
| `9-slash-commands/security-scan.md` | /security-scan — OWASP Top 10 check on changed files |

---

## Why Hooks Beat More CLAUDE.md Text

| Approach | Reliability | Why |
|---|---|---|
| CLAUDE.md instruction | Degrades after 2-5 prompts | Loaded each turn but treated as soft guidance |
| Slash command | Reliable when you invoke it | You explicitly trigger it — can't be "forgotten" |
| Hook | Always executes | Runs outside Claude's control — exit 1 blocks the action |

Move your most critical rules to hooks. Keep CLAUDE.md under 60 lines of conventions.
Use slash commands for structured workflows you want to run deliberately.

---

## Questions or Issues

Reply to your purchase receipt — I respond within 24 hours.
All buyers get free lifetime updates.

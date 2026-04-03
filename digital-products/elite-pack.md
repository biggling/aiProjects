# Claude Code Elite Pack — Product Structure

## Tiers

| Tier | Price | Target |
|---|---|---|
| Starter | $19 | Solo dev who wants drop-in stack configs + agent scripts |
| Pro | $37 | Dev who wants Memory OS + Auto Mode safety + hooks |
| Elite | $97 | Team lead or power user who wants everything + cross-platform + Notion |

---

## Complete File Structure

```
claude-code-elite-pack/
├── README.md
├── SETUP.md
│
├── 1-stack-configs/
│   ├── go-microservices/CLAUDE.md
│   ├── typescript-node/CLAUDE.md
│   ├── python-data-pipeline/CLAUDE.md
│   ├── python-fastapi-react/CLAUDE.md
│   ├── kotlin-android/CLAUDE.md
│   ├── gdscript-godot4/CLAUDE.md
│   └── side-project-workspace/CLAUDE.md
│
├── 2-memory-os/
│   ├── README.md
│   ├── projectBrief.md
│   ├── activeContext.md
│   ├── progress.md
│   ├── systemPatterns.md
│   └── setup-memory-os.sh
│
├── 3-auto-mode-profiles/
│   ├── README.md
│   ├── conservative/settings.json
│   ├── standard/settings.json
│   ├── trusted-dev/settings.json
│   └── ci-scripted/settings.json
│
├── 4-hooks/
│   ├── README.md
│   ├── pre-tool-call/block-rm-rf.sh
│   ├── pre-tool-call/block-force-push.sh
│   ├── pre-tool-call/log-tool-calls.sh
│   ├── post-tool-call/notify-telegram.sh
│   ├── session-start/print-status.sh
│   └── session-start/load-context.sh
│
├── 5-multi-agent-system/
│   ├── README.md
│   ├── run-agent.sh
│   ├── run-research.sh
│   ├── run-agent-continue.sh
│   ├── run-now.sh
│   ├── weekly-summary.sh
│   ├── crontab.conf
│   └── continue.md.template
│
├── 6-1m-context-optimization/
│   ├── README.md
│   ├── context-trim.md
│   ├── summarize-hook.sh
│   └── token-budget-statusline.md
│
├── 7-cross-platform/
│   ├── README.md
│   ├── go-microservices/AGENTS.md
│   ├── typescript-node/AGENTS.md
│   ├── python-data-pipeline/AGENTS.md
│   └── side-project-workspace/AGENTS.md
│
└── 8-notion-dashboard/
    ├── README.md
    ├── template-link.txt
    └── screenshots/
```

---

## File-by-File Build Guide

### 1-stack-configs/

Each `CLAUDE.md` encodes real engineering conventions for that stack. Generic names and project refs removed — buyer drops the file into their project root.

| File | Key conventions encoded |
|---|---|
| `go-microservices/CLAUDE.md` | Error wrapping with `fmt.Errorf`, no `panic()` in library code, `loguru`→`slog`, `pathlib`→`filepath`, interface-first design, table-driven tests |
| `typescript-node/CLAUDE.md` | Strict mode, ESM imports, `zod` for runtime validation, no `any`, MCP SDK patterns, Hono router conventions |
| `python-data-pipeline/CLAUDE.md` | SQLAlchemy 2.x sessions, Alembic migrations, Celery task patterns, `loguru`, `pathlib.Path` everywhere, never raw strings for paths |
| `python-fastapi-react/CLAUDE.md` | `asyncio.to_thread()` for sync DB calls, React Query hooks, WebSocket `ConnectionManager` singleton, `VITE_` env vars |
| `kotlin-android/CLAUDE.md` | Compose + ViewModel + StateFlow, Room DAO patterns, Hilt DI, AdMob integration, coroutines scope rules |
| `gdscript-godot4/CLAUDE.md` | Node/scene structure, signal-first communication, `_ready()` vs `_process()` rules, resource preloading, no `get_node()` in loops |
| `side-project-workspace/CLAUDE.md` | Multi-project workspace, `continue.md` pattern, research agent pattern, crontab automation structure |

---

### 2-memory-os/

The Memory Bank pattern — Claude maintains project context across sessions by writing to structured files. Eliminates context rot.

| File | Purpose |
|---|---|
| `projectBrief.md` | Static: project goal, stack, constraints, non-negotiables. Written once. |
| `activeContext.md` | Dynamic: what's in progress right now, recent decisions, current blockers. Updated each session. |
| `progress.md` | Done / in-progress / blocked / next. Running changelog. |
| `systemPatterns.md` | Architecture decisions, naming conventions, gotchas discovered. Grows over time. |
| `setup-memory-os.sh` | Creates `memory-bank/` dir + all 4 files pre-populated with prompts for the buyer. One-shot setup. |

CLAUDE.md addition that activates Memory OS:
```
## Memory OS
At session start: read memory-bank/*.md — do not skip.
At session end: update memory-bank/activeContext.md and memory-bank/progress.md.
Never truncate existing content — append only.
```

---

### 3-auto-mode-profiles/

`.claude/settings.json` controls what Claude Code can do in Auto Mode without asking. Four profiles for different risk tolerances.

| Profile | Allows | Blocks |
|---|---|---|
| `conservative` | Read, Glob, Grep only | All writes, all bash |
| `standard` | Read, Write, Edit, Glob, Grep, safe bash (npm, pip, pytest) | git push, rm, curl to external |
| `trusted-dev` | Everything standard + git add/commit, npm run build | git push --force, rm -rf, production deploy cmds |
| `ci-scripted` | Full tool access, designed for `--bare` cron runs | Interactive prompts |

---

### 4-hooks/

Shell scripts wired into Claude Code's lifecycle events.

| Hook | Event | What it does |
|---|---|---|
| `block-rm-rf.sh` | PreToolCall (Bash) | Exits 1 if command contains `rm -rf` outside `/tmp` |
| `block-force-push.sh` | PreToolCall (Bash) | Exits 1 if command contains `push --force` or `push -f` |
| `log-tool-calls.sh` | PreToolCall | Appends `timestamp \| tool \| input` to `~/.claude/tool-calls.log` |
| `notify-telegram.sh` | PostToolCall | Sends Telegram message on tool completion (optional, needs BOT_TOKEN) |
| `print-status.sh` | SessionStart | Prints `git branch`, `git status --short`, last 3 commits |
| `load-context.sh` | SessionStart | Cats `continue.md` + `research/findings/latest.md` to stdout so Claude sees them in turn 0 |

Install pattern (add to `.claude/settings.json`):
```json
{
  "hooks": {
    "PreToolCall": [{"matcher": "Bash", "hooks": [{"type": "command", "command": "bash ~/.claude/hooks/pre-tool-call/block-rm-rf.sh"}]}],
    "SessionStart": [{"hooks": [{"type": "command", "command": "bash ~/.claude/hooks/session-start/print-status.sh"}]}]
  }
}
```

---

### 5-multi-agent-system/

The full autonomous agent runner system. Drop into any project root.

| Script | Purpose |
|---|---|
| `run-agent.sh <project> [prompt]` | Runs a non-interactive Claude Code session with custom prompt |
| `run-research.sh <project\|all>` | Web research agent → saves `research/findings/YYYY-MM-DD.md` + `latest.md` |
| `run-agent-continue.sh <project> [hint]` | Inlines `continue.md` + `latest.md` into prompt — agent has full context turn 0 |
| `run-now.sh <research\|continue\|status> <project>` | Shorthand dispatcher |
| `weekly-summary.sh` | Reads all `continue.md` files → generates cross-project weekly digest |
| `crontab.conf` | Ready-to-install cron: research at 08:00, work at 20:00, summary Sunday |
| `continue.md.template` | Standard template with Daily Tasks + One-Time Next Steps sections |

---

### 6-1m-context-optimization/

Patterns to reduce token burn and get more out of the 1M context window.

| File | Contents |
|---|---|
| `README.md` | What causes context bloat, how Claude reads CLAUDE.md, token budget mental model |
| `context-trim.md` | CLAUDE.md snippets that instruct Claude to be concise, skip boilerplate, not re-explain known patterns |
| `summarize-hook.sh` | PostSession hook: summarizes last session's changes → appends 3-line summary to `activeContext.md` |
| `token-budget-statusline.md` | How to configure the rate-limit statusline field (Claude Code v2.1.86+) for visible token feedback |

---

### 7-cross-platform/

AGENTS.md files for OpenCode (120K GitHub stars, 5M users/month). Same conventions as CLAUDE.md but in OpenCode's format. Low build effort, expands TAM significantly.

Format differences from CLAUDE.md:
- Uses `## Agent Instructions` header instead of free-form
- `allowed_tools` field for tool restrictions
- `context_files` list for auto-loading

---

### 8-notion-dashboard/

Side Project Tracker Notion template. Duplicate link + setup README. Includes:
- Kanban board: all projects by status
- Timeline view: milestones per project
- Revenue tracker: targets vs actuals
- Weekly focus view: top 3 tasks this week
- Research log: findings per project with date

---

## What's in Each Tier

### Starter ($19) — includes folders 1 + 5
- 7 stack-specific CLAUDE.md configs
- Full multi-agent script system (run-agent, run-research, crontab)
- continue.md template
- README + SETUP

### Pro ($37) — includes everything in Starter + folders 2 + 3 + 4
- Memory OS (4 templates + setup script)
- Auto Mode safety profiles (4 profiles)
- Hooks library (6 hooks)

### Elite ($97) — includes everything in Pro + folders 6 + 7 + 8
- 1M context optimization guide + hook
- Cross-platform AGENTS.md (OpenCode/Cursor)
- Notion Side Project Dashboard template

---

## Build Status

| Folder | Status | Est. Build Time |
|---|---|---|
| `1-stack-configs/` | 70% — refactor from existing CLAUDE.md files | 3h |
| `2-memory-os/` | 0% — new build | 3h |
| `3-auto-mode-profiles/` | 0% — new build | 2h |
| `4-hooks/` | 50% — extract from scripts/ | 2h |
| `5-multi-agent-system/` | 90% — exists in scripts/ | 1h |
| `6-1m-context-optimization/` | 0% — new build | 2h |
| `7-cross-platform/` | 0% — new build | 1h |
| `8-notion-dashboard/` | 0% — build in Notion | 3h |
| README + SETUP | 0% — write last | 1h |

**Total: ~18h**

## Ship Order
1. Package folders 1 + 5 → Starter $19 live (Day 1, 4h)
2. Add folders 2 + 3 + 4 → Pro $37 live (Day 2, 7h)
3. Add folders 6 + 7 + 8 → Elite $97 live (Day 3, 7h)

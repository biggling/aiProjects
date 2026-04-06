# scripts/

Agent runner and scheduler for aiProjects. Uses **launchd** (macOS) to fire `scheduler.sh` every **5 minutes**, which reads `schedule.conf` and dispatches jobs.

## Files

| File | Purpose |
|------|---------|
| `schedule.conf` | Active schedule — what runs when |
| `scheduler.sh` | Reads `schedule.conf`, dispatches to runner scripts |
| `run-research.sh` | Research agent — web search + findings saved to `research/findings/` |
| `run-agent.sh` | Work agent — reads `continue.md`, executes next task |
| `run-agent-continue.sh` | Smarter work agent — inlines research findings + `continue.md` into the prompt |
| `run-agent-subdir.sh` | Subdir work agent — like `run-agent.sh` but CWD is set to a subdirectory |
| `run-now.sh` | Manual trigger from terminal |
| `install-launchd.sh` | Install the launchd plist (copies scripts to `~/scripts/`) |
| `uninstall-launchd.sh` | Remove the launchd plist |
| `weekly-summary.sh` | Sunday digest — sends Telegram summary of all projects |

## schedule.conf format

```
# comment lines are ignored
# type      project           HH:MM  [HH:MM ...]
research    mcp-apps          23:00  01:30
work        digital-products  20:00
```

- `type` — which runner to invoke (see [Supported types](#supported-types))
- `project` — directory name under `aiProjects/`; for `subwork`, use `project/subdir` notation
- `ai` — optional: `claude` or `gemini`; overrides `AI_CLI` env var for this entry only
- `hint` — optional, `subwork` only; `@file` or auto-detect (see below)
- `HH:MM` — one or more 24h times (Bangkok, GMT+7); scheduler checks every 5 min

Fields are identified by value — `ai` and `hint` can appear in any order after `project`.

## Supported types

| Type | Runner | What it does |
|------|--------|-------------|
| `research` | `run-research.sh` | Reads `<project>/research/AGENT.md`, web-searches, saves findings to `research/findings/` |
| `work` | `run-agent.sh` | Reads `<project>/continue.md` each turn, executes next priority task |
| `continue` | `run-agent-continue.sh` | Like `work` but inlines research findings into the prompt upfront |
| `subwork` | `run-agent-subdir.sh` | Like `work` but CWD is set to `project/subdir`; supports `@file` and inline prompt hints |

## subwork + ai examples

Fields are identified by value — `ai` and `hint` can appear in any order after `project`.

```
# Default AI (claude), auto-detect instructions
subwork  trade-auto/src          20:00

# Explicit AI per entry
research  digital-products  gemini   23:30
work      mcp-apps          claude   20:00

# subwork with file hint, default AI
subwork  tiktok/modules     @AGENT.md    21:00  01:00
subwork  trade-auto/src     @plan.md     20:00

# subwork with gemini + file hint (any order)
subwork  trade-auto/src     gemini  @plan.md   20:00  02:00
subwork  tiktok/modules     @AGENT.md  gemini  21:00
```

**File resolution order for `@file`:** subdir first, then project root.

**Auto-detect order (no hint):** `subdir/AGENT.md` → `subdir/plan.md` → `project/continue.md`

**AI priority:** per-entry field > `AI_CLI` env var > `.env` file > `claude` (default)

## How to add a new schedule type

Follow these four steps — using a new type `summary` as an example.

### Step 1 — Create the runner script

```bash
# scripts/run-summary.sh
#!/bin/bash
set -euo pipefail
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"
PROJECT="${1:-}"
[[ -z "$PROJECT" ]] && { echo "Usage: $0 <project>"; exit 1; }

# ... your logic here ...
echo "[$(date +'%b %d %H:%M')] Summary: $PROJECT"
```

```bash
chmod +x scripts/run-summary.sh
```

### Step 2 — Add the type to scheduler.sh

Open `scheduler.sh` and add a case branch:

```bash
case "$type" in
  research) bash "$HOME/scripts/run-research.sh" "$project" ;;
  work)     bash "$HOME/scripts/run-agent.sh"    "$project" ;;
  continue) bash "$HOME/scripts/run-agent-continue.sh" "$project" ;;
  summary)  bash "$HOME/scripts/run-summary.sh"  "$project" ;;   # ← add this
  *) echo "[$(date '+%b %d %H:%M')] Unknown type: $type" >> "$LOG" ;;
esac
```

### Step 3 — Re-install launchd so the updated script is copied to `~/scripts/`

```bash
bash scripts/install-launchd.sh
```

> **Why?** launchd runs scripts from `~/scripts/` (a non-iCloud path). `install-launchd.sh` copies the scripts there. If you skip this step, the scheduler runs the old copy.

### Step 4 — Add entries to schedule.conf

```
# format: type  project  HH:MM [HH:MM ...]
summary  mcp-apps  09:00
summary  pod       09:30
```

Changes to `schedule.conf` are picked up immediately — no restart needed.

## Manual triggers

```bash
# Status overview of all projects
./run-now.sh status

# Run a work agent on one project
./run-now.sh mcp-apps
./run-now.sh mcp-apps "Focus on the pricing page"

# Run research
./run-now.sh research mcp-apps
./run-now.sh research all

# Run continue agent (research-aware)
./run-now.sh continue mcp-apps
./run-now.sh continue trade-auto "focus on momentum backtest"

# Run all projects in priority order
./run-now.sh all
```

## Install / uninstall

```bash
# Install (runs every 5 minutes via launchd)
bash scripts/install-launchd.sh

# Verify it's loaded
launchctl list | grep com.big.aiprojects

# Uninstall
bash scripts/uninstall-launchd.sh
```

Logs: `aiProjects/logs/`  
Scheduler log: `logs/scheduler.log`  
Launchd log: `logs/launchd.log`

## Archived

`archived/` holds obsolete scripts kept for reference:

| File | Why archived |
|------|-------------|
| `crontab.conf` | Old crontab-based system, replaced by launchd + `schedule.conf` |
| `test-cron-claude.sh` | Dev test used during initial setup, has broken code |

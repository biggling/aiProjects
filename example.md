# Claude Agent — Usage Examples

## Quick Start: Continue Work on a Project

```bash
# Navigate to project and start Claude
cd tiktok && claude

# Claude reads continue.md automatically via CLAUDE.md rules
# It picks up where the last session left off
```

---

## Giving Claude Tasks

### Continue previous work
```bash
claude "read continue.md and keep working on the next actions"
```

### Add specific tasks
```bash
claude "add these to the next actions in continue.md and start working:
1. Add rate limiting to the API
2. Write tests for the publisher module
3. Fix the thumbnail generator aspect ratio bug"
```

### One-shot task
```bash
claude "fix the bug in src/strategies/grid.py where grid levels overlap when range_pct is too small"
```

### Multi-step task with context
```bash
claude "read plan.md, then:
1. Complete all unchecked [ ] items in Phase 3
2. Mark each [x] as you finish
3. Update continue.md when done"
```

---

## Non-Interactive Mode (for automation / cron)

### Basic: run a task and exit
```bash
claude --print "read continue.md and work on next actions" \
  --allowedTools "Read,Write,Edit,Bash,Glob,Grep" \
  --max-turns 50
```

### With output saved to log
```bash
claude --print "read continue.md and work on next actions" \
  --allowedTools "Read,Write,Edit,Bash,Glob,Grep" \
  --max-turns 50 \
  2>&1 | tee "data/logs/session_$(date +%Y%m%d_%H%M).log"
```

### Dangerously skip all permission prompts (use with caution)
```bash
claude --dangerously-skip-permissions \
  --print "read continue.md and work on the next 3 actions" \
  --max-turns 100
```

---

## Crontab Setup

### Edit crontab
```bash
crontab -e
```

### Example crontab entries

```crontab
# ┌───── minute (0-59)
# │ ┌──── hour (0-23)
# │ │ ┌─── day of month (1-31)
# │ │ │ ┌── month (1-12)
# │ │ │ │ ┌─ day of week (0=Sun, 1=Mon, ..., 6=Sat)
# │ │ │ │ │

# === TikTok pipeline: run daily at 6 AM Bangkok time ===
0 6 * * * cd ~/aiProjects/tiktok && claude --dangerously-skip-permissions --print "run the daily pipeline: research → strategy → scriptgen → voiceover → videogen → editor. Update continue.md when done." --max-turns 100 >> ~/aiProjects/tiktok/data/logs/cron_$(date +\%Y\%m\%d).log 2>&1

# === Trade-auto: run backtests every Monday at 7 AM ===
0 7 * * 1 cd ~/aiProjects/trade-auto && claude --dangerously-skip-permissions --print "download latest OHLCV data and run all backtests. Save results and update continue.md." --max-turns 30 >> ~/aiProjects/trade-auto/data/logs/cron_$(date +\%Y\%m\%d).log 2>&1

# === POD: check analytics daily at 9 PM ===
0 21 * * * cd ~/aiProjects/pod && claude --dangerously-skip-permissions --print "pull latest Etsy analytics, flag underperformers, update continue.md." --max-turns 30 >> ~/aiProjects/pod/data/logs/cron_$(date +\%Y\%m\%d).log 2>&1

# === Polymarket: collect data every 2 hours ===
0 */2 * * * cd ~/aiProjects/polymarket && source venv/bin/activate && python src/collector.py >> ~/aiProjects/polymarket/data/logs/collector.log 2>&1

# === Weekly summary: every Friday at 6 PM ===
0 18 * * 5 cd ~/aiProjects && claude --dangerously-skip-permissions --print "read STATUS.md and each project's continue.md. Write a weekly summary to STATUS.md with progress, blockers, and recommended next steps for the weekend." --max-turns 50 >> ~/aiProjects/weekly_$(date +\%Y\%m\%d).log 2>&1
```

### Verify crontab is saved
```bash
crontab -l
```

---

## Wrapper Script: `scripts/run-agent.sh`

```bash
#!/bin/bash
# Usage: ./scripts/run-agent.sh <project> [prompt]
# Example: ./scripts/run-agent.sh tiktok "fix the scraper fallback data"
# Example: ./scripts/run-agent.sh trade-auto  (uses default: continue work)

set -euo pipefail

PROJECT="${1:?Usage: run-agent.sh <project> [prompt]}"
PROMPT="${2:-read continue.md and work on the next actions. Update continue.md when done.}"
BASE_DIR="$(cd "$(dirname "$0")/.." && pwd)"
PROJECT_DIR="$BASE_DIR/$PROJECT"
LOG_DIR="$PROJECT_DIR/data/logs"

mkdir -p "$LOG_DIR"
LOGFILE="$LOG_DIR/agent_$(date +%Y%m%d_%H%M%S).log"

echo "[$(date)] Starting agent for $PROJECT" | tee "$LOGFILE"
echo "[$(date)] Prompt: $PROMPT" | tee -a "$LOGFILE"

cd "$PROJECT_DIR"
claude --dangerously-skip-permissions \
  --print "$PROMPT" \
  --max-turns 50 \
  2>&1 | tee -a "$LOGFILE"

echo "[$(date)] Agent finished for $PROJECT" | tee -a "$LOGFILE"
```

```bash
# Make executable
chmod +x scripts/run-agent.sh

# Usage examples
./scripts/run-agent.sh tiktok
./scripts/run-agent.sh trade-auto "download new data and rerun backtests"
./scripts/run-agent.sh pod "write tests for the copy generator"
./scripts/run-agent.sh steam-game "implement the reel spinning animation"
```

---

## Wrapper Script: `scripts/run-now.sh`

```bash
#!/bin/bash
# Run all projects that have pending work (reads continue.md for each)
# Usage: ./scripts/run-now.sh

set -euo pipefail
BASE_DIR="$(cd "$(dirname "$0")/.." && pwd)"

PROJECTS=(tiktok trade-auto pod shopee-affiliate amazon-kdp steam-game android-app polymarket)

for project in "${PROJECTS[@]}"; do
  if [ -f "$BASE_DIR/$project/continue.md" ]; then
    echo "=== Starting: $project ==="
    "$BASE_DIR/scripts/run-agent.sh" "$project" &
    sleep 5  # stagger starts
  fi
done

echo "All agents launched. Logs in each project's data/logs/"
wait
echo "All agents complete."
```

---

## Tips

### Check what Claude will do before running
```bash
# Preview mode — just prints the plan, doesn't execute
claude "read continue.md and list what you would do next. Don't make changes."
```

### Limit scope to avoid runaway sessions
```bash
# --max-turns limits how many tool calls Claude can make
claude --print "..." --max-turns 20   # small task
claude --print "..." --max-turns 50   # medium task
claude --print "..." --max-turns 100  # large task (full pipeline run)
```

### Run multiple projects in parallel
```bash
# Terminal 1
cd tiktok && claude "work on Phase 11 testing"

# Terminal 2
cd trade-auto && claude "optimize the momentum strategy parameters"

# Terminal 3
cd pod && claude "run tests and fix any failures"
```

### Pass a file as the prompt
```bash
# Write detailed instructions to a file, then pass it
claude "$(cat tasks-for-today.txt)"
```

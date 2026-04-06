#!/bin/bash
# ============================================================
# aiProjects Scheduler
# Reads schedule.conf and dispatches jobs at the right time.
# Runs via launchd at every :00 and :30 of every hour.
# ============================================================

if [[ -z "${PROJECT_ROOT:-}" ]]; then
  SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
  PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"
fi

CONF="$PROJECT_ROOT/scripts/schedule.conf"
LOG="$PROJECT_ROOT/logs/scheduler.log"
CURRENT_TIME=$(date +"%H:%M")

mkdir -p "$(dirname "$LOG")"

while IFS= read -r line; do
  [[ "$line" =~ ^[[:space:]]*# ]] && continue
  [[ -z "${line//[[:space:]]/}" ]] && continue

  type=$(awk '{print $1}' <<< "$line")
  project=$(awk '{print $2}' <<< "$line")
  times=$(awk '{for(i=3;i<=NF;i++) print $i}' <<< "$line")

  for t in $times; do
    if [[ "$t" == "$CURRENT_TIME" ]]; then
      echo "[$(date '+%b %d %H:%M')] Dispatching: $type $project" >> "$LOG"
      case "$type" in
        research) bash "$HOME/scripts/run-research.sh"      "$project" ;;
        work)     bash "$HOME/scripts/run-agent.sh"         "$project" ;;
        continue) bash "$HOME/scripts/run-agent-continue.sh" "$project" ;;
        subwork)  bash "$HOME/scripts/run-agent-subdir.sh"  "$project" ;;
        *) echo "[$(date '+%b %d %H:%M')] Unknown type: $type" >> "$LOG" ;;
      esac
      break
    fi
  done
done < "$CONF"

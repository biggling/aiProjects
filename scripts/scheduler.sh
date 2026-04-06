#!/bin/bash
# ============================================================
# aiProjects Scheduler
# Reads schedule.conf and dispatches jobs at the right time.
# Runs via launchd every 5 minutes, scheduler dispatches jobs
# based on scripts/schedule.conf
#
# schedule.conf format:
#   type  project  [hint]  HH:MM [HH:MM ...]
#
#   hint (optional, subwork only):
#     @plan.md        — read this file from the subdir as the prompt
#     "inline prompt" — use this string as the prompt
#   Times are detected by HH:MM pattern; hint is any non-time field 3.
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

  # Field 3: if it looks like HH:MM it's a time; otherwise it's a hint (file or prompt)
  field3=$(awk '{print $3}' <<< "$line")
  if [[ "$field3" =~ ^[0-9]{2}:[0-9]{2}$ ]]; then
    hint=""
    times=$(awk '{for(i=3;i<=NF;i++) print $i}' <<< "$line")
  else
    hint="$field3"
    times=$(awk '{for(i=4;i<=NF;i++) print $i}' <<< "$line")
  fi

  for t in $times; do
    if [[ "$t" == "$CURRENT_TIME" ]]; then
      echo "[$(date '+%b %d %H:%M')] Dispatching: $type $project${hint:+ hint=$hint}" >> "$LOG"
      case "$type" in
        research) bash "$HOME/scripts/run-research.sh"       "$project" ;;
        work)     bash "$HOME/scripts/run-agent.sh"          "$project" ;;
        continue) bash "$HOME/scripts/run-agent-continue.sh" "$project" ;;
        subwork)  bash "$HOME/scripts/run-agent-subdir.sh"   "$project" "$hint" ;;
        *) echo "[$(date '+%b %d %H:%M')] Unknown type: $type" >> "$LOG" ;;
      esac
      break
    fi
  done
done < "$CONF"

#!/bin/bash
# ============================================================
# aiProjects Scheduler
# Reads schedule.conf and dispatches jobs at the right time.
# Runs via launchd every 5 minutes, scheduler dispatches jobs
# based on scripts/schedule.conf
#
# schedule.conf format:
#   type  project  [ai]  [hint]  HH:MM [HH:MM ...]
#
#   ai   (optional): claude | gemini  — overrides AI_CLI env var
#   hint (optional, subwork only):
#     @plan.md   — read this file from the subdir as the prompt
#     @AGENT.md  — read this file from the subdir as the prompt
#   Fields are identified by value; order of ai/hint doesn't matter.
#   Times are always HH:MM pattern.
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

  # Parse fields 3+: classify each token by value
  #   HH:MM pattern → time
  #   claude | gemini → ai override
  #   anything else  → hint (subwork only; first non-classified token wins)
  ai=""
  hint=""
  times=""
  while IFS= read -r token; do
    [[ -z "$token" ]] && continue
    if [[ "$token" =~ ^[0-9]{2}:[0-9]{2}$ ]]; then
      times="$times $token"
    elif [[ "$token" == "claude" || "$token" == "gemini" ]]; then
      ai="$token"
    elif [[ -z "$hint" ]]; then
      hint="$token"
    fi
  done < <(awk '{for(i=3;i<=NF;i++) print $i}' <<< "$line")
  times="${times# }"

  for t in $times; do
    if [[ "$t" == "$CURRENT_TIME" ]]; then
      echo "[$(date '+%b %d %H:%M')] Dispatching: $type $project${ai:+ ai=$ai}${hint:+ hint=$hint}" >> "$LOG"
      case "$type" in
        research) AI_CLI="${ai:-}" bash "$HOME/scripts/run-research.sh"       "$project" ;;
        work)     AI_CLI="${ai:-}" bash "$HOME/scripts/run-agent.sh"          "$project" ;;
        continue) AI_CLI="${ai:-}" bash "$HOME/scripts/run-agent-continue.sh" "$project" ;;
        subwork)  AI_CLI="${ai:-}" bash "$HOME/scripts/run-agent-subdir.sh"   "$project" "$hint" ;;
        *) echo "[$(date '+%b %d %H:%M')] Unknown type: $type" >> "$LOG" ;;
      esac
      break
    fi
  done
done < "$CONF"

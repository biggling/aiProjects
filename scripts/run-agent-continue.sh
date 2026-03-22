#!/bin/bash
# ============================================================
# Continue Agent Runner
# Smarter version of run-agent.sh — inlines both continue.md
# and research/findings/latest.md into the prompt so the agent
# has full context without spending turns reading files.
#
# Usage:
#   ./run-agent-continue.sh <project>
#   ./run-agent-continue.sh <project> "optional focus hint"
#   ./run-agent-continue.sh all
# ============================================================

set -euo pipefail

# ==================== CONFIG ====================
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"
ENV_FILE="$PROJECT_ROOT/.env"

[[ -f "$ENV_FILE" ]] && source "$ENV_FILE"

TELEGRAM_BOT_TOKEN="${TELEGRAM_BOT_TOKEN:-8484927192:AAHVDDU-WGsjJDOC0pSrnb_x_5RQ-mPetaQ}"
TELEGRAM_CHAT_ID="${TELEGRAM_CHAT_ID:-8532895589}"

LOG_DIR="${LOG_DIR:-$PROJECT_ROOT/logs}"
MAX_TIMEOUT="${MAX_TIMEOUT:-600}"
CLAUDE_BIN="${CLAUDE_BIN:-claude}"
TODAY=$(date +%Y-%m-%d)

PROJECT="${1:-}"
FOCUS="${2:-}"
TIMESTAMP=$(date +%Y%m%d_%H%M%S)
DATE_HUMAN=$(date +"%b %d %H:%M")

mkdir -p "$LOG_DIR"

VALID_PROJECTS=("mcp-apps" "digital-products" "tiktok" "trade-auto" "pod" "micro-saas" "youtube-content" "shopee-affiliate" "amazon-kdp" "steam-game" "android-app" "polymarket")

# ==================== HELPERS ====================
usage() {
  echo "Usage: $0 <project|all> [focus]"
  echo ""
  echo "Projects: ${VALID_PROJECTS[*]}"
  echo ""
  echo "Examples:"
  echo "  $0 mcp-apps"
  echo "  $0 trade-auto \"focus on the momentum strategy backtest\""
  echo "  $0 all"
  exit 1
}

send_telegram() {
  local message="$1"
  local parse_mode="${2:-HTML}"
  [[ -z "${TELEGRAM_BOT_TOKEN:-}" || -z "${TELEGRAM_CHAT_ID:-}" ]] && return 0
  curl -s --max-time 10 \
    -X POST "https://api.telegram.org/bot${TELEGRAM_BOT_TOKEN}/sendMessage" \
    -H "Content-Type: application/json" \
    -d "$(jq -n \
      --arg chat_id "$TELEGRAM_CHAT_ID" \
      --arg text "$message" \
      --arg parse_mode "$parse_mode" \
      '{chat_id: $chat_id, text: $text, parse_mode: $parse_mode, disable_web_page_preview: true}'
    )" > /dev/null 2>&1 || true
}

# Returns age string: "today", "yesterday", "N days ago"
research_age() {
  local latest="$1"
  local file_date
  file_date=$(basename "$(ls -t "$(dirname "$latest")"/*.md 2>/dev/null | grep -v latest | head -1)" .md 2>/dev/null || echo "")
  if [[ -z "$file_date" ]]; then
    echo "unknown date"
    return
  fi
  local file_epoch today_epoch diff_days
  file_epoch=$(date -j -f "%Y-%m-%d" "$file_date" +%s 2>/dev/null || date -d "$file_date" +%s 2>/dev/null || echo 0)
  today_epoch=$(date +%s)
  diff_days=$(( (today_epoch - file_epoch) / 86400 ))
  case $diff_days in
    0) echo "today" ;;
    1) echo "yesterday" ;;
    *) echo "${diff_days} days ago" ;;
  esac
}

# ==================== RUN SINGLE PROJECT ====================
run_continue() {
  local proj="$1"
  local focus="${2:-}"
  local log_file="$LOG_DIR/${proj}_continue_${TIMESTAMP}.log"
  local continue_file="$PROJECT_ROOT/$proj/continue.md"
  local latest_file="$PROJECT_ROOT/$proj/research/findings/latest.md"

  echo "[$DATE_HUMAN] Continue: $proj" | tee -a "$LOG_DIR/scheduler.log"

  if [[ ! -f "$continue_file" ]]; then
    echo "[ERROR] $continue_file not found" | tee -a "$LOG_DIR/scheduler.log"
    send_telegram "❌ <b>${proj}</b> — continue.md not found"
    return 1
  fi

  # Read continue.md
  local continue_content
  continue_content=$(cat "$continue_file")

  # Extract phase and next step for Telegram
  local current_phase
  current_phase=$(echo "$continue_content" | grep -A1 "Current Phase" | tail -1 | sed 's/^[[:space:]]*//' | head -c 80)

  # Read research if available
  local research_block=""
  local research_label="none"
  if [[ -f "$latest_file" ]]; then
    local age
    age=$(research_age "$latest_file")
    research_label="$age"
    local research_content
    research_content=$(cat "$latest_file" | head -c 4000)   # cap at ~4k chars
    research_block="## Research Findings (${age})

${research_content}

---
"
  fi

  # Build focus line
  local focus_line=""
  [[ -n "$focus" ]] && focus_line="Focus on: ${focus}"

  # Read project CLAUDE.md if exists (capped)
  local claude_md_block=""
  if [[ -f "$PROJECT_ROOT/$proj/CLAUDE.md" ]]; then
    local claude_md_content
    claude_md_content=$(cat "$PROJECT_ROOT/$proj/CLAUDE.md" | head -c 2000)
    claude_md_block="## Project Config (CLAUDE.md excerpt)

${claude_md_content}

---
"
  fi

  # ── Full prompt ──────────────────────────────────────────
  local prompt
  prompt="You are continuing work on the <${proj}> project. Today is ${TODAY} (Bangkok, GMT+7).

${research_block}${claude_md_block}## Current State (continue.md)

${continue_content}

---

## Your Task

${focus_line:-Continue the highest priority next task from continue.md above.}

Rules:
- Work autonomously. Make decisions yourself unless it involves spending money or live accounts.
- Write production-quality code, not prototypes.
- Use the research findings above to inform decisions where relevant (e.g. pick niches, tune strategy, adjust pricing).
- Do not re-read files you already have above — their contents are already in this prompt.

When done, update ${proj}/continue.md with:
- What was completed this session (be specific)
- Exact next steps (specific enough that future-you can start immediately)
- Any blockers or decisions needed from BiG

End with a 3-line summary of what you accomplished."

  # Notify start
  send_telegram "▶️ <b>${proj}</b> — Continue started
📍 ${current_phase:-unknown phase}
🔬 Research: ${research_label}${focus:+
🎯 Focus: ${focus}}"

  # Run
  local exit_code=0
  local start_time=$SECONDS
  local output
  output=$(cd "$PROJECT_ROOT" && timeout "$MAX_TIMEOUT" \
    "$CLAUDE_BIN" --print "$prompt" \
    --allowedTools "Read,Write,Edit,Bash,Glob,Grep" \
    --max-turns 50 2>&1) || exit_code=$?
  local duration=$(( SECONDS - start_time ))
  local duration_min=$(( duration / 60 ))
  local duration_sec=$(( duration % 60 ))

  echo "$output" > "$log_file"

  if [[ $exit_code -eq 124 ]]; then
    echo "[$DATE_HUMAN] TIMEOUT: $proj continue (${MAX_TIMEOUT}s)" | tee -a "$LOG_DIR/scheduler.log"
    send_telegram "⏰ <b>${proj}</b> — Timed out
⏱ ${duration_min}m ${duration_sec}s"

  elif [[ $exit_code -ne 0 ]]; then
    echo "[$DATE_HUMAN] ERROR: $proj continue (exit $exit_code)" | tee -a "$LOG_DIR/scheduler.log"
    local err
    err=$(echo "$output" | tail -5 | head -c 500 | sed 's/&/\&amp;/g; s/</\&lt;/g; s/>/\&gt;/g')
    send_telegram "❌ <b>${proj}</b> — Failed (exit ${exit_code})
⏱ ${duration_min}m ${duration_sec}s
<pre>${err}</pre>"

  else
    echo "[$DATE_HUMAN] Done: $proj continue (${duration}s)" | tee -a "$LOG_DIR/scheduler.log"
    local summary
    summary=$(echo "$output" | grep -v '^$' | tail -15 | head -c 800 | sed 's/&/\&amp;/g; s/</\&lt;/g; s/>/\&gt;/g')
    local next_step
    next_step=$(grep -A2 "Next Step" "$continue_file" 2>/dev/null | tail -1 | sed 's/^[[:space:]]*//' | head -c 120 | sed 's/&/\&amp;/g; s/</\&lt;/g; s/>/\&gt;/g')

    send_telegram "✅ <b>${proj}</b> — Done
⏱ ${duration_min}m ${duration_sec}s | 🔬 Research used: ${research_label}

<b>Summary:</b>
<pre>${summary}</pre>

<b>Next:</b> ${next_step:-see continue.md}"
  fi

  local log_size
  log_size=$(wc -c < "$log_file")
  echo "[$DATE_HUMAN] Log: ${log_file##*/} (${log_size} bytes, ${duration}s)" >> "$LOG_DIR/scheduler.log"

  return $exit_code
}

# ==================== RUN ALL ====================
run_all() {
  echo "[$DATE_HUMAN] Continue all projects in priority order" | tee -a "$LOG_DIR/scheduler.log"
  send_telegram "🔄 <b>Continue batch starting</b>
📦 Projects: ${#VALID_PROJECTS[@]}"

  local failed=0 completed=0
  for proj in "${VALID_PROJECTS[@]}"; do
    run_continue "$proj" "" && ((completed++)) || ((failed++))
    sleep 30
  done

  if [[ $failed -eq 0 ]]; then
    send_telegram "🎉 <b>All ${completed} projects continued</b>"
  else
    send_telegram "⚠️ <b>Continue batch done</b>
✅ ${completed} succeeded  ❌ ${failed} failed"
  fi
}

# ==================== MAIN ====================
if [[ -z "$PROJECT" ]]; then
  usage
fi

if [[ "$PROJECT" == "all" ]]; then
  run_all
else
  valid=false
  for p in "${VALID_PROJECTS[@]}"; do
    [[ "$p" == "$PROJECT" ]] && valid=true && break
  done
  if [[ "$valid" != "true" ]]; then
    echo "ERROR: Unknown project '$PROJECT'"
    usage
  fi
  run_continue "$PROJECT" "$FOCUS"
fi

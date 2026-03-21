#!/bin/bash
# ============================================================
# Side Projects Agent Runner
# Runs Claude Code agents on schedule via crontab
# Sends results to Telegram for mobile review
# ============================================================

set -euo pipefail

# ==================== CONFIG ====================
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"
ENV_FILE="$PROJECT_ROOT/.env"

# Source .env if it exists (optional — Telegram config has defaults)
[[ -f "$ENV_FILE" ]] && source "$ENV_FILE"

# Telegram
TELEGRAM_BOT_TOKEN="${TELEGRAM_BOT_TOKEN:-8484927192:AAHVDDU-WGsjJDOC0pSrnb_x_5RQ-mPetaQ}"
TELEGRAM_CHAT_ID="${TELEGRAM_CHAT_ID:-8532895589}"

# Defaults
LOG_DIR="${LOG_DIR:-$PROJECT_ROOT/logs}"
MAX_TIMEOUT="${MAX_TIMEOUT:-600}"  # 10 minutes max per session
CLAUDE_BIN="${CLAUDE_BIN:-claude}"

# ==================== SETUP ====================
PROJECT="${1:-}"
CUSTOM_PROMPT="${2:-}"
TIMESTAMP=$(date +%Y%m%d_%H%M%S)
DATE_HUMAN=$(date +"%b %d %H:%M")

mkdir -p "$LOG_DIR"

# ==================== VALIDATION ====================
VALID_PROJECTS=("tiktok" "trade-auto" "pod" "shopee-affiliate" "amazon-kdp" "steam-game" "android-app" "polymarket")

usage() {
  echo "Usage: $0 <project> [custom-prompt]"
  echo ""
  echo "Projects: ${VALID_PROJECTS[*]}"
  echo ""
  echo "Examples:"
  echo "  $0 trade-auto"
  echo "  $0 pod \"Focus on generating 5 new t-shirt designs\""
  echo "  $0 all    # Run all projects in priority order"
  exit 1
}

if [[ -z "$PROJECT" ]]; then
  usage
fi

# ==================== TELEGRAM ====================
send_telegram() {
  local message="$1"
  local parse_mode="${2:-HTML}"

  if [[ -z "${TELEGRAM_BOT_TOKEN:-}" || -z "${TELEGRAM_CHAT_ID:-}" ]]; then
    echo "[WARN] Telegram not configured, skipping notification"
    return 0
  fi

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

# ==================== RUN SINGLE PROJECT ====================
run_project() {
  local proj="$1"
  local custom="${2:-}"
  local log_file="$LOG_DIR/${proj}_${TIMESTAMP}.log"
  local continue_file="$PROJECT_ROOT/$proj/continue.md"

  echo "[$DATE_HUMAN] Starting: $proj" | tee -a "$LOG_DIR/scheduler.log"

  # Check continue.md exists
  if [[ ! -f "$continue_file" ]]; then
    echo "[ERROR] $continue_file not found" | tee -a "$LOG_DIR/scheduler.log"
    send_telegram "❌ $proj — continue.md not found"
    return 1
  fi

  # Build the prompt
  local prompt
  if [[ -n "$custom" ]]; then
    prompt="$custom

After completing the task, update $proj/continue.md with:
- What was completed
- Exact next steps
- Any blockers"
  else
    prompt="Read $proj/continue.md carefully. Also read $proj/CLAUDE.md if it exists.

Execute the highest priority next task listed there.
Work autonomously — make decisions yourself unless it involves spending money.
Write production-quality code, not prototypes.

When done, update $proj/continue.md with:
- What was completed this session (be specific)
- Exact next steps (so specific that future-you can start immediately)
- Any blockers or decisions needed from BiG

End with a 3-line summary of what you accomplished."
  fi

  # Extract current phase from continue.md
  local current_phase
  current_phase=$(grep -A1 "Current Phase" "$continue_file" 2>/dev/null | tail -1 | sed 's/^[[:space:]]*//' | head -c 80)

  # Notify start
  send_telegram "🚀 <b>${proj}</b> — Agent started
📍 ${current_phase:-unknown phase}"

  # Run Claude Code with timeout
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

  # Save full log
  echo "$output" > "$log_file"

  # Handle results
  if [[ $exit_code -eq 124 ]]; then
    echo "[$DATE_HUMAN] TIMEOUT: $proj (${MAX_TIMEOUT}s)" | tee -a "$LOG_DIR/scheduler.log"
    send_telegram "⏰ <b>${proj}</b> — Timed out

⏱ Duration: ${duration_min}m ${duration_sec}s
📄 Log: ${log_file##*/}"

  elif [[ $exit_code -ne 0 ]]; then
    echo "[$DATE_HUMAN] ERROR: $proj (exit $exit_code)" | tee -a "$LOG_DIR/scheduler.log"
    local error_tail
    error_tail=$(echo "$output" | tail -5 | head -c 500 | sed 's/&/\&amp;/g; s/</\&lt;/g; s/>/\&gt;/g')
    send_telegram "❌ <b>${proj}</b> — Failed (exit ${exit_code})

⏱ Duration: ${duration_min}m ${duration_sec}s
<pre>${error_tail}</pre>"

  else
    echo "[$DATE_HUMAN] Done: $proj" | tee -a "$LOG_DIR/scheduler.log"

    # Extract summary: last meaningful lines (skip blank lines)
    local summary
    summary=$(echo "$output" | grep -v '^$' | tail -15 | head -c 800 | sed 's/&/\&amp;/g; s/</\&lt;/g; s/>/\&gt;/g')

    # Read updated continue.md for next actions
    local next_action
    next_action=$(grep -A2 "Next Actions" "$continue_file" 2>/dev/null | tail -1 | sed 's/^[[:space:]]*//' | head -c 120)

    send_telegram "✅ <b>${proj}</b> — Done

⏱ Duration: ${duration_min}m ${duration_sec}s
📍 Phase: ${current_phase}

<b>Summary:</b>
<pre>${summary}</pre>

<b>Next:</b> ${next_action:-check continue.md}"
  fi

  # Log file size for monitoring
  local log_size
  log_size=$(wc -c < "$log_file")
  echo "[$DATE_HUMAN] Log: ${log_file##*/} (${log_size} bytes, ${duration}s)" >> "$LOG_DIR/scheduler.log"

  return $exit_code
}

# ==================== RUN ALL PROJECTS ====================
run_all() {
  echo "[$DATE_HUMAN] Running all projects in priority order" | tee -a "$LOG_DIR/scheduler.log"
  send_telegram "🔄 <b>Full rotation starting</b>
📦 Projects: ${#VALID_PROJECTS[@]}"

  local failed=0
  local completed=0
  for proj in "${VALID_PROJECTS[@]}"; do
    run_project "$proj" "" && ((completed++)) || ((failed++))
    sleep 30
  done

  if [[ $failed -eq 0 ]]; then
    send_telegram "🎉 <b>All ${completed} projects completed</b>"
  else
    send_telegram "⚠️ <b>Rotation done</b>
✅ ${completed} succeeded
❌ ${failed} failed"
  fi
}

# ==================== MAIN ====================
if [[ "$PROJECT" == "all" ]]; then
  run_all
else
  # Validate project name
  valid=false
  for p in "${VALID_PROJECTS[@]}"; do
    [[ "$p" == "$PROJECT" ]] && valid=true && break
  done

  if [[ "$valid" != "true" ]]; then
    echo "ERROR: Unknown project '$PROJECT'"
    usage
  fi

  run_project "$PROJECT" "$CUSTOM_PROMPT"
fi

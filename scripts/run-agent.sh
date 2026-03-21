#!/bin/bash
# ============================================================
# Side Projects Agent Runner
# Runs Claude Code agents on schedule via crontab
# Sends results to Telegram for mobile review
# ============================================================

set -euo pipefail

# ==================== CONFIG ====================
# Copy .env.example to .env and fill in your values
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"
ENV_FILE="$PROJECT_ROOT/.env"

if [[ ! -f "$ENV_FILE" ]]; then
  echo "ERROR: $ENV_FILE not found. Copy .env.example to .env and fill in values."
  exit 1
fi

source "$ENV_FILE"

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
VALID_PROJECTS=("trade-auto" "pod" "shopee-affiliate" "amazon-kdp" "steam-game" "android-app" "polymarket")

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
  local parse_mode="${2:-}"

  if [[ -z "${TELEGRAM_BOT_TOKEN:-}" || -z "${TELEGRAM_CHAT_ID:-}" ]]; then
    echo "[WARN] Telegram not configured, skipping notification"
    return 0
  fi

  local payload="chat_id=$TELEGRAM_CHAT_ID&text=$message&disable_web_page_preview=true"
  if [[ -n "$parse_mode" ]]; then
    payload="$payload&parse_mode=$parse_mode"
  fi

  curl -s --max-time 10 \
    "https://api.telegram.org/bot${TELEGRAM_BOT_TOKEN}/sendMessage" \
    -d "$payload" > /dev/null 2>&1 || true
}

# ==================== RUN SINGLE PROJECT ====================
run_project() {
  local proj="$1"
  local custom="${2:-}"
  local log_file="$LOG_DIR/${proj}_${TIMESTAMP}.log"
  local continue_file="$PROJECT_ROOT/projects/$proj/continue.md"

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

After completing the task, update projects/$proj/continue.md with:
- What was completed
- Exact next steps
- Any blockers"
  else
    prompt="Read projects/$proj/continue.md carefully.

Execute the highest priority next task listed there.
Work autonomously — make decisions yourself unless it involves spending money.
Write production-quality code, not prototypes.

When done, update projects/$proj/continue.md with:
- What was completed this session (be specific)
- Exact next steps (so specific that future-you can start immediately)  
- Any blockers or decisions needed from BiG

End with a 3-line summary of what you accomplished."
  fi

  # Notify start
  send_telegram "🚀 Starting: $proj
📋 $(head -5 "$continue_file" | tail -3)"

  # Run Claude Code with timeout
  local exit_code=0
  local output
  output=$(cd "$PROJECT_ROOT" && timeout "$MAX_TIMEOUT" \
    "$CLAUDE_BIN" --agent "$proj" --print "$prompt" 2>&1) || exit_code=$?

  # Save full log
  echo "$output" > "$log_file"

  # Handle results
  if [[ $exit_code -eq 124 ]]; then
    echo "[$DATE_HUMAN] TIMEOUT: $proj (${MAX_TIMEOUT}s)" | tee -a "$LOG_DIR/scheduler.log"
    send_telegram "⏰ $proj — Timed out after ${MAX_TIMEOUT}s
Check log: ${log_file##*/}"
  elif [[ $exit_code -ne 0 ]]; then
    echo "[$DATE_HUMAN] ERROR: $proj (exit $exit_code)" | tee -a "$LOG_DIR/scheduler.log"
    local error_tail
    error_tail=$(echo "$output" | tail -5)
    send_telegram "❌ $proj — Error (exit $exit_code)
$error_tail"
  else
    echo "[$DATE_HUMAN] Done: $proj" | tee -a "$LOG_DIR/scheduler.log"

    # Extract summary (last 30 lines, trim to Telegram limit)
    local summary
    summary=$(echo "$output" | tail -30 | head -c 3000)
    send_telegram "✅ $proj — Done
$summary"
  fi

  # Log file size for monitoring
  local log_size
  log_size=$(wc -c < "$log_file")
  echo "[$DATE_HUMAN] Log: ${log_file##*/} (${log_size} bytes)" >> "$LOG_DIR/scheduler.log"

  return $exit_code
}

# ==================== RUN ALL PROJECTS ====================
run_all() {
  echo "[$DATE_HUMAN] Running all projects in priority order" | tee -a "$LOG_DIR/scheduler.log"
  send_telegram "🔄 Starting full project rotation..."

  local failed=0
  for proj in "${VALID_PROJECTS[@]}"; do
    run_project "$proj" "" || ((failed++))
    # Pause between projects to avoid rate limits
    sleep 30
  done

  if [[ $failed -eq 0 ]]; then
    send_telegram "🎉 All projects completed successfully"
  else
    send_telegram "⚠️ Rotation done — $failed project(s) had issues"
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

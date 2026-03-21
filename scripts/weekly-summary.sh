#!/bin/bash
# ============================================================
# Weekly Summary — Sends project digest to Telegram
# Runs every Sunday 21:00 via crontab
# ============================================================

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"
ENV_FILE="$PROJECT_ROOT/.env"

source "$ENV_FILE"

LOG_DIR="${LOG_DIR:-$PROJECT_ROOT/logs}"
WEEK_AGO=$(date -d "7 days ago" +%Y%m%d 2>/dev/null || date -v-7d +%Y%m%d)

# Count sessions this week per project
count_sessions() {
  local proj="$1"
  find "$LOG_DIR" -name "${proj}_*.log" -newer "$LOG_DIR/.week_marker" 2>/dev/null | wc -l || echo "0"
}

# Get last line of latest log (usually the summary)
last_summary() {
  local proj="$1"
  local latest
  latest=$(ls -t "$LOG_DIR"/${proj}_*.log 2>/dev/null | head -1)
  if [[ -n "$latest" ]]; then
    tail -5 "$latest" | head -c 500
  else
    echo "No sessions this week"
  fi
}

# Get current phase from continue.md
current_phase() {
  local proj="$1"
  local cf="$PROJECT_ROOT/projects/$proj/continue.md"
  if [[ -f "$cf" ]]; then
    grep -A1 "Current Phase" "$cf" | tail -1 | sed 's/^[[:space:]]*//'
  else
    echo "Unknown"
  fi
}

# Build summary message
MSG="📊 WEEKLY DIGEST — $(date +'%b %d, %Y')
━━━━━━━━━━━━━━━━━━━━━

🔴 Trade Automation
   Phase: $(current_phase trade-auto)
   Sessions: $(count_sessions trade-auto)
   Latest: $(last_summary trade-auto | head -1)

🟠 Print on Demand
   Phase: $(current_phase pod)
   Sessions: $(count_sessions pod)
   Latest: $(last_summary pod | head -1)

🔵 Android App
   Phase: $(current_phase android-app)
   Sessions: $(count_sessions android-app)
   Latest: $(last_summary android-app | head -1)

🟣 Polymarket
   Phase: $(current_phase polymarket)
   Sessions: $(count_sessions polymarket)
   Latest: $(last_summary polymarket | head -1)

🟢 Shopee Affiliate
   Phase: $(current_phase shopee-affiliate)
   Sessions: $(count_sessions shopee-affiliate)
   Latest: $(last_summary shopee-affiliate | head -1)

📚 Amazon KDP
   Phase: $(current_phase amazon-kdp)
   Sessions: $(count_sessions amazon-kdp)
   Latest: $(last_summary amazon-kdp | head -1)

🎮 Steam Game
   Phase: $(current_phase steam-game)
   Sessions: $(count_sessions steam-game)
   Latest: $(last_summary steam-game | head -1)

━━━━━━━━━━━━━━━━━━━━━
💡 Reply /run <project> to trigger a manual session"

# Send to Telegram
if [[ -n "${TELEGRAM_BOT_TOKEN:-}" && -n "${TELEGRAM_CHAT_ID:-}" ]]; then
  curl -s --max-time 10 \
    "https://api.telegram.org/bot${TELEGRAM_BOT_TOKEN}/sendMessage" \
    -d "chat_id=$TELEGRAM_CHAT_ID" \
    -d "text=$MSG" \
    -d "disable_web_page_preview=true" > /dev/null 2>&1
fi

# Touch week marker for next week's count
touch "$LOG_DIR/.week_marker"

echo "[$(date +'%b %d %H:%M')] Weekly summary sent" >> "$LOG_DIR/scheduler.log"

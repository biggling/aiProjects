#!/bin/bash
# ============================================================
# Weekly Summary — Sends project digest to Telegram
# Runs every Sunday 21:00 via crontab
# ============================================================

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"
ENV_FILE="$PROJECT_ROOT/.env"

[[ -f "$ENV_FILE" ]] && source "$ENV_FILE"

# Telegram config
TELEGRAM_BOT_TOKEN="${TELEGRAM_BOT_TOKEN:-8484927192:AAHVDDU-WGsjJDOC0pSrnb_x_5RQ-mPetaQ}"
TELEGRAM_CHAT_ID="${TELEGRAM_CHAT_ID:-8532895589}"

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
  local cf="$PROJECT_ROOT/$proj/continue.md"
  if [[ -f "$cf" ]]; then
    grep -A1 "Current Phase" "$cf" | tail -1 | sed 's/^[[:space:]]*//'
  else
    echo "Unknown"
  fi
}

# Build summary message
MSG="📊 <b>WEEKLY DIGEST</b> — $(date +'%b %d, %Y')

🎬 <b>TikTok</b>
   $(current_phase tiktok) | Sessions: $(count_sessions tiktok)

📈 <b>Trade Auto</b>
   $(current_phase trade-auto) | Sessions: $(count_sessions trade-auto)

🎨 <b>POD (Etsy)</b>
   $(current_phase pod) | Sessions: $(count_sessions pod)

🛒 <b>Shopee Affiliate</b>
   $(current_phase shopee-affiliate) | Sessions: $(count_sessions shopee-affiliate)

📚 <b>Amazon KDP</b>
   $(current_phase amazon-kdp) | Sessions: $(count_sessions amazon-kdp)

🎮 <b>Steam Game</b>
   $(current_phase steam-game) | Sessions: $(count_sessions steam-game)

📱 <b>Android App</b>
   $(current_phase android-app) | Sessions: $(count_sessions android-app)

🔮 <b>Polymarket</b>
   $(current_phase polymarket) | Sessions: $(count_sessions polymarket)"

# Send to Telegram
curl -s --max-time 10 \
  -X POST "https://api.telegram.org/bot${TELEGRAM_BOT_TOKEN}/sendMessage" \
  -H "Content-Type: application/json" \
  -d "$(jq -n \
    --arg chat_id "$TELEGRAM_CHAT_ID" \
    --arg text "$MSG" \
    '{chat_id: $chat_id, text: $text, parse_mode: "HTML", disable_web_page_preview: true}'
  )" > /dev/null 2>&1 || true

# Touch week marker for next week's count
touch "$LOG_DIR/.week_marker"

echo "[$(date +'%b %d %H:%M')] Weekly summary sent" >> "$LOG_DIR/scheduler.log"

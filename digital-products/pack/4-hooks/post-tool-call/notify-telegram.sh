#!/usr/bin/env bash
# post-tool-call/notify-telegram.sh
# Sends a Telegram notification after each tool call completes.
# Optional — requires TELEGRAM_BOT_TOKEN and TELEGRAM_CHAT_ID env vars.
# Claude Code hook — PostToolCall
# Always exits 0.

# Skip if not configured
if [ -z "$TELEGRAM_BOT_TOKEN" ] || [ -z "$TELEGRAM_CHAT_ID" ]; then
  exit 0
fi

INPUT=$(cat)
TOOL=$(echo "$INPUT" | python3 -c "import sys,json; d=json.load(sys.stdin); print(d.get('tool_name', d.get('type','unknown')))" 2>/dev/null || echo "unknown")
PROJECT=$(basename "$(pwd)")
TIMESTAMP=$(date +"%H:%M")

# Only notify on meaningful tools (skip reads and globs to reduce noise)
case "$TOOL" in
  Read|Glob|Grep|WebSearch) exit 0 ;;
esac

MESSAGE="[${PROJECT}] ${TOOL} completed at ${TIMESTAMP}"

curl -s -X POST "https://api.telegram.org/bot${TELEGRAM_BOT_TOKEN}/sendMessage" \
  -d "chat_id=${TELEGRAM_CHAT_ID}" \
  -d "text=${MESSAGE}" \
  -d "parse_mode=Markdown" \
  > /dev/null 2>&1

exit 0

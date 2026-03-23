#!/bin/bash
# Test script — verify claude works via cron
# Triggered every 2 minutes, logs result to logs/cron-test.log

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"
LOG="$PROJECT_ROOT/logs/cron-test.log"
TIMESTAMP=$(date "+%Y-%m-%d %H:%M:%S")

echo "[$TIMESTAMP] --- test start ---" >> "$LOG"
echo "[$TIMESTAMP] PATH=$PATH" >> "$LOG"

# Step 1: check where claude is (equivalent to subprocess which)
CLAUDE_CMD=$(which claude 2>/dev/null)
if [[ -z "$CLAUDE_CMD" ]]; then
  # fallback: check common locations
  for p in /Users/big/.local/bin/claude /usr/local/bin/claude /opt/homebrew/bin/claude; do
    [[ -x "$p" ]] && CLAUDE_CMD="$p" && break
  done
fi

echo "[$TIMESTAMP] which claude=$CLAUDE_CMD" >> "$LOG"

if [[ -z "$CLAUDE_CMD" ]]; then
  echo "[$TIMESTAMP] ERROR: claude not found" >> "$LOG"
  echo "[$TIMESTAMP] --- test end ---" >> "$LOG"
  exit 1
fi

# Step 2: run claude
RESULT=$("$CLAUDE_CMD" --print "reply with just: OK" --max-turns 1 2>&1)
EXIT=$?

echo "[$TIMESTAMP] exit=$EXIT" >> "$LOG"
echo "[$TIMESTAMP] output=$RESULT" >> "$LOG"
echo "[$TIMESTAMP] --- test end ---" >> "$LOG"

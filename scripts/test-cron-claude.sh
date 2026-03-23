#!/bin/bash
# Test script — verify claude works via cron
# Triggered every 2 minutes, logs result to logs/cron-test.log

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"
LOG="$PROJECT_ROOT/logs/cron-test.log"
TIMESTAMP=$(date "+%Y-%m-%d %H:%M:%S")

echo "[$TIMESTAMP] --- test start ---" >> "$LOG"

# Method: spawn claude via login shell so ~/.zprofile is sourced
# and session credentials are loaded
RESULT=$(exec /bin/zsh -l -c 'claude --print "reply with just: OK" --max-turns 1' 2>&1)
EXIT=$?

echo "[$TIMESTAMP] exit=$EXIT" >> "$LOG"
echo "[$TIMESTAMP] output=$RESULT" >> "$LOG"
echo "[$TIMESTAMP] --- test end ---" >> "$LOG"

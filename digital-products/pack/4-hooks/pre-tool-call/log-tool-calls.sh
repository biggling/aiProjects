#!/usr/bin/env bash
# pre-tool-call/log-tool-calls.sh
# Logs every tool call with timestamp to ~/.claude/tool-calls.log.
# Claude Code hook — PreToolUse (no matcher = fires on all tools)
# Always exits 0 — never blocks.

LOG_FILE="${HOME}/.claude/tool-calls.log"
mkdir -p "$(dirname "$LOG_FILE")"

INPUT=$(cat)
TOOL=$(echo "$INPUT" | jq -r '.tool_name // "unknown"' 2>/dev/null || echo "unknown")
TIMESTAMP=$(date -u +"%Y-%m-%dT%H:%M:%SZ")
PROJECT=$(basename "${CLAUDE_PROJECT_DIR:-$(pwd)}")

# Log compact one-liner
echo "${TIMESTAMP} | ${PROJECT} | ${TOOL}" >> "$LOG_FILE"

exit 0

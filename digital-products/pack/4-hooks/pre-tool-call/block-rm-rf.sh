#!/usr/bin/env bash
# pre-tool-call/block-rm-rf.sh
# Blocks any `rm -rf` command that targets paths outside /tmp.
# Claude Code hook — PreToolUse, matcher: Bash
# Deny: output JSON + exit 0. Allow: exit 0 with no output.

INPUT=$(cat)
COMMAND=$(echo "$INPUT" | jq -r '.tool_input.command // empty' 2>/dev/null)

# Check if this is a rm -rf / rm -r command
if echo "$COMMAND" | grep -qE 'rm\s+(-[a-zA-Z]*r[a-zA-Z]*f?|--recursive)\s'; then
  # Allow if target is strictly /tmp
  if echo "$COMMAND" | grep -qE 'rm\s+.*\s+/tmp/'; then
    exit 0
  fi
  printf '{"hookSpecificOutput":{"hookEventName":"PreToolUse","permissionDecision":"deny","permissionDecisionReason":"rm -rf is blocked outside /tmp. Use specific file deletions instead, or ask the user to run this command manually."}}'
  exit 0
fi

exit 0

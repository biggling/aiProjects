#!/usr/bin/env bash
# pre-tool-call/block-rm-rf.sh
# Blocks any `rm -rf` command that targets paths outside /tmp.
# Claude Code hook — PreToolCall, matcher: Bash
# Exit 0 = allow. Exit 1 = block.

# Hook receives tool input as JSON on stdin
INPUT=$(cat)
COMMAND=$(echo "$INPUT" | python3 -c "import sys,json; d=json.load(sys.stdin); print(d.get('command',''))" 2>/dev/null || echo "")

# Check if this is a rm -rf / rm -r command
if echo "$COMMAND" | grep -qE 'rm\s+(-[a-zA-Z]*r[a-zA-Z]*f?|--recursive)\s'; then
  # Allow if target is strictly /tmp
  if echo "$COMMAND" | grep -qE 'rm\s+.*\s+/tmp/'; then
    exit 0
  fi
  echo "BLOCKED: rm -rf detected outside /tmp. Command: $COMMAND" >&2
  echo "If you need to delete recursively, confirm with the user first or use a safer approach." >&2
  exit 1
fi

exit 0

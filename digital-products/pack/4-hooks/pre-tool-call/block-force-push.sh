#!/usr/bin/env bash
# pre-tool-call/block-force-push.sh
# Blocks git push --force and git push -f in all forms.
# Claude Code hook — PreToolCall, matcher: Bash
# Exit 0 = allow. Exit 1 = block.

INPUT=$(cat)
COMMAND=$(echo "$INPUT" | python3 -c "import sys,json; d=json.load(sys.stdin); print(d.get('command',''))" 2>/dev/null || echo "")

if echo "$COMMAND" | grep -qE 'git\s+push\s+.*(--force|-f)\b'; then
  echo "BLOCKED: git push --force is not allowed." >&2
  echo "If you need to force-push, the user must run this command manually." >&2
  exit 1
fi

if echo "$COMMAND" | grep -qE 'git\s+push\s+--force-with-lease'; then
  echo "BLOCKED: git push --force-with-lease detected. User must confirm before force-pushing." >&2
  exit 1
fi

exit 0

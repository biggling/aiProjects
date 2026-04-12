#!/usr/bin/env bash
# pre-tool-call/block-force-push.sh
# Blocks git push --force and git push -f in all forms.
# Claude Code hook — PreToolUse, matcher: Bash
# Deny: output JSON + exit 0. Allow: exit 0 with no output.

INPUT=$(cat)
COMMAND=$(echo "$INPUT" | jq -r '.tool_input.command // empty' 2>/dev/null)

if echo "$COMMAND" | grep -qE 'git\s+push\s+.*(--force|-f)\b'; then
  printf '{"hookSpecificOutput":{"hookEventName":"PreToolUse","permissionDecision":"deny","permissionDecisionReason":"git push --force is blocked. Force-pushes must be run manually by the user."}}'
  exit 0
fi

if echo "$COMMAND" | grep -qE 'git\s+push\s+--force-with-lease'; then
  printf '{"hookSpecificOutput":{"hookEventName":"PreToolUse","permissionDecision":"deny","permissionDecisionReason":"git push --force-with-lease is blocked. The user must confirm and run force-pushes manually."}}'
  exit 0
fi

exit 0

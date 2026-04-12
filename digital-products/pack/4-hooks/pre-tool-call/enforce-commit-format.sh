#!/usr/bin/env bash
# enforce-commit-format.sh — PreToolUse hook
# Blocks git commits that don't follow Conventional Commits format.
# Fires BEFORE the Bash tool executes — Claude cannot bypass this.
#
# Allowed format:  type(scope): description
# Types: feat, fix, docs, style, refactor, test, chore, perf, ci, build
#
# Setup: register in ~/.claude/settings.json under PreToolUse → matcher: "Bash"

INPUT=$(cat)
COMMAND=$(echo "$INPUT" | jq -r '.tool_input.command // empty' 2>/dev/null)

# Only check git commit commands
if ! echo "$COMMAND" | grep -qE 'git commit'; then
    exit 0
fi

# Extract the commit message (-m "..." or --message="...")
MSG=$(echo "$COMMAND" | sed -n 's/.*-m[[:space:]]*["\x27]\([^"'\'']*\)["\x27].*/\1/p')
if [ -z "$MSG" ]; then
    MSG=$(echo "$COMMAND" | sed -n 's/.*--message=["\x27]\([^"'\'']*\)["\x27].*/\1/p')
fi

# No -m flag = interactive commit = allow through
if [ -z "$MSG" ]; then
    exit 0
fi

# Validate conventional commits format
if ! echo "$MSG" | grep -qE "^(feat|fix|docs|style|refactor|test|chore|perf|ci|build)(\([^)]+\))?!?: .+"; then
    printf '{"hookSpecificOutput":{"hookEventName":"PreToolUse","permissionDecision":"deny","permissionDecisionReason":"Commit message does not follow Conventional Commits format. Required: type(scope): description. Types: feat, fix, docs, style, refactor, test, chore, perf, ci, build. Example: feat(auth): add JWT refresh endpoint. Your message: %s"}}' "$MSG"
    exit 0
fi

exit 0

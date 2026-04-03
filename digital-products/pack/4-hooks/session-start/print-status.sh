#!/usr/bin/env bash
# session-start/print-status.sh
# Prints git context when a Claude Code session opens.
# Claude Code hook — SessionStart
# Stdout is shown to Claude as context.

echo "=== Session Start: $(date '+%Y-%m-%d %H:%M %Z') ==="
echo ""

# Git branch and status
if git rev-parse --is-inside-work-tree > /dev/null 2>&1; then
  BRANCH=$(git branch --show-current)
  echo "Branch: $BRANCH"
  echo ""

  STATUS=$(git status --short)
  if [ -n "$STATUS" ]; then
    echo "Working tree:"
    echo "$STATUS"
    echo ""
  else
    echo "Working tree: clean"
    echo ""
  fi

  echo "Recent commits:"
  git log --oneline -5
  echo ""
else
  echo "(Not a git repository)"
  echo ""
fi

# Show continue.md exists
if [ -f "continue.md" ]; then
  echo "continue.md: found — read this before starting work"
fi

if [ -f "memory-bank/activeContext.md" ]; then
  echo "memory-bank/: found — read all files in memory-bank/ before starting work"
fi

echo "==="

exit 0

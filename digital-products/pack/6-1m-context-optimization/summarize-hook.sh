#!/usr/bin/env bash
# summarize-hook.sh — Post-session summarizer.
# Appends a 3-line session summary to memory-bank/activeContext.md.
# Claude Code hook — SessionStop (or run manually after a session)
# Usage: bash summarize-hook.sh (from project root)

set -e

MEMORY_FILE="memory-bank/activeContext.md"
LOG_DIR="data/logs"
mkdir -p "$LOG_DIR"

if [ ! -f "$MEMORY_FILE" ]; then
  echo "[summarize-hook] No memory-bank/activeContext.md found. Skipping." >&2
  exit 0
fi

TIMESTAMP=$(date '+%Y-%m-%d %H:%M')

# Ask Claude to summarize the session in 3 bullets
PROMPT="Look at the recent changes in this git repository and the current state of memory-bank/activeContext.md.

Write exactly 3 bullet points summarizing this session:
- Done: [what was completed]
- Decided: [key decisions made]
- Next: [the single most important next step]

Format output as:

### Session: $TIMESTAMP
- Done: ...
- Decided: ...
- Next: ...

Output only those 4 lines. Nothing else."

SUMMARY=$(claude --print "$PROMPT" \
  --allowedTools "Read,Bash,Glob,Grep" \
  --max-turns 5 \
  2>/dev/null | tail -5)

if [ -n "$SUMMARY" ]; then
  echo "" >> "$MEMORY_FILE"
  echo "$SUMMARY" >> "$MEMORY_FILE"
  echo "[summarize-hook] Appended session summary to $MEMORY_FILE"
else
  echo "[summarize-hook] No summary generated." >&2
fi

exit 0

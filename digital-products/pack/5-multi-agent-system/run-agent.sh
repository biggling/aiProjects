#!/usr/bin/env bash
# run-agent.sh — Run Claude Code non-interactively on a project.
# Usage: ./scripts/run-agent.sh <project> [prompt]
# Examples:
#   ./scripts/run-agent.sh my-project
#   ./scripts/run-agent.sh my-project "build the export feature"

set -e

WORKSPACE_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
PROJECT="${1:-}"
PROMPT="${2:-}"

if [ -z "$PROJECT" ]; then
  echo "Usage: $0 <project> [prompt]" >&2
  exit 1
fi

PROJECT_DIR="$WORKSPACE_ROOT/$PROJECT"
if [ ! -d "$PROJECT_DIR" ]; then
  echo "Project directory not found: $PROJECT_DIR" >&2
  exit 1
fi

CONTINUE_FILE="$PROJECT_DIR/continue.md"
CLAUDE_MD="$PROJECT_DIR/CLAUDE.md"
LOG_DIR="$WORKSPACE_ROOT/logs"
mkdir -p "$LOG_DIR"
LOG_FILE="$LOG_DIR/${PROJECT}_$(date +%Y%m%d_%H%M%S).log"

# Build prompt
if [ -z "$PROMPT" ]; then
  if [ -f "$CONTINUE_FILE" ]; then
    PROMPT="Read continue.md and work on the highest priority next action. Update continue.md when done."
  else
    PROMPT="Explore the project and identify the most important next task. Create continue.md with your findings."
  fi
fi

echo "[$(date '+%Y-%m-%d %H:%M:%S')] Starting agent: $PROJECT"
echo "[$(date '+%Y-%m-%d %H:%M:%S')] Prompt: $PROMPT"
echo ""

cd "$PROJECT_DIR"

ALLOWED_TOOLS="Read,Write,Edit,Bash,Glob,Grep"

claude --print "$PROMPT" \
  --allowedTools "$ALLOWED_TOOLS" \
  --max-turns 50 \
  2>&1 | tee "$LOG_FILE"

EXIT_CODE=${PIPESTATUS[0]}

echo ""
echo "[$(date '+%Y-%m-%d %H:%M:%S')] Agent finished. Exit: $EXIT_CODE. Log: $LOG_FILE"

exit $EXIT_CODE

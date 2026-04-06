#!/bin/bash
# ============================================================
# Subdir Work Agent Runner
# Like run-agent.sh but changes working directory to a
# specific subdirectory before running Claude.
#
# Usage:
#   ./run-agent-subdir.sh <project/subdir> [hint]
#
#   hint can be:
#     @plan.md          — read plan.md from the subdir as the prompt
#     @AGENT.md         — read AGENT.md from the subdir as the prompt
#     "inline prompt"   — use this string directly as the prompt
#     (empty)           — auto-detect: AGENT.md → plan.md → continue.md
#
# Examples:
#   ./run-agent-subdir.sh trade-auto/src
#   ./run-agent-subdir.sh trade-auto/src @plan.md
#   ./run-agent-subdir.sh tiktok/modules @AGENT.md
#   ./run-agent-subdir.sh pod/scripts "Generate 5 new design prompts"
#
# The project root (for continue.md and logs) is derived from
# the first path component: "trade-auto/src" → project=trade-auto
# ============================================================

set -euo pipefail

# ==================== CONFIG ====================
if [[ -z "${PROJECT_ROOT:-}" ]]; then
  SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
  PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"
fi
ENV_FILE="$PROJECT_ROOT/.env"

[[ -f "$ENV_FILE" ]] && source "$ENV_FILE"

TELEGRAM_BOT_TOKEN="${TELEGRAM_BOT_TOKEN:-8484927192:AAHVDDU-WGsjJDOC0pSrnb_x_5RQ-mPetaQ}"
TELEGRAM_CHAT_ID="${TELEGRAM_CHAT_ID:-8532895589}"

LOG_DIR="${LOG_DIR:-$PROJECT_ROOT/logs}"
MAX_TIMEOUT="${MAX_TIMEOUT:-600}"
CLAUDE_BIN="${CLAUDE_BIN:-claude}"

# ==================== ARGS ====================
PROJECT_PATH="${1:-}"   # e.g. "trade-auto/src" or "mcp-apps/packages/server"
HINT="${2:-}"           # @file, "inline prompt", or empty (auto-detect)
TIMESTAMP=$(date +%Y%m%d_%H%M%S)
DATE_HUMAN=$(date +"%b %d %H:%M")

mkdir -p "$LOG_DIR"

usage() {
  echo "Usage: $0 <project/subdir> [@file | \"prompt\"]"
  echo ""
  echo "Examples:"
  echo "  $0 trade-auto/src"
  echo "  $0 trade-auto/src @plan.md"
  echo "  $0 tiktok/modules @AGENT.md"
  echo "  $0 pod/scripts \"Generate 5 new design prompts\""
  exit 1
}

[[ -z "$PROJECT_PATH" ]] && usage

# ==================== PARSE PATH ====================
# First component = project name (for continue.md, logs, Telegram)
# Full path = working directory for Claude
PROJECT="${PROJECT_PATH%%/*}"   # "trade-auto/src" → "trade-auto"
SUBDIR="${PROJECT_PATH#*/}"     # "trade-auto/src" → "src"

# If no slash, subdir is empty (treat same as run-agent.sh)
if [[ "$PROJECT" == "$PROJECT_PATH" ]]; then
  SUBDIR=""
fi

WORK_DIR="$PROJECT_ROOT/$PROJECT_PATH"
CONTINUE_FILE="$PROJECT_ROOT/$PROJECT/continue.md"

# ==================== VALIDATION ====================
if [[ ! -d "$WORK_DIR" ]]; then
  echo "[ERROR] Directory not found: $WORK_DIR"
  exit 1
fi

# ==================== TELEGRAM ====================
send_telegram() {
  local message="$1"
  local parse_mode="${2:-HTML}"
  [[ -z "${TELEGRAM_BOT_TOKEN:-}" || -z "${TELEGRAM_CHAT_ID:-}" ]] && return 0
  curl -s --max-time 10 \
    -X POST "https://api.telegram.org/bot${TELEGRAM_BOT_TOKEN}/sendMessage" \
    -H "Content-Type: application/json" \
    -d "$(jq -n \
      --arg chat_id "$TELEGRAM_CHAT_ID" \
      --arg text "$message" \
      --arg parse_mode "$parse_mode" \
      '{chat_id: $chat_id, text: $text, parse_mode: $parse_mode, disable_web_page_preview: true}'
    )" > /dev/null 2>&1 || true
}

# ==================== RUN ====================
LOG_FILE="$LOG_DIR/${PROJECT}_subdir_${TIMESTAMP}.log"

echo "[$DATE_HUMAN] Starting subdir agent: $PROJECT_PATH" | tee -a "$LOG_DIR/scheduler.log"

# ==================== RESOLVE HINT → INSTRUCTIONS ====================
# Priority:
#   1. @file  — read named file from subdir (or project root)
#   2. "text" — use as-is
#   3. (empty) — auto-detect: AGENT.md → plan.md → continue.md

resolve_instructions() {
  local hint="$1"

  if [[ "$hint" == @* ]]; then
    # @file — strip the @ and read the file
    local fname="${hint#@}"
    # check subdir first, then project root
    for candidate in "$WORK_DIR/$fname" "$PROJECT_ROOT/$PROJECT/$fname"; do
      if [[ -f "$candidate" ]]; then
        cat "$candidate"
        return
      fi
    done
    echo "[WARN] $hint not found in $WORK_DIR or $PROJECT_ROOT/$PROJECT — falling back to continue.md" >&2
    [[ -f "$CONTINUE_FILE" ]] && cat "$CONTINUE_FILE" || echo "(no instructions found)"

  elif [[ -n "$hint" ]]; then
    # inline prompt — use directly
    echo "$hint"

  else
    # auto-detect: AGENT.md → plan.md → continue.md
    for candidate in "$WORK_DIR/AGENT.md" "$WORK_DIR/plan.md" "$CONTINUE_FILE"; do
      if [[ -f "$candidate" ]]; then
        cat "$candidate"
        return
      fi
    done
    echo "(no instructions found — add AGENT.md or plan.md to $PROJECT_PATH)"
  fi
}

INSTRUCTIONS=$(resolve_instructions "$HINT")

# Build full prompt
PROMPT="You are working on the <${PROJECT}> project, specifically in the subdirectory: ${PROJECT_PATH}

Your working directory is already set to this subdirectory — use relative paths from here.

## Instructions

${INSTRUCTIONS}

---

Rules:
- Work autonomously. Make decisions yourself unless it involves spending money or live accounts.
- Write production-quality code, not prototypes.
- Do not re-read files whose content is already above.

When done, update ${PROJECT}/continue.md with:
- What was completed this session (be specific)
- Exact next steps (so specific that future-you can start immediately)
- Any blockers or decisions needed from BiG

End with a 3-line summary of what you accomplished."

# Extract current phase for Telegram
CURRENT_PHASE=""
[[ -f "$CONTINUE_FILE" ]] && CURRENT_PHASE=$(grep -A1 "Current Phase" "$CONTINUE_FILE" 2>/dev/null | tail -1 | sed 's/^[[:space:]]*//' | head -c 80)

HINT_LABEL="${HINT:-auto}"
send_telegram "🚀 <b>${PROJECT}/${SUBDIR}</b> — Subdir agent started
📍 ${CURRENT_PHASE:-unknown phase}
📋 Instructions: ${HINT_LABEL}"

EXIT_CODE=0
START_TIME=$SECONDS
OUTPUT=$(cd "$WORK_DIR" && gtimeout "$MAX_TIMEOUT" \
  "$CLAUDE_BIN" --print "$PROMPT" \
  --allowedTools "Read,Write,Edit,Bash,Glob,Grep" \
  --max-turns 50 2>&1) || EXIT_CODE=$?
DURATION=$(( SECONDS - START_TIME ))
DURATION_MIN=$(( DURATION / 60 ))
DURATION_SEC=$(( DURATION % 60 ))

echo "$OUTPUT" > "$LOG_FILE"

if [[ $EXIT_CODE -eq 124 ]]; then
  echo "[$DATE_HUMAN] TIMEOUT: $PROJECT_PATH (${MAX_TIMEOUT}s)" | tee -a "$LOG_DIR/scheduler.log"
  send_telegram "⏰ <b>${PROJECT}/${SUBDIR}</b> — Timed out
⏱ ${DURATION_MIN}m ${DURATION_SEC}s"

elif [[ $EXIT_CODE -ne 0 ]]; then
  echo "[$DATE_HUMAN] ERROR: $PROJECT_PATH (exit $EXIT_CODE)" | tee -a "$LOG_DIR/scheduler.log"
  ERR=$(echo "$OUTPUT" | tail -5 | head -c 500 | sed 's/&/\&amp;/g; s/</\&lt;/g; s/>/\&gt;/g')
  send_telegram "❌ <b>${PROJECT}/${SUBDIR}</b> — Failed (exit ${EXIT_CODE})
⏱ ${DURATION_MIN}m ${DURATION_SEC}s
<pre>${ERR}</pre>"

else
  echo "[$DATE_HUMAN] Done: $PROJECT_PATH (${DURATION}s)" | tee -a "$LOG_DIR/scheduler.log"
  SUMMARY=$(echo "$OUTPUT" | grep -v '^$' | tail -15 | head -c 800 | sed 's/&/\&amp;/g; s/</\&lt;/g; s/>/\&gt;/g')
  NEXT_ACTION=""
  [[ -f "$CONTINUE_FILE" ]] && NEXT_ACTION=$(grep -A2 "Next Actions" "$CONTINUE_FILE" 2>/dev/null | tail -1 | sed 's/^[[:space:]]*//' | head -c 120)

  send_telegram "✅ <b>${PROJECT}/${SUBDIR}</b> — Done
⏱ ${DURATION_MIN}m ${DURATION_SEC}s

<b>Summary:</b>
<pre>${SUMMARY}</pre>

<b>Next:</b> ${NEXT_ACTION:-check continue.md}"
fi

LOG_SIZE=$(wc -c < "$LOG_FILE")
echo "[$DATE_HUMAN] Log: ${LOG_FILE##*/} (${LOG_SIZE} bytes, ${DURATION}s)" >> "$LOG_DIR/scheduler.log"

exit $EXIT_CODE

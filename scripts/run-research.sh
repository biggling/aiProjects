#!/bin/bash
# ============================================================
# Research Agent Runner
# Each project has research/AGENT.md defining what to research.
# Findings saved to research/findings/YYYY-MM-DD.md
# Send Telegram digest after each run.
#
# Usage:
#   ./run-research.sh <project>
#   ./run-research.sh all
# ============================================================

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"
ENV_FILE="$PROJECT_ROOT/.env"

[[ -f "$ENV_FILE" ]] && source "$ENV_FILE"

TELEGRAM_BOT_TOKEN="${TELEGRAM_BOT_TOKEN:-8484927192:AAHVDDU-WGsjJDOC0pSrnb_x_5RQ-mPetaQ}"
TELEGRAM_CHAT_ID="${TELEGRAM_CHAT_ID:-8532895589}"

LOG_DIR="${LOG_DIR:-$PROJECT_ROOT/logs}"
MAX_TIMEOUT="${MAX_TIMEOUT:-1800}"  # 30 min — research takes longer than work sessions
CLAUDE_BIN="${CLAUDE_BIN:-claude}"
TODAY=$(date +%Y-%m-%d)
TODAY_TIME=$(date +%Y-%m-%d_%H%M)

PROJECT="${1:-}"
TIMESTAMP=$(date +%Y%m%d_%H%M%S)
DATE_HUMAN=$(date +"%b %d %H:%M")

mkdir -p "$LOG_DIR"

VALID_PROJECTS=(
  "mcp-apps"
  "digital-products"
  "tiktok"
  "trade-auto"
  "pod"
  "micro-saas"
  "youtube-content"
  "shopee-affiliate"
  "amazon-kdp"
  "steam-game"
  "android-app"
  "polymarket"
)

# ==================== TELEGRAM ====================
send_telegram() {
  local message="$1"
  local parse_mode="${2:-HTML}"

  if [[ -z "${TELEGRAM_BOT_TOKEN:-}" || -z "${TELEGRAM_CHAT_ID:-}" ]]; then
    echo "[WARN] Telegram not configured, skipping"
    return 0
  fi

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

# ==================== RUN RESEARCH ====================
run_research() {
  local proj="$1"
  local agent_file="$PROJECT_ROOT/$proj/research/AGENT.md"
  local findings_dir="$PROJECT_ROOT/$proj/research/findings"
  local output_file="$findings_dir/${TODAY_TIME}.md"
  local latest_file="$findings_dir/latest.md"
  local log_file="$LOG_DIR/${proj}_research_${TIMESTAMP}.log"

  mkdir -p "$findings_dir"

  if [[ ! -f "$agent_file" ]]; then
    echo "[ERROR] $agent_file not found" | tee -a "$LOG_DIR/scheduler.log"
    send_telegram "❌ Research: <b>${proj}</b> — research/AGENT.md not found"
    return 1
  fi

  local agent_instructions
  agent_instructions=$(cat "$agent_file")

  local prompt
  prompt="You are a research agent for the <${proj}> project. Today is ${TODAY} (Bangkok, GMT+7).

${agent_instructions}

## Output Instructions
1. Save your complete findings to the file: ${proj}/research/findings/${TODAY_TIME}.md
2. Also write the same content to: ${proj}/research/findings/latest.md
3. Use this exact structure for the findings file:

\`\`\`
# ${proj} Research — ${TODAY_TIME}

## [Topic Section 1]
- Finding with source URL
- Finding with source URL

## [Topic Section 2]
...

## Action Items for Work Agent
- [ ] Specific action triggered by research
- [ ] Another action

## Sentiment
Overall: [Bullish / Neutral / Bearish / Opportunity / Risk]
Reasoning: one sentence
\`\`\`

4. After saving both files, print a 5-bullet summary of the most important findings to stdout."

  echo "[$DATE_HUMAN] Research starting: $proj" | tee -a "$LOG_DIR/scheduler.log"
  send_telegram "🔍 <b>Research: ${proj}</b> — Starting
📅 ${TODAY}"

  local exit_code=0
  local start_time=$SECONDS
  local output
  output=$(cd "$PROJECT_ROOT" && gtimeout "$MAX_TIMEOUT" \
    "$CLAUDE_BIN" --print "$prompt" \
    --allowedTools "Read,Write,Edit,Bash,Glob,Grep,WebSearch,WebFetch" \
    --max-turns 40 2>&1) || exit_code=$?
  local duration=$(( SECONDS - start_time ))
  local duration_min=$(( duration / 60 ))
  local duration_sec=$(( duration % 60 ))

  echo "$output" > "$log_file"

  if [[ $exit_code -eq 124 ]]; then
    echo "[$DATE_HUMAN] TIMEOUT: ${proj} research" | tee -a "$LOG_DIR/scheduler.log"
    send_telegram "⏰ <b>Research: ${proj}</b> — Timed out after ${duration_min}m"

  elif [[ $exit_code -ne 0 ]]; then
    echo "[$DATE_HUMAN] ERROR: ${proj} research (exit $exit_code)" | tee -a "$LOG_DIR/scheduler.log"
    local err
    err=$(echo "$output" | tail -4 | head -c 400 | sed 's/&/\&amp;/g; s/</\&lt;/g; s/>/\&gt;/g')
    send_telegram "❌ <b>Research: ${proj}</b> — Failed (exit ${exit_code})
<pre>${err}</pre>"

  else
    echo "[$DATE_HUMAN] Done: ${proj} research (${duration}s)" | tee -a "$LOG_DIR/scheduler.log"
    local summary
    summary=$(echo "$output" | grep -v '^$' | tail -12 | head -c 700 | sed 's/&/\&amp;/g; s/</\&lt;/g; s/>/\&gt;/g')

    # Read action items from saved findings
    local actions=""
    if [[ -f "$output_file" ]]; then
      actions=$(grep '^\- \[ \]' "$output_file" 2>/dev/null | head -3 | sed 's/- \[ \] /• /' | head -c 200 | sed 's/&/\&amp;/g; s/</\&lt;/g; s/>/\&gt;/g')
    fi

    send_telegram "📚 <b>Research: ${proj}</b> — Done ✅
⏱ ${duration_min}m ${duration_sec}s

<b>Summary:</b>
<pre>${summary}</pre>

<b>Action Items:</b>
${actions:-• See research/findings/${TODAY_TIME}.md}"
  fi

  return $exit_code
}

# ==================== RUN ALL ====================
run_all() {
  echo "[$DATE_HUMAN] Research: running all projects" | tee -a "$LOG_DIR/scheduler.log"
  send_telegram "🔄 <b>Research batch starting</b> — ${#VALID_PROJECTS[@]} projects"

  local failed=0 completed=0
  for proj in "${VALID_PROJECTS[@]}"; do
    run_research "$proj" && ((completed++)) || ((failed++))
    sleep 90   # give Anthropic API breathing room between agents
  done

  if [[ $failed -eq 0 ]]; then
    send_telegram "🎉 <b>Research batch done</b> — all ${completed} projects complete"
  else
    send_telegram "⚠️ <b>Research batch done</b>
✅ ${completed} succeeded  ❌ ${failed} failed"
  fi
}

# ==================== MAIN ====================
usage() {
  echo "Usage: $0 <project|all>"
  echo ""
  echo "Projects: ${VALID_PROJECTS[*]}"
  echo ""
  echo "Examples:"
  echo "  $0 mcp-apps"
  echo "  $0 all"
  exit 1
}

if [[ -z "$PROJECT" ]]; then
  usage
fi

if [[ "$PROJECT" == "all" ]]; then
  run_all
else
  valid=false
  for p in "${VALID_PROJECTS[@]}"; do
    [[ "$p" == "$PROJECT" ]] && valid=true && break
  done
  if [[ "$valid" != "true" ]]; then
    echo "ERROR: Unknown project '$PROJECT'"
    usage
  fi
  run_research "$PROJECT"
fi

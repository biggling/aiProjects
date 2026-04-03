#!/usr/bin/env bash
# run-research.sh — Web research agent for a project.
# Reads <project>/research/AGENT.md for the research brief,
# searches the web, and saves findings to research/findings/.
# Usage: ./scripts/run-research.sh <project|all>

set -e

WORKSPACE_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
PROJECT="${1:-}"

if [ -z "$PROJECT" ]; then
  echo "Usage: $0 <project|all>" >&2
  exit 1
fi

run_research_for_project() {
  local project="$1"
  local project_dir="$WORKSPACE_ROOT/$project"

  if [ ! -d "$project_dir" ]; then
    echo "[SKIP] $project — directory not found" >&2
    return 0
  fi

  local agent_md="$project_dir/research/AGENT.md"
  if [ ! -f "$agent_md" ]; then
    echo "[SKIP] $project — no research/AGENT.md found" >&2
    return 0
  fi

  local today
  today=$(date +%Y-%m-%d)
  local findings_dir="$project_dir/research/findings"
  local today_file="$findings_dir/${today}.md"

  # Skip if already ran today
  if [ -f "$today_file" ]; then
    echo "[SKIP] $project — research already done today ($today_file)"
    return 0
  fi

  mkdir -p "$findings_dir"
  local log_dir="$WORKSPACE_ROOT/logs"
  mkdir -p "$log_dir"
  local log_file="$log_dir/${project}_research_${today}_$(date +%H%M%S).log"

  echo "[$(date '+%H:%M:%S')] Research: $project"

  cd "$project_dir"

  AGENT_BRIEF=$(cat "$agent_md")

  PROMPT="You are a research agent for the '$project' project.

Research brief (from research/AGENT.md):
$AGENT_BRIEF

Today's date: $today

Instructions:
1. Execute all research tasks in the brief above.
2. Save your findings to: research/findings/${today}.md
3. Also overwrite: research/findings/latest.md with the same content.
4. Format findings as: date header, key findings, action items, sentiment.
5. Be specific — include URLs, numbers, names. Vague summaries are not useful.
6. End with: ## Action Items — a checklist of concrete next steps."

  claude --print "$PROMPT" \
    --allowedTools "Read,Write,Edit,Glob,Grep,WebSearch,WebFetch" \
    --max-turns 40 \
    2>&1 | tee "$log_file"

  local exit_code=${PIPESTATUS[0]}
  echo "[$(date '+%H:%M:%S')] Research done: $project (exit $exit_code)"
  return $exit_code
}

# Run all projects with a 90-second gap between each
if [ "$PROJECT" = "all" ]; then
  PROJECTS=$(ls -d "$WORKSPACE_ROOT"/*/  2>/dev/null | xargs -I{} basename {} | grep -v scripts | grep -v logs | grep -v '.git')
  FIRST=true
  for p in $PROJECTS; do
    if [ "$FIRST" = "false" ]; then
      echo "Waiting 90s before next project..."
      sleep 90
    fi
    run_research_for_project "$p"
    FIRST=false
  done
else
  run_research_for_project "$PROJECT"
fi

#!/usr/bin/env bash
# run-agent-continue.sh — Context-aware work agent.
# Inlines continue.md + latest research into the prompt at turn 0.
# Claude gets full context without spending turns reading files.
# Usage: ./scripts/run-agent-continue.sh <project|all> [focus hint]

set -e

WORKSPACE_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
PROJECT="${1:-}"
HINT="${2:-}"
MAX_CONTEXT_CHARS=4000

if [ -z "$PROJECT" ]; then
  echo "Usage: $0 <project|all> [focus hint]" >&2
  exit 1
fi

run_continue_for_project() {
  local project="$1"
  local hint="$2"
  local project_dir="$WORKSPACE_ROOT/$project"

  if [ ! -d "$project_dir" ]; then
    echo "[SKIP] $project — directory not found" >&2
    return 0
  fi

  local log_dir="$WORKSPACE_ROOT/logs"
  mkdir -p "$log_dir"
  local log_file="$log_dir/${project}_work_$(date +%Y%m%d_%H%M%S).log"

  # Load continue.md
  local continue_section=""
  if [ -f "$project_dir/continue.md" ]; then
    continue_section=$(head -c $MAX_CONTEXT_CHARS "$project_dir/continue.md")
    local size
    size=$(wc -c < "$project_dir/continue.md")
    if [ "$size" -gt "$MAX_CONTEXT_CHARS" ]; then
      continue_section="$continue_section
[... continue.md truncated. Full file at: continue.md]"
    fi
  fi

  # Load latest research
  local research_section=""
  local research_file="$project_dir/research/findings/latest.md"
  local research_age="(none)"
  if [ -f "$research_file" ]; then
    research_section=$(head -c $MAX_CONTEXT_CHARS "$research_file")
    local size
    size=$(wc -c < "$research_file")
    if [ "$size" -gt "$MAX_CONTEXT_CHARS" ]; then
      research_section="$research_section
[... research truncated. Full file at: research/findings/latest.md]"
    fi
    # Get file age
    local today
    today=$(date +%Y-%m-%d)
    local file_date
    file_date=$(date -r "$research_file" +%Y-%m-%d 2>/dev/null || echo "unknown")
    if [ "$file_date" = "$today" ]; then
      research_age="today"
    else
      research_age="$file_date"
    fi
  fi

  # Load project CLAUDE.md (capped at 2k)
  local claude_md_section=""
  if [ -f "$project_dir/CLAUDE.md" ]; then
    claude_md_section=$(head -c 2000 "$project_dir/CLAUDE.md")
  fi

  # Build focus instruction
  local focus_instruction="Continue the highest priority next task from continue.md."
  if [ -n "$hint" ]; then
    focus_instruction="Focus on: $hint"
  fi

  echo "[$(date '+%H:%M:%S')] Work agent: $project (research: $research_age)"

  PROMPT="You are working on the '$project' project.

== CONTINUE.MD ==
${continue_section:-"(no continue.md found — explore the project and create one)"}

== LATEST RESEARCH (${research_age}) ==
${research_section:-"(no research findings found)"}

== PROJECT CLAUDE.MD ==
${claude_md_section:-"(no CLAUDE.md found)"}

== TASK ==
$focus_instruction

When done:
1. Update continue.md with what was accomplished and the exact next steps.
2. Mark completed tasks [x] in continue.md.
3. Do NOT mark Daily Tasks as [x] — they repeat every session."

  cd "$project_dir"

  claude --print "$PROMPT" \
    --allowedTools "Read,Write,Edit,Bash,Glob,Grep" \
    --max-turns 50 \
    2>&1 | tee "$log_file"

  local exit_code=${PIPESTATUS[0]}
  echo "[$(date '+%H:%M:%S')] Work done: $project (exit $exit_code)"
  return $exit_code
}

if [ "$PROJECT" = "all" ]; then
  PROJECTS=$(ls -d "$WORKSPACE_ROOT"/*/  2>/dev/null | xargs -I{} basename {} | grep -v scripts | grep -v logs | grep -v '.git')
  FIRST=true
  for p in $PROJECTS; do
    if [ "$FIRST" = "false" ]; then
      echo "Waiting 30s before next project..."
      sleep 30
    fi
    run_continue_for_project "$p" "$HINT"
    FIRST=false
  done
else
  run_continue_for_project "$PROJECT" "$HINT"
fi

#!/usr/bin/env bash
# run-now.sh — Shorthand dispatcher.
# Usage:
#   ./scripts/run-now.sh research <project|all>
#   ./scripts/run-now.sh continue <project|all> [hint]
#   ./scripts/run-now.sh status

SCRIPTS_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
WORKSPACE_ROOT="$(dirname "$SCRIPTS_DIR")"
CMD="${1:-}"

case "$CMD" in
  research)
    shift
    bash "$SCRIPTS_DIR/run-research.sh" "$@"
    ;;
  continue)
    shift
    bash "$SCRIPTS_DIR/run-agent-continue.sh" "$@"
    ;;
  status)
    echo "=== Project Status ==="
    for dir in "$WORKSPACE_ROOT"/*/; do
      project=$(basename "$dir")
      [ "$project" = "scripts" ] && continue
      [ "$project" = "logs" ] && continue

      continue_file="$dir/continue.md"
      research_file="$dir/research/findings/latest.md"

      echo ""
      echo "[$project]"
      if [ -f "$continue_file" ]; then
        phase=$(grep -m1 "^## Current Phase" -A1 "$continue_file" | tail -1 | sed 's/^[#*[:space:]]*//')
        next=$(grep -m1 "^- \[ \]" "$continue_file" | sed 's/^- \[ \] //')
        echo "  Phase: ${phase:-(not set)}"
        echo "  Next:  ${next:-(no pending tasks)}"
      else
        echo "  (no continue.md)"
      fi

      if [ -f "$research_file" ]; then
        file_date=$(date -r "$research_file" +%Y-%m-%d 2>/dev/null || echo "unknown")
        today=$(date +%Y-%m-%d)
        if [ "$file_date" = "$today" ]; then
          echo "  Research: today"
        else
          echo "  Research: $file_date"
        fi
      else
        echo "  Research: none"
      fi
    done
    echo ""
    ;;
  *)
    echo "Usage: $0 <research|continue|status> [args...]" >&2
    echo ""
    echo "  $0 research <project|all>"
    echo "  $0 continue <project|all> [focus hint]"
    echo "  $0 status"
    exit 1
    ;;
esac

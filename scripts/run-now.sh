#!/bin/bash
# ============================================================
# Quick manual trigger — run from terminal or Telegram bot
# ============================================================
# Usage:
#   ./run-now.sh status
#   ./run-now.sh <project> [custom prompt]
#   ./run-now.sh all
#   ./run-now.sh research <project|all>
# ============================================================

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"
ACTION="${1:-status}"

ALL_PROJECTS="mcp-apps digital-products tiktok trade-auto pod micro-saas youtube-content shopee-affiliate amazon-kdp steam-game android-app polymarket"

case "$ACTION" in
  status)
    echo "=== PROJECT STATUS ==="
    for proj in $ALL_PROJECTS; do
      cf="$PROJECT_ROOT/$proj/continue.md"
      if [[ -f "$cf" ]]; then
        phase=$(grep -A1 "Current Phase" "$cf" | tail -1 | sed 's/^[[:space:]]*//')
        next=$(grep -A1 "Next Step" "$cf" | tail -1 | sed 's/^[[:space:]]*//')
        today=$(date +%Y-%m-%d)
        has_research="no"
        [[ -f "$PROJECT_ROOT/$proj/research/findings/$today.md" ]] && has_research="yes (today)"
        echo ""
        echo "[$proj]"
        echo "  Phase:    $phase"
        echo "  Next:     $next"
        echo "  Research: $has_research"
      fi
    done
    echo ""
    echo "=== RECENT LOGS ==="
    ls -lt "$PROJECT_ROOT/logs/"*.log 2>/dev/null | head -8 | awk '{print "  " $6, $7, $8, $9}'
    ;;

  research)
    target="${2:-all}"
    echo "Running research: $target..."
    "$SCRIPT_DIR/run-research.sh" "$target"
    ;;

  continue)
    target="${2:-all}"
    focus="${3:-}"
    echo "Running continue: $target..."
    "$SCRIPT_DIR/run-agent-continue.sh" "$target" "$focus"
    ;;

  mcp-apps|digital-products|tiktok|trade-auto|pod|micro-saas|youtube-content|shopee-affiliate|amazon-kdp|steam-game|android-app|polymarket|all)
    echo "Running $ACTION..."
    "$SCRIPT_DIR/run-agent.sh" "$ACTION" "${2:-}"
    ;;

  *)
    echo "Unknown command: $ACTION"
    echo ""
    echo "Usage:"
    echo "  $0 status"
    echo "  $0 <project> [custom prompt]        # run-agent (custom task)"
    echo "  $0 continue <project|all> [focus]   # run-agent-continue (research-aware)"
    echo "  $0 research <project|all>"
    echo "  $0 all"
    echo ""
    echo "Projects: $ALL_PROJECTS"
    exit 1
    ;;
esac

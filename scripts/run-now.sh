#!/bin/bash
# ============================================================
# Quick manual trigger — run from terminal or Telegram bot
# ============================================================
# Usage:
#   ./run-now.sh trade-auto
#   ./run-now.sh pod "Generate 10 new design concepts"
#   ./run-now.sh all
#   ./run-now.sh status
# ============================================================

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"
ACTION="${1:-status}"

case "$ACTION" in
  status)
    echo "=== PROJECT STATUS ==="
    for proj in tiktok trade-auto pod shopee-affiliate amazon-kdp steam-game android-app polymarket; do
      cf="$PROJECT_ROOT/$proj/continue.md"
      if [[ -f "$cf" ]]; then
        phase=$(grep -A1 "Current Phase" "$cf" | tail -1 | sed 's/^[[:space:]]*//')
        next=$(grep -A1 "^1\." "$cf" | head -1 | sed 's/^[[:space:]]*//')
        echo ""
        echo "[$proj]"
        echo "  Phase: $phase"
        echo "  Next:  $next"
      fi
    done
    echo ""
    echo "=== RECENT LOGS ==="
    ls -lt "$PROJECT_ROOT/logs/"*.log 2>/dev/null | head -5 | awk '{print "  " $6, $7, $8, $9}'
    ;;

  tiktok|trade-auto|pod|shopee-affiliate|amazon-kdp|steam-game|android-app|polymarket|all)
    echo "Running $ACTION..."
    "$SCRIPT_DIR/run-agent.sh" "$ACTION" "${2:-}"
    ;;

  *)
    echo "Unknown command: $ACTION"
    echo "Usage: $0 {trade-auto|pod|shopee-affiliate|amazon-kdp|steam-game|android-app|polymarket|all|status}"
    exit 1
    ;;
esac

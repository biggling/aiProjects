#!/bin/bash
# Unload and remove all aiProjects launchd agents

UID_VAL=$(id -u)
AGENTS_DIR="$HOME/Library/LaunchAgents"

echo "Uninstalling all com.big.* launchd agents..."

launchctl list | grep "com\.big\." | awk '{print $3}' | while read -r label; do
  launchctl bootout "gui/${UID_VAL}/${label}" 2>/dev/null && echo "  ✓ unloaded $label" || true
  rm -f "$AGENTS_DIR/${label}.plist" && echo "  ✓ removed ${label}.plist" || true
done

echo "Done."

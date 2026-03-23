#!/bin/bash
# ============================================================
# Install aiProjects single launchd agent
# One plist fires every :00 and :30, scheduler.sh dispatches jobs
# based on scripts/schedule.conf
#
# Usage:
#   bash scripts/install-launchd.sh
# ============================================================

set -euo pipefail

PROJ="/Users/big/Library/Mobile Documents/com~apple~CloudDocs/Fastlane/github/aiProjects"
AGENTS_DIR="$HOME/Library/LaunchAgents"
LOCAL_SCRIPTS="$HOME/scripts"
LOG_DIR="$PROJ/logs"
LABEL="com.big.aiprojects"
UID_VAL=$(id -u)

# Copy scripts to non-iCloud path (launchd cannot exec from iCloud Drive)
mkdir -p "$LOCAL_SCRIPTS" "$AGENTS_DIR" "$LOG_DIR"
cp "$PROJ/scripts/scheduler.sh"    "$LOCAL_SCRIPTS/scheduler.sh"
cp "$PROJ/scripts/run-research.sh" "$LOCAL_SCRIPTS/run-research.sh"
cp "$PROJ/scripts/run-agent.sh"    "$LOCAL_SCRIPTS/run-agent.sh"
chmod +x "$LOCAL_SCRIPTS/scheduler.sh" \
         "$LOCAL_SCRIPTS/run-research.sh" \
         "$LOCAL_SCRIPTS/run-agent.sh"

PLIST="$AGENTS_DIR/${LABEL}.plist"

cat > "$PLIST" <<PLIST
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>Label</key>
    <string>${LABEL}</string>
    <key>ProgramArguments</key>
    <array>
        <string>/bin/bash</string>
        <string>${LOCAL_SCRIPTS}/scheduler.sh</string>
    </array>
    <key>StartCalendarInterval</key>
    <array>
        <dict><key>Minute</key><integer>0</integer></dict>
        <dict><key>Minute</key><integer>30</integer></dict>
    </array>
    <key>EnvironmentVariables</key>
    <dict>
        <key>HOME</key>
        <string>/Users/big</string>
        <key>PATH</key>
        <string>/Users/big/.local/bin:/opt/homebrew/bin:/usr/local/bin:/usr/bin:/bin:/Users/big/.npm-global/bin</string>
        <key>PROJECT_ROOT</key>
        <string>${PROJ}</string>
    </dict>
    <key>StandardOutPath</key>
    <string>${LOG_DIR}/launchd.log</string>
    <key>StandardErrorPath</key>
    <string>${LOG_DIR}/launchd.log</string>
    <key>RunAtLoad</key>
    <false/>
</dict>
</plist>
PLIST

launchctl bootout "gui/${UID_VAL}/${LABEL}" 2>/dev/null || true
launchctl bootstrap "gui/${UID_VAL}" "$PLIST"

echo "✓ Installed: ${LABEL}"
echo "  Fires every :00 and :30 — schedule: $PROJ/scripts/schedule.conf"
echo ""
launchctl list | grep "$LABEL" | awk '{print "  Status: pid="$1, "exit="$2}'

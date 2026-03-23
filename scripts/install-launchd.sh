#!/bin/bash
# ============================================================
# Install all aiProjects launchd agents
# Runs as user agent — has full Keychain access (unlike cron)
#
# Usage:
#   bash scripts/install-launchd.sh          # install all
#   bash scripts/install-launchd.sh research  # research only
#   bash scripts/install-launchd.sh work      # work agents only
# ============================================================

set -euo pipefail

PROJ="/Users/big/Library/Mobile Documents/com~apple~CloudDocs/Fastlane/github/aiProjects"
AGENTS_DIR="$HOME/Library/LaunchAgents"
LOCAL_SCRIPTS="$HOME/scripts"
mkdir -p "$LOCAL_SCRIPTS"
cp "$PROJ/scripts/run-research.sh" "$LOCAL_SCRIPTS/run-research.sh"
cp "$PROJ/scripts/run-agent.sh"    "$LOCAL_SCRIPTS/run-agent.sh"
chmod +x "$LOCAL_SCRIPTS/run-research.sh" "$LOCAL_SCRIPTS/run-agent.sh"

RESEARCH_SCRIPT="$LOCAL_SCRIPTS/run-research.sh"
WORK_SCRIPT="$LOCAL_SCRIPTS/run-agent.sh"
WEEKLY_SCRIPT="$PROJ/scripts/weekly-summary.sh"
LOG_DIR="$PROJ/logs"
UID_VAL=$(id -u)

mkdir -p "$AGENTS_DIR" "$LOG_DIR"

ENV_VARS="
    <key>EnvironmentVariables</key>
    <dict>
        <key>HOME</key>
        <string>/Users/big</string>
        <key>PATH</key>
        <string>/Users/big/.local/bin:/opt/homebrew/bin:/usr/local/bin:/usr/bin:/bin:/Users/big/.npm-global/bin</string>
        <key>PROJECT_ROOT</key>
        <string>${PROJ}</string>
    </dict>"

# ============================================================
make_plist() {
  local label="$1"
  local script="$2"
  local project="$3"
  local schedule="$4"   # XML for StartCalendarInterval
  local plist="$AGENTS_DIR/${label}.plist"

  cat > "$plist" <<PLIST
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>Label</key>
    <string>${label}</string>
    <key>ProgramArguments</key>
    <array>
        <string>/bin/bash</string>
        <string>${script}</string>
        <string>${project}</string>
    </array>
    <key>StartCalendarInterval</key>
    ${schedule}${ENV_VARS}
    <key>StandardOutPath</key>
    <string>${LOG_DIR}/launchd.log</string>
    <key>StandardErrorPath</key>
    <string>${LOG_DIR}/launchd.log</string>
    <key>RunAtLoad</key>
    <false/>
</dict>
</plist>
PLIST

  launchctl bootout "gui/${UID_VAL}/${label}" 2>/dev/null || true
  launchctl bootstrap "gui/${UID_VAL}" "$plist"
  echo "  ✓ $label"
}

# Schedule helpers
at() { echo "<dict><key>Hour</key><integer>$1</integer><key>Minute</key><integer>$2</integer></dict>"; }
at_dow() { echo "<dict><key>Hour</key><integer>$1</integer><key>Minute</key><integer>$2</integer><key>Weekday</key><integer>$3</integer></dict>"; }
two_times() { echo "<array>$(at $1 $2)$(at $3 $4)</array>"; }

# ============================================================
install_research() {
  echo "Installing research agents..."

  # Top 6 — 2x daily (night + morning)
  make_plist "com.big.research.mcp-apps"         "$RESEARCH_SCRIPT" "mcp-apps"         "$(two_times 22 0  12 0)"
  make_plist "com.big.research.digital-products" "$RESEARCH_SCRIPT" "digital-products" "$(two_times 22 30 12 30)"
  make_plist "com.big.research.trade-auto"       "$RESEARCH_SCRIPT" "trade-auto"       "$(two_times 23 0  13 0)"
  make_plist "com.big.research.pod"              "$RESEARCH_SCRIPT" "pod"              "$(two_times 23 30 13 30)"
  make_plist "com.big.research.android-app"      "$RESEARCH_SCRIPT" "android-app"      "$(two_times 0  0  14 0)"
  make_plist "com.big.research.micro-saas"       "$RESEARCH_SCRIPT" "micro-saas"       "$(two_times 0  30 14 30)"

}

# ============================================================
MODE="${1:-research}"
case "$MODE" in
  research) install_research ;;
  *)        echo "Usage: $0 [research]"; exit 1 ;;
esac

echo ""
echo "Done. List loaded agents:"
launchctl list | grep "com.big\." | awk '{print "  "$3, "pid="$1}'

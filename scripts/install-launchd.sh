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
  make_plist "com.big.research.mcp-apps"         "$RESEARCH_SCRIPT" "mcp-apps"         "$(two_times 22 0  9 30)"
  make_plist "com.big.research.digital-products" "$RESEARCH_SCRIPT" "digital-products" "$(two_times 22 30 10 0)"
  make_plist "com.big.research.trade-auto"       "$RESEARCH_SCRIPT" "trade-auto"       "$(two_times 23 0  10 30)"
  make_plist "com.big.research.pod"              "$RESEARCH_SCRIPT" "pod"              "$(two_times 23 30 11 0)"
  make_plist "com.big.research.android-app"      "$RESEARCH_SCRIPT" "android-app"      "$(two_times 0  0  11 30)"
  make_plist "com.big.research.micro-saas"       "$RESEARCH_SCRIPT" "micro-saas"       "$(two_times 0  30 12 0)"

  # Bottom 6 — weekly
  make_plist "com.big.research.tiktok"           "$RESEARCH_SCRIPT" "tiktok"           "<array>$(at_dow 8 0 4)</array>"
  make_plist "com.big.research.youtube-content"  "$RESEARCH_SCRIPT" "youtube-content"  "<array>$(at_dow 9 0 4)</array>"
  make_plist "com.big.research.shopee-affiliate" "$RESEARCH_SCRIPT" "shopee-affiliate" "<array>$(at_dow 8 0 6)</array>"
  make_plist "com.big.research.amazon-kdp"       "$RESEARCH_SCRIPT" "amazon-kdp"       "<array>$(at_dow 9 0 6)</array>"
  make_plist "com.big.research.steam-game"       "$RESEARCH_SCRIPT" "steam-game"       "<array>$(at_dow 10 0 6)</array>"
  make_plist "com.big.research.polymarket"       "$RESEARCH_SCRIPT" "polymarket"       "<array>$(at_dow 8 0 0)</array>"
}

# ============================================================
install_work() {
  echo "Installing work agents..."

  make_plist "com.big.work.mcp-apps-mon"         "$WORK_SCRIPT" "mcp-apps"         "<array>$(at_dow 19 0 1)</array>"
  make_plist "com.big.work.mcp-apps-thu"         "$WORK_SCRIPT" "mcp-apps"         "<array>$(at_dow 19 0 4)</array>"
  make_plist "com.big.work.digital-products-mon" "$WORK_SCRIPT" "digital-products" "<array>$(at_dow 20 0 1)</array>"
  make_plist "com.big.work.digital-products-thu" "$WORK_SCRIPT" "digital-products" "<array>$(at_dow 20 0 4)</array>"
  make_plist "com.big.work.trade-auto-tue"       "$WORK_SCRIPT" "trade-auto"       "<array>$(at_dow 19 0 2)</array>"
  make_plist "com.big.work.trade-auto-fri"       "$WORK_SCRIPT" "trade-auto"       "<array>$(at_dow 19 0 5)</array>"
  make_plist "com.big.work.pod-tue"              "$WORK_SCRIPT" "pod"              "<array>$(at_dow 20 0 2)</array>"
  make_plist "com.big.work.pod-fri"              "$WORK_SCRIPT" "pod"              "<array>$(at_dow 20 0 5)</array>"
  make_plist "com.big.work.android-app"          "$WORK_SCRIPT" "android-app"      "<array>$(at_dow 19 0 3)</array>"
  make_plist "com.big.work.micro-saas"           "$WORK_SCRIPT" "micro-saas"       "<array>$(at_dow 21 0 3)</array>"
  make_plist "com.big.work.tiktok"               "$WORK_SCRIPT" "tiktok"           "<array>$(at_dow 20 0 3)</array>"
  make_plist "com.big.work.youtube-content"      "$WORK_SCRIPT" "youtube-content"  "<array>$(at_dow 21 0 5)</array>"
  make_plist "com.big.work.shopee-affiliate"     "$WORK_SCRIPT" "shopee-affiliate" "<array>$(at_dow 14 0 6)</array>"
  make_plist "com.big.work.amazon-kdp"           "$WORK_SCRIPT" "amazon-kdp"       "<array>$(at_dow 15 0 6)</array>"
  make_plist "com.big.work.steam-game"           "$WORK_SCRIPT" "steam-game"       "<array>$(at_dow 14 0 0)</array>"
}

# ============================================================
MODE="${1:-all}"
case "$MODE" in
  research) install_research ;;
  work)     install_work ;;
  all)      install_research; install_work ;;
  *)        echo "Usage: $0 [research|work|all]"; exit 1 ;;
esac

echo ""
echo "Done. List loaded agents:"
launchctl list | grep "com.big\." | awk '{print "  "$3, "pid="$1}'

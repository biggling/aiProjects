#!/usr/bin/env bash
# Run the Gemini trend scraper for digital products niche discovery.
# Uses the pod venv which already has google-genai installed,
# OR installs deps into a local venv if running standalone.

set -euo pipefail
cd "$(dirname "$0")"

POD_VENV="../pod/venv/bin/python"
MCP_VENV="../mcp-apps/venv/bin/python"
LOCAL_VENV="venv/bin/python"

if [[ -x "$POD_VENV" ]]; then
  PYTHON="$POD_VENV"
elif [[ -x "$MCP_VENV" ]]; then
  PYTHON="$MCP_VENV"
elif [[ -x "$LOCAL_VENV" ]]; then
  PYTHON="$LOCAL_VENV"
else
  echo "No venv found. Creating one and installing deps..."
  python3 -m venv venv
  venv/bin/pip install -q google-genai python-dotenv
  PYTHON="$LOCAL_VENV"
fi

echo "Using: $PYTHON"
"$PYTHON" -m tools.gemini_trend_scraper "$@"

#!/bin/bash
# Test script — verify claude works via cron using Python subprocess
# Triggered every 2 minutes, logs result to logs/cron-test.log

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"
LOG="$PROJECT_ROOT/logs/cron-test.log"

python3 - "$PROJECT_ROOT" "$LOG" <<'EOF'
import subprocess
import sys
import os
from datetime import datetime

project_root = sys.argv[1]
log_path = sys.argv[2]
timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

def log(msg):
    with open(log_path, "a") as f:
        f.write(f"[{timestamp}] {msg}\n")

log("--- test start ---")
log(f"PATH={os.environ.get('PATH', 'not set')}")

# Step 1: find claude binary
check_cmd = subprocess.run(
    ["which", "claude"],
    capture_output=True,
    text=True
)
claude_cmd = check_cmd.stdout.strip()

# fallback to known locations
if not claude_cmd:
    for p in ["/Users/big/.local/bin/claude", "/usr/local/bin/claude", "/opt/homebrew/bin/claude"]:
        if os.path.isfile(p) and os.access(p, os.X_OK):
            claude_cmd = p
            break

log(f"which claude={claude_cmd or 'NOT FOUND'}")

if not claude_cmd:
    log("ERROR: claude not found in PATH or known locations")
    log("--- test end ---")
    sys.exit(1)

# Step 2: run claude via subprocess
result = subprocess.run(
    [claude_cmd, "--print", "reply with just: OK", "--max-turns", "1"],
    capture_output=True,
    text=True
)

log(f"exit={result.returncode}")
log(f"stdout={result.stdout.strip()}")
if result.stderr.strip():
    log(f"stderr={result.stderr.strip()}")


# Call Claude CLI
log_message("Calling local Claude CLI for research...")
#response = call_claude_cli(research_request, config)
log("--- test end ---")
EOF

#Resume this session with:
#claude --resume de0f4a41-1ae4-41b4-ba05-984d28388b37
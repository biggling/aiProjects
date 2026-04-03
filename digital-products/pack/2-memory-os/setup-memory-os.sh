#!/usr/bin/env bash
# setup-memory-os.sh
# Run once from your project root to create the memory-bank/ directory.
# Usage: bash setup-memory-os.sh

set -e

PROJECT_ROOT="$(pwd)"
MEMORY_DIR="$PROJECT_ROOT/memory-bank"
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

echo "Setting up Memory OS in: $PROJECT_ROOT"

if [ -d "$MEMORY_DIR" ]; then
  echo "memory-bank/ already exists. Skipping creation."
  echo "To reset, delete memory-bank/ and re-run this script."
  exit 0
fi

mkdir -p "$MEMORY_DIR"

# Copy templates
cp "$SCRIPT_DIR/projectBrief.md"   "$MEMORY_DIR/projectBrief.md"
cp "$SCRIPT_DIR/activeContext.md"  "$MEMORY_DIR/activeContext.md"
cp "$SCRIPT_DIR/progress.md"       "$MEMORY_DIR/progress.md"
cp "$SCRIPT_DIR/systemPatterns.md" "$MEMORY_DIR/systemPatterns.md"

echo ""
echo "✓ Created memory-bank/ with 4 files:"
echo "  memory-bank/projectBrief.md"
echo "  memory-bank/activeContext.md"
echo "  memory-bank/progress.md"
echo "  memory-bank/systemPatterns.md"
echo ""
echo "Next steps:"
echo ""
echo "1. Add this block to your project's CLAUDE.md:"
echo ""
echo "   ## Memory OS"
echo "   At session start: read ALL files in memory-bank/ before doing anything else."
echo "   At session end: update memory-bank/activeContext.md and memory-bank/progress.md."
echo "   Never truncate existing content — append only. Keep each file under 200 lines."
echo ""
echo "2. Fill in memory-bank/projectBrief.md with your project details."
echo "   (The other files can start empty — Claude will populate them.)"
echo ""
echo "3. Start a Claude Code session. Claude will read the files automatically."

#!/usr/bin/env bash
# weekly-summary.sh — Cross-project weekly digest.
# Reads all continue.md files and generates a summary.
# Usage: ./scripts/weekly-summary.sh

set -e

WORKSPACE_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
WEEK=$(date +%Y-W%V)
OUTPUT_FILE="$WORKSPACE_ROOT/logs/weekly-summary-${WEEK}.md"
mkdir -p "$WORKSPACE_ROOT/logs"

echo "Generating weekly summary for $WEEK..."

# Collect all continue.md content
CONTEXT=""
for dir in "$WORKSPACE_ROOT"/*/; do
  project=$(basename "$dir")
  [ "$project" = "scripts" ] && continue
  [ "$project" = "logs" ] && continue

  continue_file="$dir/continue.md"
  if [ -f "$continue_file" ]; then
    CONTEXT="$CONTEXT

=== $project/continue.md ===
$(head -c 2000 "$continue_file")"
  fi
done

PROMPT="Generate a weekly summary for a solo developer's side projects.

Today: $(date '+%Y-%m-%d (%A)')
Week: $WEEK

Project states (from continue.md files):
$CONTEXT

Write a concise weekly summary with these sections:
1. **This Week's Wins** — what got shipped or completed
2. **In Progress** — what's actively being worked on
3. **Blocked** — what's stuck and why
4. **Next Week's Focus** — top 3 priorities (be specific)
5. **Revenue Status** — any income, any close to revenue

Keep it under 400 words. Be direct, no fluff."

claude --print "$PROMPT" \
  --allowedTools "Read" \
  --max-turns 5 \
  2>&1 | tee "$OUTPUT_FILE"

echo ""
echo "Summary saved to: $OUTPUT_FILE"

# Agent Usage Examples

## Overview

Three agent scripts, each with a different purpose:

| Script | Purpose | Tools | When |
|--------|---------|-------|------|
| `run-research.sh` | Web research → saves findings | WebSearch, WebFetch, Read, Write | Morning |
| `run-agent.sh` | Custom task with a prompt | Read, Write, Edit, Bash, Glob, Grep | Any time |
| `run-agent-continue.sh` | Continue work, auto-injects research context | Read, Write, Edit, Bash, Glob, Grep | Evening |

`run-agent-continue.sh` vs `run-agent.sh`:
- **continue**: inlines `continue.md` + `research/findings/latest.md` directly into the prompt — agent has full context in turn 0, no file-read overhead
- **agent**: takes a custom prompt, doesn't auto-load research

---

## Run Research — All Projects

```bash
# Run research for one project
./scripts/run-research.sh mcp-apps
./scripts/run-research.sh digital-products
./scripts/run-research.sh tiktok
./scripts/run-research.sh trade-auto
./scripts/run-research.sh pod
./scripts/run-research.sh micro-saas
./scripts/run-research.sh youtube-content
./scripts/run-research.sh shopee-affiliate
./scripts/run-research.sh amazon-kdp
./scripts/run-research.sh steam-game
./scripts/run-research.sh android-app
./scripts/run-research.sh polymarket

# Run all 12 in sequence (90s gap between each)
./scripts/run-research.sh all

# Via run-now shorthand
./scripts/run-now.sh research mcp-apps
./scripts/run-now.sh research all
```

What the research agent does per project:
- Reads `<project>/research/AGENT.md` for its search brief
- Searches the web and fetches relevant pages
- Saves findings → `<project>/research/findings/YYYY-MM-DD.md`
- Overwrites `<project>/research/findings/latest.md`
- Sends a Telegram digest with key findings and action items
- Skips if today's findings already exist (safe to re-run)

---

## Continue Work (Research-Aware) — All Projects

`run-agent-continue.sh` automatically inlines `continue.md` + `research/findings/latest.md`
into the prompt. The agent sees full context from turn 0 with no extra file-read turns.

```bash
# Basic continue — picks up from continue.md, uses latest research automatically
./scripts/run-agent-continue.sh mcp-apps
./scripts/run-agent-continue.sh digital-products
./scripts/run-agent-continue.sh tiktok
./scripts/run-agent-continue.sh trade-auto
./scripts/run-agent-continue.sh pod
./scripts/run-agent-continue.sh micro-saas
./scripts/run-agent-continue.sh youtube-content
./scripts/run-agent-continue.sh shopee-affiliate
./scripts/run-agent-continue.sh amazon-kdp
./scripts/run-agent-continue.sh steam-game
./scripts/run-agent-continue.sh android-app
./scripts/run-agent-continue.sh polymarket

# With an optional focus hint (overrides "next task" default)
./scripts/run-agent-continue.sh mcp-apps       "focus on the Stripe billing integration"
./scripts/run-agent-continue.sh digital-products "write the Gumroad product description"
./scripts/run-agent-continue.sh trade-auto     "tune momentum strategy parameters based on research"
./scripts/run-agent-continue.sh tiktok         "fix the thumbnail generator aspect ratio bug"
./scripts/run-agent-continue.sh pod            "generate 5 designs for the niche found in research"
./scripts/run-agent-continue.sh micro-saas     "scaffold the Go backend for Shopee analytics MVP"
./scripts/run-agent-continue.sh shopee-affiliate "write 3 Thai product review posts for this week's campaign"
./scripts/run-agent-continue.sh amazon-kdp     "generate 3 planner interiors for the top KDP niche"
./scripts/run-agent-continue.sh steam-game     "implement the sigil unlock tree from research player feedback"
./scripts/run-agent-continue.sh android-app    "build the usage stats reader using the Android UsageStatsManager API"
./scripts/run-agent-continue.sh polymarket     "find markets where price differs >8% from Kalshi"

# Run all projects in priority order (30s gap between each)
./scripts/run-agent-continue.sh all

# Via run-now shorthand
./scripts/run-now.sh continue mcp-apps
./scripts/run-now.sh continue mcp-apps "focus on Stripe billing"
./scripts/run-now.sh continue all
```

What happens inside each run:
1. Reads `<project>/continue.md` — full content inlined
2. Reads `<project>/research/findings/latest.md` — inlined (capped at 4k chars)
3. Reads `<project>/CLAUDE.md` if it exists — inlined (capped at 2k chars)
4. Runs the work agent with all context already in the prompt
5. Telegram notification shows research age (today / yesterday / N days ago)
6. Updates `continue.md` with what was done and exact next steps

---

## Custom Task (No Research Context) — All Projects

### 1. mcp-apps
```bash
# Interactive
cd mcp-apps && claude

# Non-interactive (cron-style)
./scripts/run-agent.sh mcp-apps

# With custom prompt
./scripts/run-agent.sh mcp-apps "scaffold a TypeScript MCP server with one tool: get_portfolio_value(coins[])"

# Read today's research first, then build
./scripts/run-agent.sh mcp-apps "read research/findings/latest.md for market context, then continue work from continue.md"
```

### 2. digital-products
```bash
cd digital-products && claude

./scripts/run-agent.sh digital-products

# Specific tasks
./scripts/run-agent.sh digital-products "package the CLAUDE.md agent configs into a ZIP with README, price at \$9"
./scripts/run-agent.sh digital-products "write 3 product descriptions for Gumroad based on research/findings/latest.md"
```

### 3. tiktok
```bash
cd tiktok && claude

./scripts/run-agent.sh tiktok

# Pipeline-specific
./scripts/run-agent.sh tiktok "run the daily pipeline: research → scriptgen → voiceover → videogen"
./scripts/run-agent.sh tiktok "read research/findings/latest.md and add top 3 trending products to the research DB"
./scripts/run-agent.sh tiktok "fix the thumbnail generator aspect ratio bug and add a test"
```

### 4. trade-auto
```bash
cd trade-auto && claude

./scripts/run-agent.sh trade-auto

# Strategy work
./scripts/run-agent.sh trade-auto "download latest OHLCV data for BTC/ETH and run all 3 backtests"
./scripts/run-agent.sh trade-auto "read research/findings/latest.md for market regime, then tune momentum strategy params"
./scripts/run-agent.sh trade-auto "implement the RSI divergence strategy from src/strategies/ and add backtest"
```

### 5. pod
```bash
cd pod && claude

./scripts/run-agent.sh pod

# Design and listing work
./scripts/run-agent.sh pod "generate 5 new t-shirt designs based on trending themes in research/findings/latest.md"
./scripts/run-agent.sh pod "run integration tests and fix any failures"
./scripts/run-agent.sh pod "create Printify listings for the 3 newest designs in designs/"
```

### 6. micro-saas
```bash
cd micro-saas && claude

./scripts/run-agent.sh micro-saas

# Validation first, then build
./scripts/run-agent.sh micro-saas "read research/findings/latest.md and draft 5 cold outreach messages to validate Shopee analytics idea"
./scripts/run-agent.sh micro-saas "scaffold a Go backend with Postgres for the Shopee seller dashboard MVP"
./scripts/run-agent.sh micro-saas "build the landing page with waitlist form — deploy to Railway"
```

### 7. youtube-content
```bash
cd youtube-content && claude

./scripts/run-agent.sh youtube-content

# Content planning
./scripts/run-agent.sh youtube-content "read research/findings/latest.md and create a 4-video content calendar for next month"
./scripts/run-agent.sh youtube-content "write a YouTube description + tags for the MCP server tutorial video"
./scripts/run-agent.sh youtube-content "draft affiliate link list for the video description based on research/findings/latest.md"
```

### 8. shopee-affiliate
```bash
cd shopee-affiliate && claude

./scripts/run-agent.sh shopee-affiliate

# Content pipeline
./scripts/run-agent.sh shopee-affiliate "read research/findings/latest.md and write 3 Thai-language product review posts for top trending categories"
./scripts/run-agent.sh shopee-affiliate "build the content generation pipeline: niche → copy → affiliate link → schedule"
./scripts/run-agent.sh shopee-affiliate "create a campaign content pack for the upcoming Shopee double-day sale"
```

### 9. amazon-kdp
```bash
cd amazon-kdp && claude

./scripts/run-agent.sh amazon-kdp

# Book production
./scripts/run-agent.sh amazon-kdp "read research/findings/latest.md and generate 3 planner interiors for the top niche found"
./scripts/run-agent.sh amazon-kdp "build the cover generator using Pillow — output 6x9 and 8.5x11 variants"
./scripts/run-agent.sh amazon-kdp "add 5 new planner templates to the interior generator and export as PDFs"
```

### 10. steam-game
```bash
cd steam-game && claude

./scripts/run-agent.sh steam-game

# Godot development
./scripts/run-agent.sh steam-game "implement the core slot reel spin mechanic in Godot 4 — reels should cascade and stop one by one"
./scripts/run-agent.sh steam-game "read research/findings/latest.md for player feedback from similar games, then design the first 3 sigil types"
./scripts/run-agent.sh steam-game "build the roguelike progression system: round counter, score multiplier, sigil unlock tree"
```

### 11. android-app
```bash
cd android-app && claude

./scripts/run-agent.sh android-app

# Kotlin/Compose development
./scripts/run-agent.sh android-app "scaffold the Kotlin/Compose project with Navigation, ViewModel, and Room dependencies"
./scripts/run-agent.sh android-app "implement the QuickBlock core feature: usage stats reader + per-app time limit setter"
./scripts/run-agent.sh android-app "read research/findings/latest.md for competitor gaps, then add the most-requested missing feature"
```

### 12. polymarket
```bash
cd polymarket && claude

./scripts/run-agent.sh polymarket

# Data and analysis
./scripts/run-agent.sh polymarket "run the data collector and pull today's top 50 markets by volume"
./scripts/run-agent.sh polymarket "read research/findings/latest.md and identify markets where Polymarket price differs >8% from Kalshi"
./scripts/run-agent.sh polymarket "analyze last 30 days of collected data — find categories where crowd is systematically biased"
```

---

## Check Status
```bash
# See all 12 projects: phase, next step, whether today's research is done
./scripts/run-now.sh status
```

Output looks like:
```
[mcp-apps]
  Phase:    Phase 1 — Scaffold first MCP server
  Next:     Read Anthropic MCP SDK docs
  Research: yes (today)

[digital-products]
  Phase:    Phase 1 — Package configs → Gumroad
  Next:     Create product ZIP with README
  Research: no
```

---

## Workflow: Research → Work (same day)

```bash
# Morning: research runs automatically via cron at 08:00
# Or trigger manually:
./scripts/run-now.sh research mcp-apps

# Evening: work agent reads latest.md automatically if prompted
./scripts/run-agent.sh mcp-apps "read research/findings/latest.md for market context, then continue from continue.md"

# Or let the default work agent run — it will use continue.md
# (work agent does NOT read research automatically unless told to)
./scripts/run-agent.sh mcp-apps
```

---

## continue.md — Recurring Daily Tasks Pattern

The agent reads `continue.md` at the start of every session. By adding a
**Daily Tasks** section, you guarantee those tasks run on every work session
without having to remember to ask for them.

### Template structure

```markdown
# <Project> — Continue

## Daily Tasks  ← agent always runs these first, every session
- [ ] <repeating task 1>
- [ ] <repeating task 2>
- [ ] <repeating task 3>

## Current Phase
Phase N — short description

## One-Time Next Steps  ← agent picks the top unchecked item
- [ ] specific task A
- [ ] specific task B
- [x] completed task C

## Notes / Blockers
- any context the agent needs to know
```

The agent instruction in `run-agent-continue.sh` says:
> "Continue the highest priority next task from continue.md"

So put **Daily Tasks first** — the agent will always run them before moving to
one-time steps.

---

### Example: mcp-apps/continue.md with daily research loop

```markdown
# mcp-apps — Continue

## Daily Tasks
- [ ] Search "new MCP server launched site:github.com" — log any in research/ideas.md
- [ ] Check https://glama.ai/mcp/servers for newly listed servers, note gaps
- [ ] Review research/findings/latest.md action items — pick one to act on today

## Current Phase
**Phase 2** — Building crypto portfolio tracker MCP server

## One-Time Next Steps
- [ ] Add get_portfolio_value() tool to the MCP server
- [ ] Write README with install + usage instructions
- [ ] Set up Stripe payment link via Gumroad
- [x] Scaffold TypeScript MCP server with MCP SDK

## Blockers
- Need to decide: remote HTTP SSE vs local stdio — check community preference first
```

---

### Example: digital-products/continue.md with daily idea capture

```markdown
# digital-products — Continue

## Daily Tasks
- [ ] Search Gumroad "developer" sorted by popular — log any new products to research/ideas.md
- [ ] Check Etsy "notion template" new listings — note pricing and format trends
- [ ] Write one product description draft (even rough) and save to drafts/

## Current Phase
**Phase 1** — Packaging Claude Code agent configs for Gumroad

## One-Time Next Steps
- [ ] Create ZIP of CLAUDE.md configs with README
- [ ] Set up Gumroad product page at $9
- [ ] Design cover image in Canva (1280x720)
- [x] Identify first product: Claude Code agent config pack
```

---

### Example: trade-auto/continue.md with daily market check

```markdown
# trade-auto — Continue

## Daily Tasks
- [ ] Fetch BTC/ETH 24h price change — log to data/daily_market.csv
- [ ] Check if any open position hits stop-loss threshold — alert if so
- [ ] Run strategy health check: python src/health_check.py

## Current Phase
**Phase 2** — Backtesting momentum strategy on 2023-2024 data

## One-Time Next Steps
- [ ] Fix grid level overlap bug when range_pct < 0.02
- [ ] Add Bybit paper trading connector
- [ ] Write backtest report for momentum strategy
- [x] Implement 3 base strategies (momentum, mean-reversion, grid)
```

---

### Example: shopee-affiliate/continue.md with daily content output

```markdown
# shopee-affiliate — Continue

## Daily Tasks
- [ ] Write 1 Thai product review post → save to content/drafts/YYYY-MM-DD.md
- [ ] Pull today's Shopee TH trending products — log top 5 to research/trending.md
- [ ] Check if any scheduled post needs affiliate links updated

## Current Phase
**Phase 2** — Building content generation pipeline

## One-Time Next Steps
- [ ] Build content/generator.py: niche → draft → affiliate link insert
- [ ] Set up LINE Official Account for distribution
- [ ] Create content calendar for April double-day campaigns
- [x] Niche research complete — beauty + home appliances selected
```

---

### How the agent handles checkboxes

The agent does **not** permanently check off Daily Tasks — it runs them and
leaves them unchecked so they repeat next session. One-Time Next Steps get
checked `[x]` when complete.

To make this explicit, add a note at the top of the Daily Tasks section:

```markdown
## Daily Tasks  (reset each session — do not mark [x])
- [ ] ...
```

---

## Non-Interactive (--print) Mode

```bash
# Basic task, exit when done
claude --print "read continue.md and work on next actions" \
  --allowedTools "Read,Write,Edit,Bash,Glob,Grep" \
  --max-turns 50

# Research mode (adds web tools)
claude --print "read mcp-apps/research/AGENT.md and execute all research tasks" \
  --allowedTools "Read,Write,Edit,Bash,Glob,Grep,WebSearch,WebFetch" \
  --max-turns 40

# Save output to log
claude --print "read continue.md and work on next actions" \
  --allowedTools "Read,Write,Edit,Bash,Glob,Grep" \
  --max-turns 50 \
  2>&1 | tee "logs/session_$(date +%Y%m%d_%H%M).log"
```

---

## Tips

```bash
# Preview what Claude would do — no changes made
claude "read continue.md and list what you would do next. Don't make any changes."

# Limit scope for small tasks
claude --print "..." --max-turns 20   # small fix
claude --print "..." --max-turns 50   # feature work
claude --print "..." --max-turns 100  # full pipeline run

# Run two projects in parallel (separate terminals)
# Terminal 1:
./scripts/run-agent.sh mcp-apps
# Terminal 2:
./scripts/run-agent.sh digital-products

# Re-run research even if today's file exists (force)
rm mcp-apps/research/findings/$(date +%Y-%m-%d).md
./scripts/run-research.sh mcp-apps

# Read latest research findings manually
cat mcp-apps/research/findings/latest.md
```

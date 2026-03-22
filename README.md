# BiG's Side Projects

AI-assisted side projects aimed at building passive/semi-passive income streams. Claude agents work autonomously across all 12 projects with minimal human oversight (<5 hours/week total).

## Projects

| # | Project | Description | Tier | Status |
|---|---------|-------------|------|--------|
| 1 | [mcp-apps](./mcp-apps/) | Niche MCP server products for Claude/ChatGPT marketplaces ($10-50/mo) | HIGH | 🆕 New |
| 2 | [digital-products](./digital-products/) | Gumroad/Etsy digital downloads — templates, prompt packs, configs (90%+ margin) | HIGH | 🆕 New |
| 3 | [tiktok](./tiktok/) | TikTok/Reels/Shorts affiliate automation — 10 videos/week | — | 🟡 Active |
| 4 | [trade-auto](./trade-auto/) | Crypto trading bots (momentum, mean-reversion, grid) | — | 🟡 Active |
| 5 | [pod](./pod/) | Etsy print-on-demand — Gen Z niche designs | — | 🟡 Active |
| 6 | [micro-saas](./micro-saas/) | Focused software for Thai market (Shopee seller analytics first) | GOOD | 🆕 New |
| 7 | [youtube-content](./youtube-content/) | Dev tutorial YouTube channel — recorded during normal work sessions | GOOD | 🆕 New |
| 8 | [shopee-affiliate](./shopee-affiliate/) | Shopee affiliate marketing (Thailand) | — | 🟡 Active |
| 9 | [amazon-kdp](./amazon-kdp/) | Kindle Direct Publishing — low-content books and planners | — | 🟡 Active |
| 10 | [steam-game](./steam-game/) | Indie game on Steam — Sigil Spin (Godot 4, slot-roguelike) | — | 🟡 Active |
| 11 | [android-app](./android-app/) | Play Store apps — QuickBlock focus/productivity app | — | 🟡 Active |
| 12 | [polymarket](./polymarket/) | Prediction market trading bot | — | 🟡 Active |

## How It Works

Three agent types run on a cron schedule. Each project has its own config for all three.

```
Morning 08:00  →  run-research.sh      Web search + analysis → research/findings/YYYY-MM-DD.md
Evening 19:00  →  run-agent-continue.sh  Inlines research + continue.md → builds, codes, ships
Any time       →  run-agent.sh         Custom one-off task with a prompt
```

Each project maintains:

```
project/
├── continue.md              # Session state — phase, next steps, blockers
│                            # Includes "Daily Tasks" that repeat every session
├── CLAUDE.md                # Project-specific instructions (if present)
└── research/
    ├── AGENT.md             # What the research agent searches for
    └── findings/
        ├── YYYY-MM-DD.md    # Dated research output
        └── latest.md        # Always points to most recent findings
```

### continue.md — Daily Tasks Pattern

A project's `continue.md` can include a **Daily Tasks** section that the agent
always runs before one-time work. This enables recurring loops like idea research,
market checks, or content drafts without any human prompt.

```markdown
## Daily Tasks  (reset each session — do not mark [x])
- [ ] Search for new competitor products, log to research/ideas.md
- [ ] Check trending categories, note opportunities
- [ ] Write one draft output (post, design brief, etc.)

## One-Time Next Steps
- [ ] Build feature X
- [x] Completed task Y
```

## Scripts

| Script | What it does |
|--------|-------------|
| `scripts/run-research.sh <project\|all>` | Research agent — web search, saves findings, Telegram digest |
| `scripts/run-agent-continue.sh <project\|all> [focus]` | Continue agent — inlines research + continue.md into prompt |
| `scripts/run-agent.sh <project\|all> [prompt]` | Work agent — custom task prompt |
| `scripts/run-now.sh <command>` | Manual trigger shorthand for all of the above |
| `scripts/weekly-summary.sh` | Sunday digest of all 12 projects to Telegram |

```bash
# Quick commands
./scripts/run-now.sh status                        # all projects: phase + research status
./scripts/run-now.sh research mcp-apps             # run research for one project
./scripts/run-now.sh continue mcp-apps             # continue work (uses latest research)
./scripts/run-now.sh continue mcp-apps "focus on X" # continue with focus hint
./scripts/run-now.sh research all                  # research all 12 projects
./scripts/run-now.sh continue all                  # continue all 12 projects
```

See [example.md](./example.md) for full usage examples and `continue.md` templates.

## Cron Schedule

```
Mon  08:00  research: mcp-apps          19:00  work: mcp-apps
     09:00  research: micro-saas        20:00  work: digital-products
Tue  08:00  research: digital-products  19:00  work: tiktok
     09:00  research: youtube-content   20:00  work: trade-auto
Wed  08:00  research: tiktok            20:00  work: pod
     09:00  research: shopee-affiliate  21:00  work: micro-saas
Thu  08:00  research: trade-auto        19:00  work: mcp-apps (2nd)
     09:00  research: pod               20:00  work: digital-products (2nd)
Fri  08:00  research: micro-saas        19:00  work: tiktok (2nd)
                                        20:00  work: trade-auto (2nd)
                                        21:00  work: youtube-content
Sat  08:00  research: amazon-kdp        14:00  work: shopee-affiliate
     09:00  research: steam-game        15:00  work: amazon-kdp
     10:00  research: android-app       16:00  work: android-app
Sun  08:00  research: polymarket        14:00  work: steam-game
                                        21:00  weekly summary → Telegram
```

## Stack

- **MCP Servers**: TypeScript, MCP SDK, Cloudflare Workers / Railway
- **Automation**: Python, FastAPI, Celery, Redis
- **Trading**: Python / Go, Binance API, Bybit API
- **Video**: FFmpeg, ElevenLabs, Runway / Kling
- **SaaS**: Go, Postgres, Stripe
- **Game**: Godot 4
- **Mobile**: Android (Kotlin + Jetpack Compose)
- **Notifications**: Telegram Bot API
- **Infra**: Mac Mini + VPS (cron-scheduled agents)

## Constraints

- < 5 hours/week human time across all 12 projects
- Free tools preferred until revenue justifies paid
- Bangkok, Thailand (GMT+7)
- Make decisions autonomously unless it involves money or live-account strategy

## Status Board

See [STATUS.md](./STATUS.md) for the live cross-project status board and revenue tracker.

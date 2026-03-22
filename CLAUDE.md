# BiG's Side Projects Workspace

## Quick Start
```bash
# Work on a specific project (run from project directory):
cd mcp-apps && claude        # NEW — HIGH priority
cd digital-products && claude # NEW — HIGH priority
cd tiktok && claude
cd trade-auto && claude
cd pod && claude
cd micro-saas && claude      # NEW — GOOD priority
cd youtube-content && claude # NEW — GOOD priority
cd shopee-affiliate && claude
cd amazon-kdp && claude
cd steam-game && claude
cd android-app && claude
cd polymarket && claude
```

## Structure
```
aiProjects/
├── CLAUDE.md               # This file — workspace-level instructions
├── STATUS.md               # Cross-project status board
├── scripts/                # Crontab runner, weekly summary, manual triggers
│   ├── run-agent.sh
│   ├── run-now.sh
│   ├── weekly-summary.sh
│   └── crontab.conf
├── mcp-apps/               # Priority 1 — MCP server products (HIGH conviction)
│   └── continue.md
├── digital-products/       # Priority 2 — Gumroad/Etsy digital downloads (HIGH conviction)
│   └── continue.md
├── tiktok/                 # Priority 3 — TikTok/Reels/Shorts affiliate automation
│   ├── CLAUDE.md
│   ├── plan.md
│   ├── continue.md
│   ├── modules/            # Pipeline: research → script → voice → video → publish
│   ├── api/
│   ├── dashboard/
│   ├── scheduler/
│   └── tests/
├── trade-auto/             # Priority 4 — Crypto trading bots
│   ├── continue.md
│   ├── src/
│   ├── backtests/
│   └── docs/
├── pod/                    # Priority 5 — Etsy print on demand
│   ├── continue.md
│   ├── designs/
│   ├── listings/
│   └── scripts/
├── micro-saas/             # Priority 6 — Micro-SaaS (GOOD fit)
│   └── continue.md
├── youtube-content/        # Priority 7 — Dev tutorial YouTube channel (GOOD fit)
│   └── continue.md
├── shopee-affiliate/       # Priority 8 — Shopee affiliate (Thailand)
│   ├── continue.md
│   ├── src/
│   ├── content/
│   ├── research/
│   └── campaigns/
├── amazon-kdp/             # Priority 9 — Kindle Direct Publishing
│   ├── continue.md
│   ├── src/
│   ├── books/
│   ├── covers/
│   ├── research/
│   └── templates/
├── steam-game/             # Priority 10 — Indie game on Steam
│   ├── continue.md
│   ├── godot/
│   ├── docs/
│   ├── assets/
│   └── data/
├── android-app/            # Priority 11 — Play Store apps
│   ├── continue.md
│   ├── app/
│   └── docs/
└── polymarket/             # Priority 12 — Prediction market bot
    ├── continue.md
    ├── src/
    ├── data/
    └── analysis/
```

## Rules for All Agents
- ALWAYS read `continue.md` (and project `CLAUDE.md` if present) before starting work
- ALWAYS update `continue.md` before ending a session
- Ship fast, iterate later — BiG has < 5 hours/week total
- Make decisions autonomously unless it involves money or live-account strategy
- Write production code, not prototypes
- Use free tools/APIs until revenue justifies paid ones
- Update `STATUS.md` at the workspace root when project phase or status changes

## BiG's Context
- Based in Bangkok, Thailand (GMT+7)
- Full-time software developer (limited side project time)
- Experience: Go, Java, Python, Node.js, iOS, microservices, K8s
- Has: Mac Mini, VPS, Claude Pro subscription
- Goal: Build multiple passive/semi-passive income streams

# BiG's Side Projects Workspace

## Quick Start
```bash
# Work on a specific project (run from project directory):
cd mcp-apps && claude         # Priority 1 — HIGH
cd digital-products && claude # Priority 2 — HIGH
cd trade-auto && claude       # Priority 3
cd pod && claude              # Priority 4
cd android-app && claude      # Priority 5
cd micro-saas && claude       # Priority 6
cd tiktok && claude           # Priority 7
cd youtube-content && claude  # Priority 8
cd shopee-affiliate && claude # Priority 9
cd amazon-kdp && claude       # Priority 10
cd steam-game && claude       # Priority 11
cd polymarket && claude       # Priority 12
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
├── trade-auto/             # Priority 3 — Crypto trading bots
│   ├── continue.md
│   ├── src/
│   ├── backtests/
│   └── docs/
├── pod/                    # Priority 4 — Etsy print on demand
│   ├── continue.md
│   ├── designs/
│   ├── listings/
│   └── scripts/
├── android-app/            # Priority 5 — Play Store apps
│   ├── continue.md
│   ├── app/
│   └── docs/
├── micro-saas/             # Priority 6 — Micro-SaaS
│   └── continue.md
├── tiktok/                 # Priority 7 — TikTok/Reels/Shorts affiliate automation
│   ├── CLAUDE.md
│   ├── plan.md
│   ├── continue.md
│   ├── modules/            # Pipeline: research → script → voice → video → publish
│   ├── api/
│   ├── dashboard/
│   ├── scheduler/
│   └── tests/
├── youtube-content/        # Priority 8 — Dev tutorial YouTube channel
│   └── continue.md
├── shopee-affiliate/       # Priority 9 — Shopee affiliate (Thailand)
│   ├── continue.md
│   ├── src/
│   ├── content/
│   ├── research/
│   └── campaigns/
├── amazon-kdp/             # Priority 10 — Kindle Direct Publishing
│   ├── continue.md
│   ├── src/
│   ├── books/
│   ├── covers/
│   ├── research/
│   └── templates/
├── steam-game/             # Priority 11 — Indie game on Steam
│   ├── continue.md
│   ├── godot/
│   ├── docs/
│   ├── assets/
│   └── data/
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

# BiG's Side Projects Workspace

## Quick Start
```bash
# Work on a specific project (run from project directory):
cd tiktok && claude
cd trade-auto && claude
cd pod && claude
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
├── tiktok/                 # Priority 1 — TikTok/Reels/Shorts affiliate automation
│   ├── CLAUDE.md
│   ├── plan.md
│   ├── continue.md
│   ├── modules/            # Pipeline: research → script → voice → video → publish
│   ├── api/
│   ├── dashboard/
│   ├── scheduler/
│   └── tests/
├── trade-auto/             # Priority 2 — Crypto trading bots
│   ├── continue.md
│   ├── src/
│   ├── backtests/
│   └── docs/
├── pod/                    # Priority 3 — Etsy print on demand
│   ├── continue.md
│   ├── designs/
│   ├── listings/
│   └── scripts/
├── shopee-affiliate/       # Priority 4 — Shopee affiliate (Thailand)
│   ├── continue.md
│   ├── src/
│   ├── content/
│   ├── research/
│   └── campaigns/
├── amazon-kdp/             # Priority 5 — Kindle Direct Publishing
│   ├── continue.md
│   ├── src/
│   ├── books/
│   ├── covers/
│   ├── research/
│   └── templates/
├── steam-game/             # Priority 6 — Indie game on Steam
│   ├── continue.md
│   ├── godot/
│   ├── docs/
│   ├── assets/
│   └── data/
├── android-app/            # Priority 7 — Play Store apps
│   ├── continue.md
│   ├── app/
│   └── docs/
└── polymarket/             # Priority 8 — Prediction market bot
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

# BiG's Side Projects Workspace

## Quick Start
```bash
# Work on highest priority project:
claude --agent orchestrator

# Work on a specific project:
claude --agent trade-auto
claude --agent pod
claude --agent shopee-affiliate
claude --agent amazon-kdp
claude --agent steam-game
claude --agent android-app
claude --agent polymarket
```

## Structure
```
side-projects/
├── .claude/agents/         # Agent configs (one per project + orchestrator)
├── scripts/                # Crontab runner, weekly summary, manual triggers
├── projects/
│   ├── STATUS.md           # Cross-project status board
│   ├── trade-auto/         # Priority 1 — Crypto trading bots
│   │   ├── continue.md
│   │   ├── src/
│   │   ├── backtests/
│   │   └── docs/
│   ├── pod/                # Priority 2 — Etsy print on demand
│   │   ├── continue.md
│   │   ├── designs/
│   │   ├── listings/
│   │   └── scripts/
│   ├── shopee-affiliate/   # Priority 3 — Shopee affiliate (Thailand)
│   │   ├── continue.md
│   │   ├── src/
│   │   ├── content/
│   │   ├── research/
│   │   └── campaigns/
│   ├── amazon-kdp/         # Priority 4 — Kindle Direct Publishing
│   │   ├── continue.md
│   │   ├── src/
│   │   ├── books/
│   │   ├── covers/
│   │   ├── research/
│   │   └── templates/
│   ├── steam-game/         # Priority 5 — Indie game on Steam
│   │   ├── continue.md
│   │   ├── godot/
│   │   ├── docs/
│   │   ├── assets/
│   │   └── data/
│   ├── android-app/        # Priority 6 — Play Store apps
│   │   ├── continue.md
│   │   ├── app/
│   │   └── docs/
│   └── polymarket/         # Priority 7 — Prediction market bot
│       ├── continue.md
│       ├── src/
│       ├── data/
│       └── analysis/
```

## Rules for All Agents
- ALWAYS read continue.md before starting work
- ALWAYS update continue.md before ending session
- Ship fast, iterate later — BiG has < 5 hours/week total
- Make decisions autonomously unless it involves money or strategy
- Write production code, not prototypes
- Use free tools/APIs until revenue justifies paid ones

## BiG's Context
- Based in Bangkok, Thailand (GMT+7)
- Full-time software developer (limited side project time)
- Experience: Go, Java, Python, Node.js, iOS, microservices, K8s
- Has: Mac Mini, VPS, Claude Pro subscription
- Goal: Build multiple passive/semi-passive income streams

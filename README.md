# BiG's Side Projects

A collection of AI-assisted side projects aimed at building passive/semi-passive income streams. Each project is worked on autonomously by Claude agents with minimal human oversight.

## Projects

| Priority | Project | Description | Status |
|----------|---------|-------------|--------|
| 1 | [tiktok](./tiktok/) | TikTok/Reels/Shorts affiliate automation — 10 videos/week, ~90 min human input | 🟡 In Progress |
| 2 | [trade-auto](./trade-auto/) | Crypto trading bots (grid, mean reversion, momentum) | 🟡 Research |
| 3 | [pod](./pod/) | Etsy print-on-demand — Gen Z niche designs | 🟡 Research |
| 4 | [shopee-affiliate](./shopee-affiliate/) | Shopee affiliate marketing (Thailand) | 🟡 Research |
| 5 | [amazon-kdp](./amazon-kdp/) | Kindle Direct Publishing — low-content books | 🟡 Research |
| 6 | [steam-game](./steam-game/) | Indie game on Steam (Godot) | 🟡 Concept |
| 7 | [android-app](./android-app/) | Play Store apps | 🟡 Concept |
| 8 | [polymarket](./polymarket/) | Prediction market trading bot | 🟡 Research |

## How It Works

Each project has a `continue.md` that serves as the persistent session state for Claude. Before any session, Claude reads it; before ending, Claude updates it. This allows autonomous work across multiple short sessions.

```
project/
├── continue.md    # Session state — what was done, what's next, blockers
├── CLAUDE.md      # Project-specific instructions (if present)
└── plan.md        # Implementation plan (if present)
```

## Stack

- **Automation**: Python, FastAPI, Celery, Redis
- **Trading**: Python, vectorbt / backtrader, Binance API
- **Video**: FFmpeg, ElevenLabs, Runway/Kling
- **Game**: Godot 4
- **Mobile**: Android (Kotlin)
- **Infra**: Mac Mini + VPS

## Constraints

- < 5 hours/week human time across all projects
- Free tools preferred until revenue justifies paid
- Bangkok, Thailand (GMT+7)

## Status Board

See [STATUS.md](./STATUS.md) for the live cross-project status board and revenue tracker.

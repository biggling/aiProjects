# MCP Apps / MCP Server Products — Continue

## Last Session
2026-04-05 — Batch 2 research complete: 10 new MCP opportunities researched (sports/betting, media monitoring, visa/travel, energy/carbon, grants, health/wearables, multi-cloud FinOps, academic literature, CVE security, patent IP). Top picks: Visa Requirements MCP (+6 score), CVE Security MCP (+5), Grant Discovery MCP (+5). See research/findings/2026-04-05_new-niches-batch2.md. Master ranking updated to 30 total opportunities in master-opportunity-ranking-2026-04-05.md.

## What This Is
Build and sell niche MCP servers listed on Claude/ChatGPT app marketplaces. App directories are largely empty in 2026 — early movers with quality, focused tools can command $10-50/month subscriptions.

## Priority: HIGH (Tier 1)
Biggest opportunity: BiG already understands MCP deeply from Claude Code work. Weekend-scale projects with real recurring revenue potential.

## Target Niches (ranked by fit)
1. **Crypto portfolio tracker MCP** — pulls live prices, P&L, portfolio summary into Claude context
2. **Shopee API MCP** — product search, affiliate link generation, price tracking for Thai market
3. **Thai banking / PromptPay MCP** — QR generation, transaction summaries
4. **Claude Code agent config packs** — meta: sell the configs BiG already built

## Marketplaces to Target
- Anthropic MCP directory (claude.ai)
- ChatGPT plugin/GPT store
- Gumroad (for paid config packs)

## Tech Stack
- TypeScript (MCP SDK standard)
- Node.js runtime
- Free-tier hosting: Railway / Render / Cloudflare Workers

## Phase Plan
- [x] Phase 1: Research top MCP directories, pick first niche, scaffold server
- [ ] Phase 2: Build MVP MCP server (crypto portfolio tracker — no auth needed for free tier)
- [ ] Phase 3: List on Anthropic directory + set up Lemon Squeezy billing
- [ ] Phase 4: Iterate on feedback, build second niche server

## Current Phase
**Phase 2** — Ready to build

## Next Step
Scaffold TypeScript MCP server using `@modelcontextprotocol/server` v1.x + Streamable HTTP (via `@modelcontextprotocol/hono` or express). Integrate CoinGecko free API for multi-coin support. Target: portfolio summary, add holdings, live prices, P&L — all in one server. Keep responses under 25k tokens.

## Notes
- MCP servers can be local (stdio) or remote (Streamable HTTP) — remote = subscription model
- SSE transport is DEPRECATED — use Streamable HTTP only
- Anthropic directory submission form: https://docs.google.com/forms/d/e/1FAIpQLSeafJF2NDI7oYx1r8o0ycivCSVLNq92Mpc1FPxMKSw1CzDkqA/viewform
- Submission requires: HTTPS, Streamable HTTP, OAuth 2.0, safety annotations per tool, privacy policy, 3+ examples, GA status
- Billing: use Lemon Squeezy (Stripe Managed Payments) — handles Thai VAT compliance
- Also register on MCPize (85% revenue share) and glama.ai (free listing, 19,899 servers)
- Price target: $9-15/month confirmed viable by Ref MCP case study (hundreds of subscribers)
- Crypto niche: zero polished paid offerings — wide open
- Keep tool responses under 25,000 tokens (Anthropic hard limit)
- CoinGecko free API: 15,000+ coins — better than Binance-only approach
- Differentiators over kukapay/crypto-portfolio-mcp: multi-exchange via CCXT, cloud sync, P&L/tax reporting
- **Primary buyer persona confirmed:** Crypto-native quant developer, age 25–34, pays $49+/mo for Nansen/Glassnode; WTP $19–29/month for portfolio MCP
- **TAM:** 6,400–32,000 paying subscribers realistically addressable from Claude user base
- **Top frustration:** No CEX + DeFi combined P&L with cost basis — biggest confirmed gap
- **Discovery priority order:** GitHub → Smithery → MCP Hive (May 11) → Reddit r/algotrading → X/Twitter
- **Freemium benchmark:** 8% free-to-paid conversion; 500 installs → 40 paid → $760 MRR at $19/month

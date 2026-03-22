# MCP Apps / MCP Server Products — Continue

## Last Session
2026-03-22 — Phase 1 research complete. See mcp-apps/research/findings/2026-03-22.md for full findings.

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

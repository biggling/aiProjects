# MCP Apps / MCP Server Products — Continue

## Last Session
2026-03-22 — Project initialized.

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
- [ ] Phase 1: Research top MCP directories, pick first niche, scaffold server
- [ ] Phase 2: Build MVP MCP server (crypto portfolio tracker — no auth needed)
- [ ] Phase 3: List on Anthropic directory + set up Stripe/Gumroad
- [ ] Phase 4: Iterate on feedback, build second niche server

## Current Phase
**Phase 1** — Not started

## Next Step
Read the Anthropic MCP SDK docs, scaffold a minimal TypeScript MCP server, pick crypto portfolio tracker as first product.

## Notes
- MCP servers can be local (stdio) or remote (HTTP SSE) — remote = subscription model
- Anthropic's directory: https://www.anthropic.com/news/model-context-protocol (check for submission process)
- Keep servers small and focused — one tool that does one thing great

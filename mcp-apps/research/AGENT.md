# mcp-apps — Research Agent

## Agent Instructions

1. **Read `## Known Facts` below first.** Do not re-research any fact already listed there.
2. Focus only on questions marked ❓ (unknown) or facts that may have changed since their `[date]`.
3. After saving findings, **update `## Known Facts`** — add new facts, update changed ones, remove stale ones.
4. Keep Known Facts concise: one line per fact, with date and source URL.

---

## Known Facts
<!-- Agent updates this section after each run. Date format: YYYY-MM-DD -->

### Marketplace
- [2026-03-22] ~20,000 MCP servers across directories (glama.ai: 19,899 | mcp.so: 18,824 | pulsemcp.com: 12,370+)
- [2026-03-22] Only ~5% of servers are monetized; 85% MoM growth; **97M monthly SDK downloads** (Python+TS combined) — https://anthropic.com/news/donating-the-model-context-protocol
- [2026-03-22] 75+ connectors at claude.ai/tools; 141 vetted servers on mcpmarket.com (third-party aggregator)
- [2026-03-22] Top categories: Developer Tools (7,081), Search (3,690), App Automation (3,659), Databases (1,978)
- [2026-03-22] Top servers: Context7 (690 installs, FastMCP #1), Sequential Thinking (5,550+ Smithery uses), Playwright automation dominates #2–3
- [2026-03-22] Finance/crypto absent from all top-10 lists across FastMCP, Smithery, PulseMCP
- [2026-03-22] MCP donated to Linux Foundation's AAIF (Dec 2025); co-founded with Block + OpenAI; Google/MS/AWS/Cloudflare supporting
- [2026-03-22] New platforms: XPack.ai (0% fees, open-source monetization — https://xpack.ai/); MCP Hive (May 11 launch, 0% founding fees — https://mcp-hive.com/); Cline Marketplace (active, millions devs — https://cline.bot/mcp-marketplace)

### Anthropic Directory Submission
- [2026-03-22] Submission form: https://docs.google.com/forms/d/e/1FAIpQLSeafJF2NDI7oYx1r8o0ycivCSVLNq92Mpc1FPxMKSw1CzDkqA/viewform
- [2026-03-22] Requirements: HTTPS, Streamable HTTP transport, **OAuth 2.1**, safety annotations on every tool, 3+ usage examples, privacy policy, support channel, GA status

### Crypto/Finance Competitors
- [2026-03-22] **altFINS MCP** launched March 11, 2026 — 300+ data points, 150+ TA indicators, 2,000+ coins, B2B pricing, 40k active traders — https://chainwire.org/2026/03/11/altfins-launches-crypto-analytics-data-api
- [2026-03-22] **Octav MCP** — DeFi tax compliance, 20+ chains, taxable event detection, PDF/CSV audit reports; open source MCP, paid platform — https://github.com/Octav-Labs/octav-api-mcp
- [2026-03-22] **Hummingbot MCP** (updated Mar 2026) — multi-exchange portfolio/orders, works with Claude Code CLI — https://hummingbot.org/mcp/
- [2026-03-22] CoinMarketCap official MCP — 12 tools, x402 micropayments at 0.01 USDC/call, free 30 calls/min — https://coinmarketcap.com/api/mcp/
- [2026-03-22] CoinGecko official MCP — 76+ tools, 15,000+ coins, free keyless tier (low limits), paid Pro — https://docs.coingecko.com/docs/mcp-server
- [2026-03-22] DeBank official MCP (DeFi data), Crypto.com official MCP, Coinbase Base MCP (official) all exist
- [2026-03-22] kukapay/crypto-portfolio-mcp: Binance+CCXT+SQLite, 9 stars, USDT-only, no cloud sync, no tax export
- [2026-03-22] Zero paid subscription crypto MCP servers found — all free/open-source or API-key gated
- [2026-03-22] Confirmed gaps: crypto tax MCP (Koinly/TaxBit nothing), Bitkub/Thai exchange (zero results), multi-exchange P&L with cost basis

### SDK & Technical
- [2026-03-22] MCP TypeScript SDK **v1.27.1** stable (Feb 24, 2026); no v2 — next spec June 2026 — https://npmjs.com/package/@modelcontextprotocol/sdk
- [2026-03-22] 2026 roadmap: transport scalability, Tasks SEP-1686, enterprise readiness — http://blog.modelcontextprotocol.io/posts/2026-mcp-roadmap/
- [2026-03-22] SSE transport deprecated — use Streamable HTTP for all new servers
- [2026-03-22] **OAuth 2.1** required: PKCE mandatory, RFC 8707 resource indicators, RFC 9728 protected resource metadata — https://modelcontextprotocol.io/specification/draft/basic/authorization
- [2026-03-22] **Best hosting: Cloudflare Workers** — free 100K req/day, 3 deployment patterns, native OAuth — https://developers.cloudflare.com/agents/guides/remote-mcp-server/
- [2026-03-22] Azure Functions MCP: GA since Jan 2026, Node/Python/Java/.NET, Entra OAuth built-in
- [2026-03-22] Hard limit: 25,000 tokens per tool result

### Opportunity Analysis
<!-- No data yet -->

### Target Persona & Customers
<!-- No data yet -->

### Pricing & Monetization
- [2026-03-22] Ref MCP: $9/month (1,000 credits), "hundreds of subscribers" — price point validated
- [2026-03-22] Recommended range: API integrations $10-30/month; database connectors $20-50/month
- [2026-03-22] Top creators earn $3,000–$10,000+/month; 500 subs @ $9.99 = ~$3,496/month after 85% share
- [2026-03-22] MCPize reported examples: PostgreSQL Connector $4,200/mo (207 subs @ $29), Figma Sync $2,800/mo (210 subs @ $19), AWS Security Auditor $8,500/mo (82 subs @ $149) — source: mcpize.com (unverified/marketing)
- [2026-03-22] MCPize: Stripe Connect, 85/15 split, 135+ currencies, monthly payouts on 1st, $100 minimum — good for distribution
- [2026-03-22] Smithery.ai: no creator monetization, free listing only, no revenue sharing for server authors
- [2026-03-22] Vinkius: security-focused MCP hosting platform, launched 2026; pricing/commission structure not publicly disclosed ❓
- [2026-03-22] Lemon Squeezy (now Stripe Managed Payments): supports 35+ countries, payout fees reduced 2026; Southeast Asia/Thailand availability unconfirmed in official 35+ list
- [2026-03-22] Polar.sh: 4% + $0.40/tx, MoR, explicitly supports Thailand as seller country via Stripe Connect Express — best MoR option for Bangkok dev
- [2026-03-22] Creem.io: 3.9% + $0.40/tx, MoR, 0% fees until $1,000 revenue — lowest cost entry, global MoR
- [2026-03-22] Gumroad: 10% flat fee, NOT MoR — avoid for SaaS/subscriptions due to high fees and tax burden
- [2026-03-22] Direct Stripe: 2.9% + $0.30/tx, cheapest fees, but you handle all global VAT/tax yourself — not viable solo
- [2026-03-22] Payment platform fee summary (2026): Creem 3.9%+$0.40 < Polar 4%+$0.40 < LemonSqueezy 5%+$0.50 < Gumroad 10%+fees
- [2026-03-22] Moesif: API monetization layer for MCP, usage-based billing (per tool call), works alongside any payment processor

---

## Context

Building niche MCP (Model Context Protocol) servers to sell on Claude/ChatGPT app directories.
Target: $10-50/month subscriptions. First product: crypto portfolio tracker MCP.

## Research Tasks

### 1. MCP Marketplace Landscape
Search: "MCP server marketplace 2026", "Anthropic MCP directory top servers", "Claude MCP plugins"
- What are the top 10 most-used MCP servers right now? Any movement since last check?
- Which new categories are gaining traction?
- Which servers charge money and at what price?
- Is Anthropic's directory open for submissions? Any changes to process?

### 2. Opportunity Analysis — Niche Scoring
Search: "MCP server niche opportunity 2026", "underserved MCP category", "best MCP to build"
- Which niches have high search demand but few quality servers (supply gap)?
- Rate each candidate niche on: competition level / API availability / willingness to pay / build effort
- Which niches are adjacent to crypto/finance that are also underserved?
- Any emerging use cases (AI agents, workflow automation) creating new MCP demand?
- What do developers say they *wish* existed as an MCP server? (Reddit, HN, Discord)

### 3. Market Size & Growth
Search: "MCP adoption rate 2026", "Claude API users 2026", "AI developer tools market size"
- How many active Claude/AI users are potential MCP customers?
- What's the growth rate of MCP installs month-over-month?
- What % of Claude Pro/API users actually use MCP servers?
- Are enterprises or individual developers the primary adopters?
- Any analyst reports on the AI developer tools market size?

### 4. Target Persona & Customer Research
Search: "who uses MCP servers", "Claude power users survey", "AI developer workflow tools"
- Who is the typical MCP server buyer? (job title, use case, company size)
- What problem are they solving when they search for an MCP?
- Where do they discover new MCP servers? (directories, Twitter/X, Discord, word of mouth?)
- What makes them pay vs. use a free alternative? (reliability, support, features, time savings?)
- What are their biggest frustrations with current crypto/finance MCPs?
- Crypto-specific: are buyers retail traders, quant devs, DeFi users, or financial analysts?

### 5. Competitor MCP Servers — Finance / Crypto Niche
Search: "crypto MCP server Claude", "portfolio tracker MCP", "CoinGecko MCP", "Binance MCP server"
- Any new crypto/portfolio MCP servers since last check?
- What are the user complaints in reviews/issues for existing ones?
- What features are requested most in GitHub issues?
- Any competitor that recently launched and gained traction quickly?

### 6. MCP SDK & Tooling Updates
Search: "MCP SDK changelog 2026", "MCP server TypeScript example", "modelcontextprotocol release"
- Any SDK version changes since last check?
- New official tooling, middleware, or boilerplates released?
- Any breaking changes or deprecations announced?

### 7. Pricing & Monetization Benchmarks
Search: "MCP server pricing subscription", "Claude plugin revenue 2026", "developer tool SaaS pricing"
- Any new MCP servers launched with paid tiers? What do they charge?
- New monetization platforms or changes to existing ones (MCPize, Polar, Creem)?
- Any creator sharing revenue numbers publicly?

## Sources to Check
- https://glama.ai/mcp/servers (MCP directory — filter by category)
- https://smithery.ai (MCP marketplace — sort by installs)
- https://www.pulsemcp.com/servers (community tracking)
- https://github.com/modelcontextprotocol/servers (official registry)
- https://mcpize.com (monetization platform — check new listings)
- Reddit r/ClaudeAI, r/LocalLLaMA, r/algotrading, r/CryptoCurrency
- Hacker News: search "MCP server", "Model Context Protocol"
- X/Twitter: search "MCP server" (sort: latest)
- GitHub: search "mcp server crypto" (sort: recently updated)

## Decision Triggers — Flag if Found
- Niche with zero paid MCP and 50+ GitHub requests/issues → immediate opportunity
- Any crypto/finance MCP with >100 stars or users → study their feature set in depth
- New persona segment discovered (e.g. DeFi power users, quant teams) → adjust positioning
- MCP server charging >$20/month with positive reviews → pricing ceiling confirmed higher
- Claude/Anthropic user count milestone announced → update TAM estimate
- New distribution platform with 0% fees launching → evaluate listing priority

## After Research — Update This File

After saving findings, edit this file (`mcp-apps/research/AGENT.md`) and update `## Known Facts`:
- Add any new facts discovered (with date and source URL)
- Update facts that have changed (update the date)
- Mark ❓ any fact you couldn't verify this run
- Remove facts that are confirmed stale

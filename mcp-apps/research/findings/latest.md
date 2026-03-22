# mcp-apps Research — 2026-03-22

## MCP Marketplace Landscape

- **Top servers by installs (FastMCP):** Context7 (690 installs, 11k views), Sequential Thinking (569), Playwright Browser Automation (414), GitHub (204), Puppeteer (199) — https://fastmcp.me/blog/top-10-most-popular-mcp-servers
- **Top servers by uses (Smithery gateway):** Sequential Thinking (5,550+), wcgw (4,920+), GitHub (2,890+), Brave Search (680+), Web Research (533+) — https://github.com/pedrojaques99/popular-mcp-servers
- **Dominant categories:** Browser Automation (#2/#3 by demand), Memory/Docs (Context7 #1), AI Reasoning (Sequential Thinking), Developer/Git tools
- **Finance/crypto still absent** from all top-10 lists across both platforms
- **SDK downloads corrected:** 97M monthly downloads (Python + TypeScript combined) — NOT 8M; that figure is outdated — https://www.anthropic.com/news/donating-the-model-context-protocol-and-establishing-of-the-agentic-ai-foundation
- **Claude's directory:** 75+ connectors at claude.ai/tools (separate from mcpmarket.com's 141 vetted listing)

## New MCP Distribution Platforms (2026)

- **XPack.ai** — "world's first open-source MCP monetization platform," wrap any OpenAPI spec as paid MCP, 0% platform fee (Stripe pass-through only), open source — https://xpack.ai/ | https://github.com/xpack-ai/XPack-MCP-Marketplace
- **MCP Hive** — "premier MCP monetization marketplace," launching **May 11, 2026**; founding providers currently get 0% platform fees — https://mcp-hive.com/ | https://news.ycombinator.com/item?id=47110500
- **Cline MCP Marketplace** — active now, millions of developer users, "App Store for AI capabilities" — https://cline.bot/mcp-marketplace
- **Smithery.ai** — 7,300+ tools but **NO creator monetization** — discovery only, no revenue split, no earnings dashboard — https://smithery.ai/
- **Vinkius** — originally planned March 25 launch; site live but product details sparse, pricing unconfirmed — https://mcp-fusion.vinkius.com/

## Crypto / Finance MCP Competitors

### New Entrants Since Jan 2026
- **altFINS MCP** (launched March 11, 2026) — 300+ pre-computed data points, 150+ technical indicators, 120 trading signals, 2,000+ coins, 7 years history, 5 timeframes; 40,000+ active traders on the platform; B2B/enterprise pricing (not public) — https://altfins.com/knowledge-base/the-ultimate-guide-to-cryptocurrency-mcp-servers-in-2026-complete-comparison-for-traders-developers-trading-platforms/ | https://chainwire.org/2026/03/11/altfins-launches-crypto-analytics-data-api-and-mcp-for-algo-trading-ai-agents-and-trading-signals/
- **Hummingbot MCP** (updated March 2026) — multi-exchange portfolio balances, order history, market prices, funding rates, bot deployment; works with Claude Code CLI, Claude Desktop, Gemini CLI — https://hummingbot.org/mcp/

### Established Competitors
- **CoinMarketCap official MCP** — 12 tools, 10,000+ coins, TA indicators (MA, MACD, RSI, Fibonacci), on-chain metrics, holder distribution, trending narratives; **x402 micropayments: 0.01 USDC/tool call**; free tier 30 calls/min, 10k credits/month — https://coinmarketcap.com/api/mcp/
- **Octav MCP** (`Octav-Labs/octav-api-mcp`) — DeFi + tax compliance, 20+ chains, identifies taxable events (swaps, staking, lending), generates PDF/CSV audit-ready reports; open source MCP, paid platform (PRO tier) — https://github.com/Octav-Labs/octav-api-mcp | https://octav.fi/
- **DeBank official MCP** — DeFi data across multiple chains (protocols, tokens, pools, user assets) — https://www.pulsemcp.com/servers/demcp-debank
- **Coinbase Base MCP** (official) — onchain tools for Base network and Coinbase API — https://github.com/base/base-mcp
- **Crypto.com official MCP** — https://mcp.crypto.com/docs/what-is-mcp
- **Bit2Me MCP** — 52 tools, free with verified exchange account (EU-focused)

### Confirmed Market Gaps (Opportunities)
- **Crypto tax / Form 1099-DA MCP:** completely empty — Koinly, CoinTracking, TaxBit have zero MCP presence
- **Bitkub / Thai exchange MCP:** zero results found anywhere — completely unoccupied niche
- **Multi-exchange P&L with cost basis:** Octav covers DeFi only; no CEX + DeFi combined paid product
- **Paid subscription crypto MCP:** none found — all competitors are free/open source or API-key gated
- **Official Binance MCP:** community-only (nirholas/Binance-MCP), low quality, no commercial version
- **x402 micropayment model** emerging as alternative to subscriptions (0.01 USDC/call via Coinbase CDP)

## MCP SDK & Technical Updates

- **Current stable version: v1.27.1** (released February 24, 2026) — v1.x series still active, no v2 — https://www.npmjs.com/package/@modelcontextprotocol/sdk
- **Next spec version:** targeting June 2026 (not Q1 as previously thought); project uses SEP working group model, no hard deadlines — http://blog.modelcontextprotocol.io/posts/2026-mcp-roadmap/
- **Auth standard corrected: OAuth 2.1** (not 2.0) — requires PKCE, RFC 8707 resource indicators, RFC 9728 protected resource metadata — https://modelcontextprotocol.io/specification/draft/basic/authorization
- **Best hosting: Cloudflare Workers** — free 100K requests/day, 3 deployment patterns (`createMcpHandler`, `McpAgent`, raw transport), built-in OAuth for GitHub/Google/Slack/Auth0 — https://developers.cloudflare.com/agents/guides/remote-mcp-server/
- **Azure Functions MCP:** GA since January 2026, supports .NET/Java/JS/Python/TypeScript, Microsoft Entra OAuth built-in — https://www.infoq.com/news/2026/01/azure-functions-mcp-support/
- **Key recent SDK features:** conformance tests, OAuth server discovery, Tasks streaming (SEP-1686), auth pre-registration, security fix for command injection (v1.27.1)
- **SSE transport:** confirmed deprecated — Streamable HTTP is the standard
- **2026 roadmap priorities:** transport scalability (stateless sessions), Tasks spec (retry/expiration), enterprise readiness (audit trails, SSO, gateway behavior)

## Pricing & Monetization Benchmarks

### Revenue Data Points
- **Ref MCP:** $9/month, hundreds of subscribers (implied ~$1k–$3k MRR, not confirmed) — https://www.pulsemcp.com/posts/pricing-the-unknown-a-paid-mcp-server
- **MCPize case studies (unverified):** PostgreSQL Connector $4,200/mo (207 subs @ $29), Figma Sync $2,800/mo (210 subs @ $19), AWS Security Auditor $8,500/mo (82 subs @ $149) — https://mcpize.com/developers/monetize-mcp-servers
- **No independently verified Indie Hackers posts** with confirmed MCP server MRR found
- **Signal:** $149/month at low subscriber count ($8.5k/mo with 82 subs) — enterprise/professional pricing validated

### Payment Platform Update (Bangkok Dev)
| Platform | Fee | MoR | Thailand | Notes |
|---|---|---|---|---|
| Polar.sh | 4% + $0.40 | Yes | **Confirmed** | Developer-friendly, GitHub integration |
| Lemon Squeezy | 5% + $0.50 | Yes | Unconfirmed (35+ countries) | No longer clear winner |
| Creem.io | 3.9% + $0.40 | Yes | Unconfirmed | 0% fees until $1k MRR |
| Gumroad | 10% | No | Yes | Avoid for MCP servers |
| MCPize | 15% | N/A | Yes | Marketplace split — for distribution |

- **Polar.sh is now the recommended direct billing option** — Thailand confirmed, dev-focused, cheaper than Lemon Squeezy — https://polar.sh/docs/merchant-of-record/supported-countries
- **Smithery confirmed NOT a revenue channel** — use for discoverability only
- **MCP Hive founding provider window** — 0% platform fees if you list before May 11 launch — https://mcp-hive.com/

---

## Action Items for Work Agent

- [ ] **URGENT: Apply to MCP Hive as founding provider** — 0% fees if listed before May 11 launch (https://mcp-hive.com/)
- [ ] **Switch billing stack to Polar.sh** — confirmed Thailand support, replaces Lemon Squeezy as primary recommendation
- [ ] **Study Octav MCP feature set** — closest competitor in tax/DeFi space; understand what they don't cover for CEX users
- [ ] **Study altFINS MCP** — most sophisticated analytics competitor; their paid B2B model validates commercial viability in crypto space
- [ ] **Prototype crypto tax MCP** — biggest confirmed gap; no Koinly/CoinTracking/TaxBit MCP exists
- [ ] **Validate CoinMarketCap x402 model** — 0.01 USDC/call as alternative to subscriptions; evaluate for first product
- [ ] **Deploy first server on Cloudflare Workers** — free 100K req/day, native OAuth, fastest time-to-live
- [ ] **Check Vinkius on/after March 25** — confirm pricing and commission model after launch
- [ ] **Update OAuth implementation target to 2.1** — not 2.0; requires PKCE + RFC 8707 resource indicators
- [ ] **Evaluate enterprise pricing tier** — MCPize case study shows $149/month with 82 subs earns $8.5k/mo; consider professional tier for portfolio product

---

## Sentiment

Overall: **Bullish / Opportunity**
Reasoning: The monetization infrastructure (MCP Hive, Polar.sh, XPack.ai) is being built RIGHT NOW in Q1 2026, creating a first-mover window — crypto/finance is confirmed empty of paid products while altFINS proves commercial demand exists in the category.

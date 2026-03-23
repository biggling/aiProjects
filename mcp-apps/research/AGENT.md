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
- [2026-03-23] ~20,000 MCP servers across directories (glama.ai: 19,922 | mcp.so: 18,824 | pulsemcp.com: 12,370+); Smithery catalogs 7,300+ tools; +23 servers/day on Glama
- [2026-03-22] Only ~5% of servers are monetized; 85% MoM growth; **97M monthly SDK downloads** (Python+TS combined) — https://anthropic.com/news/donating-the-model-context-protocol
- [2026-03-22] 75+ connectors at claude.ai/tools; 141 vetted servers on mcpmarket.com (third-party aggregator)
- [2026-03-22] Top categories: Developer Tools (7,081), Search (3,690), App Automation (3,659), Databases (1,978)
- [2026-03-23] PulseMCP top-10 by weekly visitors: Datadog 33.8M (#1), Playwright 1.4M (#2), Context7 496K (#3), Chrome DevTools 433K (#4), MongoDB 422K (#5), Git 341K (#6), Filesystem 281K (#7), Mapbox Docs 279K (#8), Context Mode 277K (#9), Claude Flow 234K (#10) — https://www.pulsemcp.com/servers
- [2026-03-22] Top servers by installs: Context7 (690 installs, FastMCP #1), Sequential Thinking (5,550+ Smithery uses), Playwright automation dominates #2–3
- [2026-03-23] Finance/crypto absent from top-10; CoinPaprika #15 at 141K/wk; Nansen #20 at 109K/wk; 245 crypto servers on PulseMCP (~2% of total)
- [2026-03-23] Fastest-growing new categories (March 2026): Observability/DevOps (Datadog #1 overall), Security/code-quality, Browser Automation (3 of top-10), Cloud Platform Management
- [2026-03-22] MCP donated to Linux Foundation's AAIF (Dec 2025); co-founded with Block + OpenAI; Google/MS/AWS/Cloudflare supporting
- [2026-03-23] **Google unified MCP** (Mar 17, 2026 GA) — fully managed remote MCP across all GCP services (Maps, BigQuery, GKE, Compute); IAM + audit + Model Armor; auto-enabled with service — https://cloud.google.com/blog/products/ai-machine-learning/announcing-official-mcp-support-for-google-services
- [2026-03-23] **SonarQube Cloud native MCP embed** (Mar 17, 2026) — no Docker required; free tier 50K LOC/5 users — https://www.sonarsource.com/blog/announcing-native-mcp-server-in-sonarqube-cloud/
- [2026-03-23] **Azure MCP in Visual Studio 2026 GA** — built-in out-of-the-box with Azure/AI workload — https://devblogs.microsoft.com/visualstudio/azure-mcp-server-now-built-in-with-visual-studio-2026-a-new-era-for-agentic-workflows/
- [2026-03-23] New platforms: XPack.ai v1.0 live (0% fees — https://xpack.ai/); MCP Hive (May 11 launch, 0% founding fees, "Project Ignite" phase — https://mcp-hive.com/); Cline Marketplace (active — https://cline.bot/mcp-marketplace); **Vinkius MCP Fusion now live** (zero commission — https://mcp-fusion.vinkius.com/)
- [2026-03-22] Enterprise "shadow IT" MCP risk flagged by Qualys — signals rapid enterprise adoption — https://blog.qualys.com/product-tech/2026/03/19/mcp-servers-shadow-it-ai-qualys-totalai-2026
- [2026-03-23] **SmartLoader trojanized MCP attack** (Feb 2026) targets crypto wallet holders + devs via bogus GitHub MCP servers — security/trust is now a paid MCP differentiator — https://thehackernews.com/2026/02/smartloader-attack-uses-trojanized-oura.html

### Market Size & TAM
- [2026-03-23] **Anthropic $19B annualized revenue** (March 2026); projects $26B full-year; Claude Code alone $2.5B ARR (Feb 2026, doubling since Jan) — https://sacra.com/c/anthropic/
- [2026-03-22] Claude: 18.9M MAU, 11M DAU, 300K+ enterprise customers, 70% Fortune 100 — https://www.demandsage.com/claude-ai-statistics/
- [2026-03-22] 34% of Claude tasks = "computer and mathematical" (Anthropic Economic Index Jan 2026) → ~6.4M technical users
- [2026-03-22] Crypto MCP TAM: 5–10% of technical users = 320K–640K; 8% conversion = 6,400–32,000 subs; $122K–$608K ARR at 1% capture @ $19/mo
- [2026-03-22] MCP Server market: $2.7B (2025) → $5.6B by 2034 — MCP Manager
- [2026-03-22] AI Code Tools market: $34.6B in 2026 → $91.3B by 2032 at 17.5% CAGR — Research and Markets
- [2026-03-22] CrewAI, OpenAgents, Microsoft Agent Framework (GA Q1 2026) all support MCP natively — user pool extends beyond Claude
- [2026-03-23] **Claude Code Channels** (new feature): connect Claude Code to Discord/Telegram — enables ambient portfolio agent with messaging wrapper as distribution channel — https://venturebeat.com/orchestration/anthropic-just-shipped-an-openclaw-killer-called-claude-code-channels
- [2026-03-23] **DeFAI** (DeFi+AI agents) is emerging category: 550+ AI agent crypto projects on CoinGecko, $4.34B combined market cap; all DeFi-only, no CEX P&L — https://coincub.com/blog/crypto-ai-agents/
- [2026-03-23] MCP 2026 roadmap: 4 directions — transport evolution, A2A communication, governance maturation, enterprise readiness — https://dev.to/pockit_tools/mcp-vs-a2a-the-complete-guide-to-ai-agent-protocols-in-2026-30li

### Anthropic Directory Submission
- [2026-03-22] Submission form: https://docs.google.com/forms/d/e/1FAIpQLSeafJF2NDI7oYx1r8o0ycivCSVLNq92Mpc1FPxMKSw1CzDkqA/viewform
- [2026-03-22] Requirements: HTTPS, Streamable HTTP transport, **OAuth 2.1**, safety annotations on every tool, 3+ usage examples, privacy policy, support channel, GA status

### Crypto/Finance Competitors
- [2026-03-22] **DECISION TRIGGER: OKX Agent Trade Kit** (Mar 3, 2026) — 124 stars, 106 tools, 8 modules (spot/perp/futures/options/account/earning/grid), read-only safety flag, MIT, free — https://github.com/okx/agent-trade-kit
- [2026-03-23] **Alpaca MCP** — 570 stars (updated Mar 18); stocks+ETFs+crypto+options, paper trading, GTC/IOC — https://github.com/alpacahq/alpaca-mcp-server
- [2026-03-22] **altFINS MCP** launched March 11, 2026 — 300+ data points, 150+ TA indicators, 2,000+ coins, B2B pricing, 40k active traders — https://chainwire.org/2026/03/11/altfins-launches-crypto-analytics-data-api
- [2026-03-22] **Octav MCP** — DeFi tax compliance, 20+ chains, taxable event detection, PDF/CSV audit reports; open source MCP, paid platform — https://github.com/Octav-Labs/octav-api-mcp
- [2026-03-22] **Hummingbot MCP** (updated Mar 2026) — multi-exchange portfolio/orders + bot deployment, new "Skills" system — https://hummingbot.org/mcp/
- [2026-03-22] CoinMarketCap official MCP — 12 tools, x402 micropayments at 0.01 USDC/call, free 30 calls/min — https://coinmarketcap.com/api/mcp/
- [2026-03-22] CoinGecko official MCP — 76+ tools, 15,000+ coins, free keyless tier (low limits), paid Pro — https://docs.coingecko.com/docs/mcp-server
- [2026-03-22] DeBank official MCP (DeFi data), Crypto.com official MCP, Coinbase Base MCP (official), Bit2Me MCP (52 tools, EU-focused) all exist
- [2026-03-22] kukapay/crypto-portfolio-mcp: 9 stars, stagnant. kukapay/crypto-indicators-mcp: 113 stars, #1,025 PulseMCP — more active — https://www.pulsemcp.com/servers/kukapay-crypto-indicators
- [2026-03-22] badkk/awesome-crypto-mcp-servers: 130 stars, 41 forks, 12 curated servers — https://github.com/badkk/awesome-crypto-mcp-servers
- [2026-03-22] **Zenwork Tax1099 MCP** launched — first tax-adjacent MCP; US 1099 filing focus — https://www.morningstar.com/news/accesswire/1116658msn/zenwork-tax1099-launches-mcp-server-for-ai-first-businesses-accounting-firms
- [2026-03-22] **Pane MCP** (March 2026) — personal finance MCP inside Claude (spending/net worth/investments); HN: "needed this so bad already" — https://news.ycombinator.com/item?id=47240363
- [2026-03-22] **Rot MCP** (Feb 2026) — Reddit sentiment trading signals, OSS, 9,000 clones in 5 days — https://news.ycombinator.com/item?id=47056745
- [2026-03-23] **nirholas/Binance-MCP** — 15 stars, 478+ tools, full Binance API; zero portfolio P&L or cost basis — https://github.com/nirholas/Binance-MCP
- [2026-03-23] **edkdev/defi-trading-mcp** — 42 stars, active (14 commits); 17+ blockchains, 0x swaps, MEV protection, TX history; DeFi-only, no CEX portfolio — https://github.com/edkdev/defi-trading-mcp
- [2026-03-23] **Nayshins/mcp-server-ccxt** — 62 stars, 22 forks; 100+ exchanges via CCXT; market data/OHLCV only, no P&L/cost basis — https://github.com/Nayshins/mcp-server-ccxt
- [2026-03-23] **armorwallet/armor-crypto-mcp** — wallet creation, swaps, **DCA/stop loss/take profit** — first DCA automation MCP — https://github.com/armorwallet/armor-crypto-mcp
- [2026-03-23] **TronScan MCP** (Mar 9, 2026) — official TRON blockchain data MCP — https://support.tronscan.org/hc/en-us/articles/55764103590553
- [2026-03-23] **CryptoRank MCP** — 35,000+ assets, token unlocks, investor profiles — https://cryptorank.io/public-api/mcp
- [2026-03-23] **Gloria AI (Crypto Briefing)** — #1 on PulseMCP crypto search, **6,500 weekly visitors** — highest-traffic crypto MCP — https://www.pulsemcp.com/servers?q=crypto
- [2026-03-23] **ZARQ Crypto Risk Intelligence** — #2 on PulseMCP crypto search, 712 weekly visitors — https://www.pulsemcp.com/servers?q=crypto
- [2026-03-23] Zero paid subscription crypto MCP servers found — all free/open-source or API-key gated (confirmed again)
- [2026-03-23] **TaxBit discontinued consumer crypto tax** — enterprise-only now; retail users abandoned — crypto tax MCP gap widened — https://taxbit.com
- [2026-03-23] Confirmed gaps (still open): crypto tax MCP (retail), Bitkub/Thai exchange, CEX+DeFi combined P&L with cost basis, enterprise compliance (sanctions/audit trail), derivatives intelligence
- [2026-03-23] **Bitkub**: listed RLUSD (first Thai THB pairing), $200M HK IPO planned 2026; 13.5M+ app downloads, 240+ cryptos, 80%+ Thailand volume, ~$66M daily; zero MCP server; API at https://github.com/bitkub/bitkub-official-api-docs
- [2026-03-23] **altFINS MCP** (Mar 11, 2026): 150+ TA indicators, 130+ signals, 2,000 assets, B2B pricing; no portfolio P&L/cost basis/tax — https://chainwire.org/2026/03/11/altfins-launches-crypto-analytics-data-api-and-mcp-for-algo-trading-ai-agents-and-trading-signals/
- [2026-03-23] **Hive Intelligence Crypto MCP**: 351 tools, 14 categories, 60+ blockchains, CoinGecko+LunarCrush+DefiLlama+CCXT+10 more sources; most comprehensive market data MCP; no CEX P&L/cost basis/tax — https://hiveintelligence.xyz/
- [2026-03-23] **Gloria AI feature set confirmed**: news+sentiment only (5 free tools + 2 paid x402); no portfolio/P&L/cost basis/tax; 6,500 weekly PulseMCP visitors — https://github.com/cryptobriefing/gloria-mcp
- [2026-03-23] **ZARQ feature set confirmed**: 8 tools, 198-205 tokens, pre-trade risk scoring (DtD, trust score, crash probability); no CEX integration/P&L/cost basis — https://glama.ai/mcp/servers/zarq-ai/zarq-risk-intelligence
- [2026-03-23] **altFINS guide** explicitly lists unmet crypto MCP needs: portfolio P&L, cost basis, crypto tax, Southeast Asian exchange coverage, compliance/sanctions — first third-party source to articulate these gaps in writing
- [2026-03-23] **Enterprise compliance gap**: sanctions screening, regulatory status, audit trail — no MCP addresses this; 65% of financial institutions cite data security as primary AI barrier (Zuplo State of MCP Report) — https://zuplo.com/mcp-report

### SDK & Technical
- [2026-03-23] MCP TypeScript SDK **v1.27.1** stable (Feb 24, 2026) — no new release; **v1.28/v1.29 do not exist**; v2 still pre-alpha — https://github.com/modelcontextprotocol/typescript-sdk/releases
- [2026-03-23] **C# SDK v1.0 GA** (Mar 5, 2026) — full 2025-11-25 spec, .NET now first-class MCP platform, Entra OAuth built-in — https://devblogs.microsoft.com/dotnet/release-v10-of-the-official-mcp-csharp-sdk/
- [2026-03-22] Latest stable spec: **2025-11-25** — breaking change: JSON-RPC batching removed; new: Tasks primitive, Tool icons, OAuth Client ID Metadata — https://modelcontextprotocol.io/specification/2025-11-25/changelog
- [2026-03-23] Next spec release: **June 2026** (tentative) — SEPs being finalized Q1 2026; no new RFC/draft published in March 2026 — http://blog.modelcontextprotocol.io/posts/2026-mcp-roadmap/
- [2026-03-22] 2026 roadmap: transport scalability (stateless sessions), Tasks spec finalization (SEP-1686), enterprise readiness (audit trails, SSO, gateway) — no new transports — http://blog.modelcontextprotocol.io/posts/2026-mcp-roadmap/
- [2026-03-22] SSE transport deprecated — use Streamable HTTP for all new servers
- [2026-03-22] **OAuth 2.1** required: PKCE mandatory, RFC 8707 resource indicators, RFC 9728 protected resource metadata — https://modelcontextprotocol.io/specification/draft/basic/authorization
- [2026-03-22] v1.27.1 includes security fix for command injection — important for hosted/public servers
- [2026-03-22] **GitHub MCP Registry** now official discovery layer — https://github.blog/ai-and-ml/github-copilot/meet-the-github-mcp-registry-the-fastest-way-to-discover-mcp-servers/
- [2026-03-22] **Best hosting: Cloudflare Workers** — free 100K req/day, 3 deployment patterns, native OAuth — https://developers.cloudflare.com/agents/guides/remote-mcp-server/
- [2026-03-22] Azure Functions MCP: GA since Jan 2026, Node/Python/Java/.NET, Entra OAuth built-in
- [2026-03-22] Hard limit: 25,000 tokens per tool result

### Opportunity Analysis
- [2026-03-23] Top niche by score: **Crypto Tax / 1099-DA MCP (score +7)** — TaxBit abandoned retail; IRS 1099-DA enforcement LIVE (Feb 17, 2026 forms sent); PulseMCP 0/0 results for "crypto tax"; DeFi+1099-DA = highest confusion/audit risk segment — https://www.taxnotes.com/featured-analysis/what-irss-new-form-1099-da-means-defi-users/2026/03/11/7v0md
- [2026-03-22] Tied top: Dev Analytics / GA4 natural-language MCP for indie founders (score +5) — only GoodData at $1,200/mo enterprise exists
- [2026-03-22] #3: Multi-exchange P&L + cost basis (score +4) — CCXT APIs mature; CCXT MCP (62 stars) covers market data only, NOT P&L/cost basis — gap confirmed
- [2026-03-22] #4 tied: Sentiment trading signals MCP (score +3) — Rot MCP got 9,000 GitHub clones in 5 days Feb 2026; open source only
- [2026-03-23] #4 tied: Bitkub / Thai exchange MCP (score +3) — zero MCP servers; IPO news raises profile; API docs available
- [2026-03-22] Finance/healthcare/legal/education confirmed as "future trends" in MCP — still early mover window — https://fastmcp.me/blog/most-popular-mcp-tools-2026
- [2026-03-22] Rot MCP creator quote: "Wall Street pays millions for retail sentiment data. It's free on Reddit." — HN Feb 2026
- [2026-03-22] "needed this so bad already" — HN commenter on Pane financial data MCP, March 2026
- [2026-03-22] Alpaca MCP quality complaints: "context size is huge" (#45), "configuration is truly negligent" (#47) — quality gap = opportunity
- [2026-03-22] CrewAI now supports MCP server URLs in config — user pool extends beyond Claude-only clients
- [2026-03-22] Microsoft merged AutoGen + Semantic Kernel → "Microsoft Agent Framework" GA Q1 2026 — MCP via extension modules
- [2026-03-22] x402 micropayment model (0.01 USDC/call) validated by CoinMarketCap MCP — viable alternative to subscriptions

### Target Persona & Customers
- [2026-03-22] Primary buyer (crypto MCP): Crypto-native quant developer — 25–34, 77% male, pays $49–175/mo for Nansen/Glassnode, discovers via GitHub + Smithery
- [2026-03-22] Secondary buyer: Active retail trader — holds 5–20 assets on 2–3 exchanges, already pays CoinTracking/CoinStats $8–179/mo
- [2026-03-22] Tertiary buyer: Enterprise fintech developer — pays $149–300/mo for specialized B2B tools, discovers via GitHub + HN
- [2026-03-22] Discovery channels ranked: GitHub #1, Smithery #2, Claude.ai/tools #3, PulseMCP #4, Reddit #5, X #6, MCP Hive (May launch) #7
- [2026-03-22] Free-to-paid conversion benchmark: 8% (MCPize data) — 500 free installs → 40 paid → $760 MRR at $19/mo
- [2026-03-22] Top pain point: CEX + DeFi combined P&L with cost basis — not solved by any current tool

### Pricing & Monetization
- [2026-03-22] Ref MCP: $9/month (1,000 credits), "hundreds of subscribers" — price point validated
- [2026-03-23] Standard paid MCP tiers confirmed (2026 market benchmarks): $49 Starter / $299 Pro / $999 Enterprise
- [2026-03-22] Recommended range: API integrations $10-30/month; database connectors $20-50/month
- [2026-03-23] **$1K MRR achievable confirmed** — MCPize "growing creator" tier = $1K–3K/mo (6–12 months); Apify: multiple creators >$1K MRR, top creators >$10K MRR — https://apify.com/mcp/developers
- [2026-03-22] MCPize reported examples: PostgreSQL Connector $4,200/mo (207 subs @ $29), Figma Sync $2,800/mo (210 subs @ $19), AWS Security Auditor $8,500/mo (82 subs @ $149) — source: mcpize.com (unverified/marketing)
- [2026-03-23] MCPize enterprise WTP confirmed: Atlan $1,200+/mo (small teams), MindsDB $750+/mo — enterprise ceiling higher than previously modeled
- [2026-03-22] MCPize: Stripe Connect, 85/15 split, 135+ currencies, monthly payouts on 1st, $100 minimum — good for distribution
- [2026-03-23] Smithery.ai: **charges creators $30/month** — no revenue share (avoid for monetization; free listing was previously assumed but incorrect)
- [2026-03-23] Vinkius MCP Fusion: **live and operational** (zero commission); framework supports Cursor, Claude Desktop, Claude Code, Windsurf, Cline — https://mcp-fusion.vinkius.com/
- [2026-03-22] Lemon Squeezy (now Stripe Managed Payments): supports 35+ countries; Thailand unconfirmed — no longer recommended default
- [2026-03-22] Polar.sh: 4% + $0.40/tx, MoR, **Thailand confirmed** via Stripe Connect Express — https://polar.sh/docs/merchant-of-record/supported-countries
- [2026-03-22] Creem.io: 3.9% + $0.40/tx, MoR, 0% fees until $1,000 revenue, **Thailand confirmed** via local bank transfer — https://docs.creem.io/merchant-of-record/supported-countries
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

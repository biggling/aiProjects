# MCP Apps — Implementation Plan

> Build and sell niche MCP servers on Claude/ChatGPT marketplaces.
> First product: **Crypto Portfolio Tracker MCP** — pulls live prices, P&L, portfolio summary into Claude context.
> Revenue target: $760+ MRR from 40 paid subscribers at $19/month.

---

## Phase 0: Deep Market Research & Target Customer (DO FIRST)

**Goal:** Validate product-market fit with laser-focused customer research before writing code.

### Market Sizing & Validation
- [ ] Count active MCP server users on Smithery, LobeHub, PulseMCP — extract install numbers for finance/crypto category
- [ ] Scrape Smithery/PulseMCP for all crypto-related MCP servers — catalog features, pricing, install counts, user reviews
- [ ] Analyze CoinStats MCP (closest competitor): feature gaps, user complaints, pricing, install count
- [ ] Research BitGo MCP user feedback — what do institutional users want that BitGo doesn't offer?
- [ ] Survey r/algotrading + r/CryptoCurrency posts about tax reporting pain points — extract exact quotes
- [ ] Research CoinTracker, Koinly, TokenTax pricing + user complaints (G2, Trustpilot, Reddit) — find gaps MCP can fill
- [ ] Quantify 1099-DA filing market: how many US crypto holders file taxes? (IRS data, Chainalysis reports)
- [ ] Research Thailand crypto tax landscape: how many Bitkub users, what tools they use for tax reporting

### Laser-Targeted Customer Persona
- [ ] **Primary persona: "DeFi Dan"** — Validate or refine:
  - Age, income, location (US vs global split)
  - Current tool stack (Nansen? Glassnode? Zerion? DeBank?)
  - Monthly spending on crypto tools ($49-200/mo range — verify)
  - Top 3 daily frustrations with current portfolio tracking
  - Where they hang out online (Discord servers, Telegram groups, subreddits, X accounts)
  - What would make them switch to an MCP-based tool?
- [ ] **Secondary persona: "Tax Season Tom"** — seasonal user:
  - When do they start looking for tax tools? (Jan? March? April?)
  - What's the trigger to buy? (1099-DA received? CPA asks for data?)
  - Price sensitivity for a tax-only tool vs all-year portfolio tracker
  - Do they want self-serve or would they give it to their CPA?
- [ ] Interview 5-10 people from r/algotrading or crypto Discord who match the persona
- [ ] Ask: "If I built an MCP server that does X, would you pay $19/month?" — record exact responses

### Competitor Deep-Dive
- [ ] Create comparison matrix: CoinStats MCP vs kukapay vs Gloria AI vs BitGo MCP
  - Features, pricing, install count, user ratings, last update date
- [ ] Test CoinStats MCP hands-on — document UX friction points, missing features, response quality
- [ ] Research MetaMask Tax Hub (Summ) in detail — what can't it do that an MCP can?
- [ ] Map the "cost basis calculation" competitive landscape (TurboTax, H&R Block, CoinTracker, Koinly)
- [ ] Identify what "winning" looks like: what # of installs/subscribers = success at 3mo, 6mo, 12mo?

### Customer Discovery Channels
- [ ] Join and monitor 5 crypto tax Discord servers — lurk for pain points
- [ ] Follow top 10 crypto tax Twitter/X accounts — note what their audience complains about
- [ ] Monitor r/CryptoTax, r/algotrading, r/CryptoCurrency weekly for tax-related posts
- [ ] Find 3-5 CPAs/tax professionals who specialize in crypto — understand their workflow and tool needs
- [ ] Research Telegram groups where Thai crypto traders discuss tax (Bitkub community channels)

### Research Deliverables
- [ ] 1-page "Customer Brief" document: who they are, what they need, what they'll pay, where to find them
- [ ] Competitor comparison matrix (spreadsheet)
- [ ] List of 20+ exact customer quotes about crypto tax pain points
- [ ] Go/no-go decision on crypto tax MCP vs pivot to different niche

---

## Tech Stack

| Layer | Tool |
|---|---|
| Language | TypeScript |
| Runtime | Node.js 20+ |
| MCP SDK | `@modelcontextprotocol/server` v1.x |
| Transport | Streamable HTTP (SSE is deprecated) |
| API | CoinGecko free tier (15,000+ coins) |
| Multi-exchange | CCXT library |
| Auth | OAuth 2.0 (required for Anthropic directory) |
| Billing | Lemon Squeezy (handles Thai VAT) |
| Hosting | Railway / Cloudflare Workers |
| DB | SQLite (local) / Turso (cloud sync) |

---

## Phase 1: Project Scaffold & Local MCP Server

**Goal:** Working MCP server running locally via stdio with basic crypto price tools.

### Tasks
- [ ] Initialize TypeScript project with `@modelcontextprotocol/server`
- [ ] Set up project structure:
  ```
  mcp-apps/
  ├── src/
  │   ├── server.ts          # MCP server entry point
  │   ├── tools/              # Tool implementations
  │   │   ├── prices.ts       # Live price lookup
  │   │   ├── portfolio.ts    # Portfolio CRUD + P&L
  │   │   ├── holdings.ts     # Add/remove holdings
  │   │   └── tax.ts          # Cost basis / P&L reporting
  │   ├── services/
  │   │   ├── coingecko.ts    # CoinGecko API client
  │   │   ├── ccxt.ts         # Multi-exchange client
  │   │   └── storage.ts      # Portfolio persistence
  │   └── types.ts
  ├── package.json
  ├── tsconfig.json
  └── .env.example
  ```
- [ ] Implement CoinGecko API client (price, market data, coin list)
- [ ] Implement `get_price` tool — lookup current price for 1+ coins
- [ ] Implement `add_holding` tool — add coin, quantity, buy price, exchange
- [ ] Implement `get_portfolio` tool — return all holdings with live P&L
- [ ] Implement local JSON file storage for portfolio data
- [ ] Cap all tool descriptions to ≤2KB (Claude Code hard limit)
- [ ] Add safety annotations per tool (required for Anthropic directory)
- [ ] Test locally via Claude Code with stdio transport
- [ ] Write unit tests for each tool

### Deliverable
`npx tsx src/server.ts` runs. Claude Code can call all 4 tools and get real data.

---

## Phase 2: Advanced Features — Tax, Multi-Exchange, Cloud Sync

**Goal:** Differentiate from kukapay/crypto-portfolio-mcp with CEX+DeFi P&L and cost basis tracking.

### Tasks
- [ ] Implement CCXT integration for multi-exchange balance fetching (Binance, Bybit, OKX)
- [ ] Implement `get_cost_basis` tool — FIFO/LIFO/specific-ID lot tracking
- [ ] Implement `get_tax_report` tool — capital gains summary per tax year
- [ ] Add 2026 1099-DA context: lot identification relief (Notice 2026-20) explainer
- [ ] Implement `get_portfolio_summary` tool — aggregated P&L across all exchanges + manual holdings
- [ ] Add DeFi wallet tracking via public address (Etherscan/similar free APIs)
- [ ] Implement cloud sync via Turso (SQLite edge DB) for cross-device portfolio
- [ ] Add rate limiting and retry logic for all API calls
- [ ] Ensure all responses stay under 25,000 tokens
- [ ] Write integration tests

### Deliverable
Portfolio tracks holdings across multiple exchanges with accurate cost basis and P&L reporting.

---

## Phase 3: Remote Server + OAuth + Billing

**Goal:** Deploy as a remote MCP server with Streamable HTTP, OAuth 2.0 auth, and subscription billing.

### Tasks
- [ ] Convert from stdio to Streamable HTTP transport
- [ ] Implement OAuth 2.0 authentication flow
- [ ] Deploy to Railway (or Cloudflare Workers)
- [ ] Set up HTTPS with custom domain
- [ ] Integrate Lemon Squeezy for subscription billing ($19/month)
- [ ] Implement free tier (3 coins, manual-only) vs paid tier (unlimited, multi-exchange, tax)
- [ ] Add API key management per subscriber
- [ ] Create privacy policy page (required for Anthropic directory)
- [ ] Write 3+ usage examples (required for Anthropic directory)
- [ ] Test end-to-end: sign up → pay → authorize → use tools in Claude

### Deliverable
Paying subscribers can add the server to Claude Desktop/Code and use all tools.

---

## Phase 4: Marketplace Listings & Launch

**Goal:** List on all major MCP directories and execute launch sequence.

### Tasks
- [ ] Submit to Anthropic MCP directory (via Google Forms submission)
- [ ] List on Smithery (discovery priority #1 per research)
- [ ] List on MCPize (85% revenue share)
- [ ] List on LobeHub (43,400+ servers, large discovery surface)
- [ ] List on MCPmarket.com (daily "Top MCP Servers" lists)
- [ ] List on glama.ai (19,899+ servers)
- [ ] Create GitHub repo with README, screenshots, and demo GIF
- [ ] Add "Verified secure / auth-required" badge language to listings
- [ ] Launch sequence: GitHub → Smithery → Reddit r/algotrading → r/ClaudeCode → X/Twitter
- [ ] Post on Hacker News (Show HN)

### Deliverable
Server listed on 5+ directories. First 500 installs target → 40 paid at 8% conversion.

---

## Phase 5: Iterate & Second Product

**Goal:** Respond to user feedback, improve retention, build second MCP server.

### Tasks
- [ ] Monitor user feedback and usage patterns
- [ ] Add portfolio alerting tool (price targets, P&L thresholds)
- [ ] Evaluate Stripe MPP as alternative billing (session-based micropayments)
- [ ] Consider x402 for crypto-native audience (permissionless payments)
- [ ] Scope second MCP server: Bitkub MCP (Thailand exchange) or Shopee API MCP
- [ ] Build and launch second server using same infra
- [ ] Record YouTube content during build sessions (synergy with youtube-content project)

### Deliverable
First server at 40+ paid subscribers. Second server in development.

---

## Key Research Insights Driving This Plan

- **Zero competition**: PulseMCP shows 0 results for "crypto tax" MCP as of 2026-03-28
- **1099-DA demand peak**: Cost basis gap confirmed — all 2025 forms report gross proceeds ONLY
- **Primary buyer**: Crypto-native quant dev, 25-34, already paying $49+/mo for analytics tools
- **TAM**: 6,400-32,000 addressable paying subscribers from Claude user base
- **Biggest gap**: No CEX + DeFi combined P&L with cost basis — this is the wedge
- **Stripe MPP launched**: Enterprise-grade agent payments now viable (Anthropic/Visa backed)
- **Security differentiator**: 38% of MCP servers lack auth — being secure is a trust signal

---

## Notes for Claude

- Always use Streamable HTTP, never SSE (deprecated)
- Tool descriptions must be ≤2KB
- Tool responses must be ≤25,000 tokens
- Use `pathlib`-equivalent (`path` module) for all file paths
- All API calls need timeout (10s default) and retry (3x exponential backoff)
- CoinGecko free tier: 10-30 calls/min — cache aggressively (60s TTL for prices)
- Never hardcode API keys — use environment variables
- OAuth 2.0 is mandatory for Anthropic directory listing

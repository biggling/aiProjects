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
- [2026-03-28] **12,870+ registered MCP servers** (PulseMCP, ~100/day growth); Glama index over 20,000+ total entries — https://www.pulsemcp.com/servers
- [2026-03-27] **LobeHub MCP Marketplace**: 43,400+ servers indexed (Dev Skills 22.4k, Utility 4.8k, Productivity 2.2k); high discovery surface — https://lobehub.com/mcp
- [2026-03-27] **MCP security scanning servers** now a distinct category on MCPmarket.com — ecosystem maturing — https://mcpmarket.com/
- [2026-03-23] **MCP Apps (SEP-1865)** finalized; `ui://` iframes with bidirectional JSON-RPC bridge in Claude, ChatGPT, VS Code — https://devtk.ai
- [2026-03-26] **MCP Gateway 1.0** announced to provide a standardized routing layer for cross-tool communication — https://skillsllm.com
- [2026-03-26] **Figma write access** (March 24) via `use_figma` allows AI agents to create/modify frames/components — https://mcpmanager.ai
- [2026-03-26] **SurePath AI policy controls** (March 12) provide enterprise-grade governance for MCP tool usage — https://agentsource.co
- [2026-03-24] **Smithery listing is FREE** (no creator fee); Hobby/Pro plans for *hosted runtime* only — https://smithery.ai/pricing
- [2026-03-24] **Vinkius MCP Fusion** (vurb.ts framework) active on GitHub (v3.8.0 Mar 22) — https://github.com/vinkius-labs/mcp-fusion
- [2026-03-28] **Topsort MCP Server** (Mar 27) — auction-based retail media infrastructure; vertical-specific MCP acceleration — https://nationaltoday.com/us/ca/palo-alto/news/2026/03/27/topsort-launches-mcp-server-to-power-agent-operated-retail-media/
- [2026-03-28] **LILT MCP Server** — human-verified translation with agent-to-agent integration; enterprise vertical entrant — https://www.prnewswire.com/news-releases/lilt-launches-industry-first-mcp-server-and-agent-to-agent-integration-bringing-human-verified-translation-to-ai-assistants-302702081.html

### Market Size & TAM
- [2026-03-23] **Anthropic $19B annualized revenue** (March 2026); Claude Code alone $2.5B ARR — https://sacra.com/c/anthropic/
- [2026-03-24] **Claude Code Channels**: connect Claude Code to Discord/Telegram for ambient portfolio agents — https://venturebeat.com/orchestration/anthropic-just-shipped-an-openclaw-killer-called-claude-code-channels
- [2026-03-22] Crypto MCP TAM: 5–10% of technical users = 320K–640K; 8% conversion = 6,400–32,000 subs — Research and Markets

### Crypto/Finance Competitors
- [2026-03-25] **BitGo Official MCP** (Mar 25, 2026) — official wallet/trading server; NO tax/P&L — https://thepaypers.com
- [2026-03-24] **Nansen MCP** (Mar 12, 2026) — Smart Money signals, wallet profiling, on-chain analytics — https://www.pulsemcp.com/servers
- [2026-03-27] **MetaMask Tax Hub** (powered by Summ): 3,000+ wallet/exchange/DeFi integrations, IRS-ready reports, 30% MetaMask user discount — web2 competitor, NOT MCP — https://metamask.io/news/us-crypto-tax-reporting-2026
- [2026-03-26] **Bitkub community MCPs** (Gokub, @node2flow) now active; "zero presence" window is closed — https://github.com/node2flow-th
- [2026-03-24] **Bitkub pivots to $200M Hong Kong IPO** for late 2026; 75%+ local market share — https://financefeeds.com
- [2026-03-26] **IRS Form 1099-DA** e-file deadline is March 31, 2026; basis reporting mandatory for 2026 acquisitions — https://taxplaniq.com
- [2026-03-27] **1099-DA "gross problem"**: 2025 forms show gross proceeds ONLY (no cost basis); users must calculate basis manually → peak demand moment for tax MCP — https://www.accountingtoday.com/news/1099-da-rules-have-a-gross-problem-in-2026
- [2026-03-27] **IRS e-consent rule** (Mar 5, 2026): proposed alternative process for digital asset brokers to deliver 1099-DA electronically — https://vipwealthadvisors.com/insights/irs-form-1099-da-crypto-reporting-2026
- [2026-03-26] **Thailand Foreign Income Rule:** 2-year grace period proposal is STALLED; 2024 rules (taxable on remittance) apply — https://aimbangkok.com
- [2026-03-26] **Thailand Crypto Tax holiday:** 5-year personal income tax waiver (2025-2029) for capital gains on Thai-SEC licensed exchanges — https://aimbangkok.com
- [2026-03-28] PulseMCP "crypto tax" still **0 results** — first-mover window for tax engines fully open — https://pulsemcp.com/servers?q=crypto+tax
- [2026-03-28] **IRS Notice 2026-20** (Mar 18): lot identification relief extended through 2026 — brokers use taxpayer's own records; sustains manual-basis demand past tax season — https://www.currentfederaltaxdevelopments.com/blog/2026/3/18/extension-of-temporary-relief-for-digital-asset-identification-a-technical-review-of-notice-2026-20
- [2026-03-28] **Notice 2024-56**: brokers may issue 1099-DAs up to 12 months late; corrected forms possible until early 2027 — https://www.cointracker.io/blog/when-are-1099-das-due-to-the-irs

### SDK & Technical
- [2026-03-28] **Claude Code v2.1.85** (Mar 26): added `CLAUDE_CODE_MCP_SERVER_NAME`/`CLAUDE_CODE_MCP_SERVER_URL` env vars for multi-server scripts; conditional hook filtering — https://releasebot.io/updates/anthropic/claude-code
- [2026-03-28] **Computer use in Claude Code** now available for Pro/Max users (open files, run dev tools, click/navigate) — https://platform.claude.com/docs/en/release-notes/overview
- [2026-03-25] **OpenAI Agents SDK v0.12.5** (Mar 25, 2026) adds native MCP auth and retry logic — https://contextstudios.ai
- [2026-03-26] **VS Code v1.112**: Integrated browser debugging for MCP UIs and restricted sandboxing for local servers — https://infoworld.com
- [2026-03-24] **MCP TypeScript SDK v1.27.1** (Feb 24, 2026); **Python SDK v1.26** (Jan 24) — https://npmjs.com
- [2026-03-26] **Spring AI** (Mar 24, 2026) now supports MCP applications in the Java ecosystem — https://webrix.ai
- [2026-03-26] **Google ADK v2.0.0a1** (Mar 18, 2026) introduces Task API for structured agent delegation — https://gofastmcp.com
- [2026-03-24] **MCP Elicitation** (Claude Code, March 2026): servers request structured mid-call input (forms, pickers) — https://releasebot.io/updates/anthropic/claude-code
- [2026-03-27] **Elicitation + ElicitationResult hooks**: intercept/override elicitation responses before sending — custom UX flows — https://releasebot.io/updates/anthropic/claude-code
- [2026-03-27] **MCP tool descriptions capped at 2KB** in Claude Code — affects server manifest design — https://releasebot.io/updates/anthropic/claude-code
- [2026-03-26] **2026 Roadmap pillars:** Stateful Sessions, Horizontal Scaling, Agent-to-Agent Delegation, Discovery — https://gofastmcp.com
- [2026-03-27] **Claude Code MCP startup**: ~600ms faster launch for unauthenticated HTTP/SSE MCP servers — https://releasebot.io/updates/anthropic/claude-code
- [2026-03-27] **MCP Shadow IT risk** (Qualys TotalAI, Mar 19): MCP servers flagged as enterprise security risk; prompt injection & tool poisoning key attack vectors — https://blog.qualys.com/product-tech/2026/03/19/mcp-servers-shadow-it-ai-qualys-totalai-2026
- [2026-03-27] **MCP security stats**: 30 CVEs in 60 days; 38% of servers lack auth; 53% use static API keys; "MCPwned" at RSAC 2026 — https://astrix.security/learn/blog/state-of-mcp-server-security-2025/

### Opportunity Analysis
- [2026-03-24] **#1: Crypto Tax / 1099-DA MCP App** — 1099-DA + CARF now LIVE; zero competitors; use Elicitation for input UX
- [2026-03-23] **#2: Interactive Crypto Dashboard** — Visual charts/P&L inside Claude via SEP-1865; multi-client support
- [2026-03-26] **#3: Bitkub / Thai exchange MCP** — Shift to "Best-in-class UX" play as community servers now exist

### Pricing & Monetization
- [2026-03-24] **MCPize** (live): 85% revenue share, Stripe payouts, `@mcpize/cli` for one-click deployment — https://mcpize.com
- [2026-03-24] **MCP Hive** (launching May 11, 2026): per-request billing for high-value expert data — https://mcp-hive.com/
- [2026-03-26] **Masumi Network**: Agent-to-agent (A2A) payments and Kodosumi runtime for decentralized AI workflows — https://masumi.network
- [2026-03-24] **Apify** platform-wide $596K/month payouts (Dec 2025); top creators >$10K MRR; **21st.dev hit $10K MRR in 6 weeks** — https://apify.com/mcp/developers
- [2026-03-27] **x402 Protocol** (Coinbase): HTTP-native stablecoin payments; ~131K daily txns, avg $0.20/payment; best for crypto-native/permissionless use cases — https://www.x402.org/
- [2026-03-27] **Stripe MPP** (Machine Payments Protocol, Mar 18, 2026): session-based streaming payments; stablecoin + fiat; 100+ services at launch; backed by Anthropic/OpenAI/Visa/Mastercard/Shopify; best for enterprise/B2B — https://stripe.com/blog/machine-payments-protocol
- [2026-03-27] **x402 vs MPP**: x402 = permissionless/crypto-first (indie/DeFi); MPP = compliance-ready/fiat-first (enterprise/Stripe users) — https://workos.com/blog/x402-vs-stripe-mpp-how-to-choose-payment-infrastructure-for-ai-agents-and-mcp-tools-in-2026
- [2026-03-27] **MonetizedMCP**: open-source payment-enabled MCP framework using Fluora — https://www.monetizedmcp.org/
- [2026-03-27] **Moesif**: analytics + per-query billing middleware for MCP servers — https://www.moesif.com/blog/api-strategy/model-context-protocol/Monetizing-MCP-Model-Context-Protocol-Servers-With-Moesif/
- [2026-03-27] Less than **5% of 11,000+ MCP servers** are monetized — opportunity window still wide open — https://dev.to/namel/mcp-server-monetization-2026-1p2j
- [2026-03-28] **Agentic payments still tiny**: ~$28K/day total x402 volume, avg $0.20/payment — rails in place but pre-mainstream — https://workos.com/blog/x402-vs-stripe-mcp-how-to-choose-payment-infrastructure-for-ai-agents-and-mcp-tools-in-2026

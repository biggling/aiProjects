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
- [2026-03-24] **20,075 servers on Glama** (accurate count); PulseMCP at 12,432+; Smithery 7,300+ tools — https://glama.ai/mcp/servers
- [2026-03-23] **MCP Apps (SEP-1865)** GA since Jan 26, 2026; `ui://` iframes supported in Claude, ChatGPT, Goose, VS Code — https://blog.modelcontextprotocol.io/posts/2026-01-26-mcp-apps/
- [2026-03-22] Only ~5% of servers are monetized; 85% MoM growth; **97M monthly SDK downloads** (Python+TS combined) — https://anthropic.com/news/donating-the-model-context-protocol
- [2026-03-23] PulseMCP top-10: Datadog still #1 (33.8M/wk); Interactive UI Apps (Firecrawl, Excalidraw) climbing — https://www.pulsemcp.com/servers
- [2026-03-24] **Smithery listing is FREE** (no creator fee); Hobby/Pro plans are for *hosted runtime* only — no creator revenue share — https://smithery.ai/pricing
- [2026-03-24] **Vinkius MCP Fusion** (vurb.ts framework) active on GitHub (v3.8.0 Mar 22); website currently unreachable — https://github.com/vinkius-labs/mcp-fusion
- [2026-03-23] **SmartLoader trojanized MCP attack** (Feb 2026) targets crypto wallet holders via bogus GitHub MCP servers — https://thehackernews.com/2026/02/smartloader-attack-uses-trojanized-oura.html

### Market Size & TAM
- [2026-03-23] **Anthropic $19B annualized revenue** (March 2026); projects $26B full-year; Claude Code alone $2.5B ARR — https://sacra.com/c/anthropic/
- [2026-03-24] **Claude Code Channels**: connect Claude Code to Discord/Telegram for ambient portfolio MCP agents — https://venturebeat.com/orchestration/anthropic-just-shipped-an-openclaw-killer-called-claude-code-channels
- [2026-03-22] Crypto MCP TAM: 5–10% of technical users = 320K–640K; 8% conversion = 6,400–32,000 subs; $122K–$608K ARR at 1% capture @ $19/mo
- [2026-03-22] AI Code Tools market: $34.6B in 2026 → $91.3B by 2032 at 17.5% CAGR — Research and Markets

### Crypto/Finance Competitors
- [2026-03-24] **BitGo MCP** (Mar 23, 2026) — institutional wallet + trading for AI agents; NO tax, NO retail P&L — https://www.bakersfield.com/ap/news/bitgo-launches-mcp-server-bringing-institutional-grade-crypto-infrastructure-to-ai-agents/article_46b701e0-bab1-59dd-862c-c7dc6b6c5010.html
- [2026-03-24] **Nansen MCP** (Mar 12, 2026) — Smart Money signals, wallet profiling, on-chain analytics; no tax — https://www.pulsemcp.com/servers
- [2026-03-24] **CryptoQuant MCP** — 245 on-chain endpoints (whale tracking, market metrics); no tax — https://glama.ai/mcp/servers
- [2026-03-23] **CoinStats MCP** (Mar 18) — syncs CEX balances; NO cost basis, NO P&L, NO tax — https://glama.ai/mcp/servers/@CoinStatsHQ/coinstats-mcp
- [2026-03-23] **altFINS MCP** (Mar 11) — 150+ TA indicators; no portfolio P&L/tax — https://chainwire.org/2026/03/11/altfins-launches-crypto-analytics-data-api-and-mcp-for-algo-trading-ai-agents-and-trading-signals/
- [2026-03-23] **Bitkub**: zero MCP server; $66M daily volume; high-value regional gap — https://github.com/bitkub/bitkub-official-api-docs
- [2026-03-23] **TaxBit discontinued consumer crypto tax**; retail gap widened — https://taxbit.com
- [2026-03-24] **IRS Form 1099-DA reporting is LIVE in 2026**; **CARF** (international) also begins 2026 — expats in Thailand directly exposed — https://www.pwc.com/us/en/services/tax/library/global-crypto-tax-developments-in-2026.html
- [2026-03-24] PulseMCP "crypto tax" still **0 results** — first-mover window fully open — https://www.pulsemcp.com/servers?q=crypto+tax

### SDK & Technical
- [2026-03-24] MCP TypeScript SDK **v1.27.1** stable; Python SDK v1.26; spec version **2025-11-25** — no new release — https://blog.modelcontextprotocol.io
- [2026-03-23] **C# SDK v1.0 GA** (Mar 5, 2026) — .NET now first-class MCP platform — https://devblogs.microsoft.com/dotnet/release-v10-of-the-official-mcp-csharp-sdk/
- [2026-03-24] **MCP Elicitation** (Claude Code, March 2026): servers request structured mid-call input (forms, pickers) — key for tax year/wallet input UX — https://releasebot.io/updates/anthropic/claude-code
- [2026-03-24] Next spec release: **June 2026** (tentative); 2026 roadmap: enterprise SSO/audit trails, Streamable HTTP, `.well-known` server discovery

### Opportunity Analysis
- [2026-03-24] **#1: Crypto Tax / 1099-DA MCP App** — 1099-DA + CARF now LIVE; zero competitors; CARF adds expat (Thailand) angle; use Elicitation for input UX
- [2026-03-23] **#2: Interactive Crypto Dashboard** — Visual charts/P&L inside Claude via SEP-1865; multi-client (ChatGPT + Claude + VS Code); no competitor
- [2026-03-23] **#3: Bitkub / Thai exchange MCP** — Regional leader with zero MCP presence; IPO news adds urgency

### Pricing & Monetization
- [2026-03-24] **MCPize** (live): 85% revenue share, Stripe payouts, zero DevOps — strongest immediate option — https://mcpize.com
- [2026-03-24] **MCP Hive** (launching May 11, 2026): per-request billing; ideal for high-frequency crypto data — https://mcp-hive.com/
- [2026-03-24] **Masumi Network** (live): agent-to-agent micropayments for autonomous MCP workflows — https://www.masumi.network/blogs/monetization-of-mcp-servers
- [2026-03-23] Creem.io and Polar.sh confirmed for Thailand
- [2026-03-24] **Apify** platform-wide $596K/month payouts (Dec 2025); top creators >$10K MRR — https://apify.com/mcp/developers

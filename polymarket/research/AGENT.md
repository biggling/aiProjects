# polymarket — Research Agent

## Context
Prediction market bot for Polymarket. Currently in data collection phase.
Goal: find markets where the crowd probability is miscalibrated and bet systematically.

## Research Tasks

### 1. Open High-Volume Markets
Fetch: https://gamma-api.polymarket.com/markets?active=true&closed=false&limit=50&sort_by=volume
- What are the 10 highest-volume open markets right now?
- What categories dominate (politics, crypto, sports, geopolitics)?
- Which markets have prices near 50% (most uncertain = most exploitable)?
- Any markets closing in the next 7 days worth targeting?

### 2. Calibration Research
Search: "Polymarket calibration study 2026", "prediction market accuracy research", "Polymarket vs reality"
- Are Polymarket prices historically well-calibrated or systematically biased?
- Any academic studies on prediction market calibration published recently?
- Do sports markets vs. political markets differ in calibration?
- Any known Polymarket biases (recency bias, round number bias)?

### 3. Edge Opportunities
Search: "Polymarket edge strategy", "prediction market arbitrage 2026", "Polymarket CLOB liquidity"
- Are there arbitrage opportunities between Polymarket and other prediction markets (Kalshi, Manifold)?
- Any reported cases of easy-to-find market inefficiencies?
- Current liquidity on CLOB markets — what order sizes are realistic without slippage?

### 4. API & Data Access
Search: "Polymarket API 2026", "Polymarket CLOB API docs", "Polymarket historical data"
- Any updates to the Polymarket gamma API or CLOB API?
- Free historical resolution data available anywhere?
- Any community tools for Polymarket data analysis?

### 5. Other Prediction Markets
Search: "Kalshi vs Polymarket 2026", "prediction market comparison 2026", "Manifold Markets revenue"
- Is Kalshi accessible to non-US users in 2026?
- Any new prediction market platforms gaining liquidity?
- Cross-platform opportunities?

## Sources to Check
- https://polymarket.com (browse top markets)
- https://gamma-api.polymarket.com/markets (API — fetch and parse)
- Reddit r/Polymarket, r/predictionmarkets
- Manifold Markets (compare similar markets)
- Kalshi.com (US-regulated competitor)
- Hacker News: "prediction market" (recent posts)

## Decision Triggers — Flag if Found
- Market with >$100k volume where Polymarket price differs >10% from Kalshi → potential arb
- Paper/post showing specific Polymarket bias pattern → implement as signal in bot
- API endpoint change → update collector immediately
- New high-liquidity market category emerging → add to collection scope

# Shopee Affiliate — Implementation Plan

## Phase 1: Niche & Platform Research ← CURRENT
- [x] Research top Shopee affiliate niches in Thailand
- [x] Analyze successful Thai affiliate content creators
- [x] Identify best niches by commission × volume × feasibility
- [x] Draft platform strategy
- [ ] Validate with real Shopee affiliate dashboard data

## Phase 2: Product Scraper
- [ ] Build Shopee product scraper (trending, bestsellers, flash deals)
- [ ] Filter by commission rate ≥ 10%
- [ ] Store products in SQLite DB
- [ ] Daily auto-scrape via cron

## Phase 3: Content Generation
- [ ] Create content templates (review, comparison, deal alert)
- [ ] Use Claude API for Thai copywriting
- [ ] Generate images with product screenshots + overlays
- [ ] Generate short-form video scripts

## Phase 4: Publishing Automation
- [ ] Facebook page auto-posting (Graph API)
- [ ] TikTok content scheduling
- [ ] LINE Official Account integration
- [ ] UTM tracking on all affiliate links

## Phase 5: Analytics & Optimization
- [ ] Track clicks, conversions, commissions per post
- [ ] A/B test content formats
- [ ] Auto-promote winners, kill underperformers
- [ ] Weekly performance report

## Mega-Sale Campaign Calendar
3.3 (Mar) | 4.4 (Apr) | 5.5 (May) | 6.6 | 7.7 | 8.8 | 9.9 | 10.10 | 11.11 | 12.12
Plan content 2 weeks before each sale. Ramp up posting frequency 3 days before.

## Top Niches (Research Results)

### Tier 1 — High Commission + High Volume
1. **Beauty & Skincare** — 10-15% commission, massive Thai market, easy content
2. **Health Supplements** — 12-20% commission, repeat purchases, trust-based content
3. **Home & Kitchen Gadgets** — 10-15% commission, viral demo potential

### Tier 2 — Good Opportunity
4. **Baby & Kids** — 8-12% commission, loyal audience, seasonal spikes
5. **Fashion Accessories** — 10-15% commission, visual content, trend-driven

### Platform Strategy
- **Facebook**: Primary — review posts, deal alerts, comparison carousels. BiG has existing experience.
- **TikTok**: Secondary — short demo videos, unboxing, "TikTok made me buy it" format.
- **LINE**: Tertiary — deal alerts to OA subscribers, flash sale notifications.

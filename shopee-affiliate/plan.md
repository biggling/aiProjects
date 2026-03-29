# Shopee Affiliate — Implementation Plan

## Phase 0: Deep Market Research & Target Customer (DO FIRST)

**Goal:** Validate affiliate niche selection with real Shopee data and build laser-focused buyer profiles.

### Market Sizing & Validation
- [ ] Research Shopee affiliate program details for Thailand:
  - Commission rates by category (verify 10-20% range from research)
  - Cookie duration (how long after click does attribution last?)
  - Payment terms (monthly? minimum payout? Thai bank requirements?)
  - Top affiliate creators in Thailand — estimated monthly earnings
- [ ] Analyze Shopee Thailand bestsellers by category:
  - Top 50 products in Beauty & Skincare — avg price, commission, monthly sales
  - Top 50 in Health Supplements — same analysis
  - Top 50 in Home & Kitchen Gadgets — same analysis
  - Which specific products have >10% commission AND >100 daily sales?
- [ ] Research mega-sale performance data:
  - How much do affiliate commissions spike during 3.3, 4.4 etc. sales?
  - What content performs best pre-sale vs during sale?
  - Average order value during mega-sales vs normal days
- [ ] Calculate unit economics for affiliate content:
  - Cost: Claude API for Thai copy, image generation, scheduling tools
  - Revenue: avg clicks × conversion rate × avg commission per click
  - What volume of posts needed for ฿10K/month ($300)?

### Laser-Targeted Audience Persona
- [ ] **Primary audience: "Deal Hunter Dao"** — Thai female, 25-40:
  - Follows beauty/skincare pages on Facebook
  - Checks Shopee 2-3x/week, daily during mega-sales
  - Price sensitive: compares across sellers, waits for deals
  - Content that drives purchase: comparison posts, "ลดราคาเหลือ ฿X" (price drop alerts)
  - Trust triggers: real usage photos, detailed ingredient lists, before/after
  - Platform preference: Facebook (primary), LINE (deals), TikTok (discovery)
- [ ] **Secondary audience: "Gadget Seeker Gor"** — Thai male, 20-35:
  - Shops for: kitchen gadgets, tech accessories, home improvement
  - Higher impulse buy tendency for unique/viral products
  - Content that works: demo videos, "ของเจ๋งใน Shopee" (cool Shopee finds)
  - Platform: TikTok (primary), Facebook groups (secondary)
- [ ] Research Thai affiliate marketing landscape:
  - Who are the top 10 Thai Shopee affiliates? (Facebook pages, TikTok accounts)
  - What content format gets most engagement? (carousel? video? deal alert?)
  - What posting frequency do successful affiliates maintain?
- [ ] Join 5 Thai beauty/gadget review Facebook groups — observe what content gets engagement

### Competitor Deep-Dive
- [ ] Analyze 5 successful Thai Shopee affiliate Facebook pages:
  - Follower count, avg post engagement, posting frequency
  - Content format mix: review vs deal alert vs comparison vs unboxing
  - Which products they promote most (category patterns)
- [ ] Analyze 5 Thai Shopee affiliate TikTok accounts:
  - Follower count, avg video views, content style
  - Are they using AI-generated content or manual?
- [ ] Research LINE Official Account affiliate strategies:
  - How many Thai affiliate LINE OAs exist?
  - Subscriber growth tactics that work
  - Message frequency that doesn't cause unfollows

### Research Deliverables
- [ ] Product selection matrix: product × commission × daily sales × content difficulty
- [ ] Audience persona cards with platform preferences and buying triggers
- [ ] Competitor analysis: top 10 Thai affiliates with content strategy breakdown
- [ ] Revenue projection model: posts per week × expected clicks × conversion × commission
- [ ] Mega-sale calendar with content prep timeline (2 weeks before each sale)

---

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

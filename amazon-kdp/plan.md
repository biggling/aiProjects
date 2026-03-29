# Amazon KDP — Implementation Plan

## Phase 0: Deep Market Research & Target Customer (DO FIRST)

**Goal:** Validate specific book niches with real Amazon data and understand exactly who buys low-content books.

### Market Sizing & Validation
- [ ] Research Amazon KDP low-content book market:
  - Total low-content books on Amazon (journals, planners, logbooks) — estimate via search results
  - Market growth rate: is the niche growing or saturated in 2026?
  - Average monthly revenue for a new KDP publisher in first 6 months
- [ ] Deep-dive each target niche with real Amazon data:
  - **Specialized Logbooks**: search "fishing log book" — count results, check BSR #1-10 sales rank, review counts
  - **Gratitude Journals**: same analysis — is this oversaturated now?
  - **Password Organizers**: same — evergreen demand still confirmed?
  - **Fitness Trackers**: same — competition level?
  - **Budget Planners**: same
- [ ] For each niche, extract from top 10 BSR:
  - Price range, review count, BSR rank, page count, publish date, estimated monthly sales
- [ ] Research Amazon Ads costs for low-content books:
  - Average CPC for keywords like "fishing log book", "gratitude journal"
  - ACoS benchmarks for new KDP publishers (what's acceptable?)
  - Minimum ad budget needed to get traction ($5/day? $10/day?)
- [ ] Check KDP royalty calculator for each target price point:
  - At $6.99, $7.99, $9.99, $12.99 — what's the net royalty after printing costs?
  - How does page count affect printing cost and margin?

### Laser-Targeted Customer Persona
- [ ] **Primary persona: "Gift-Giving Grandma Gloria"** — buys journals as gifts:
  - Age: 50-70
  - Buys for: grandchildren, friends, church group, herself
  - Search behavior: "gratitude journal for women", "prayer journal", "garden planner"
  - Price sensitivity: $7.99-$12.99 (gift range)
  - What makes her buy: beautiful cover, 4+ star rating, good reviews, Prime shipping
  - What makes her NOT buy: <10 reviews, boring cover, unclear what's inside
- [ ] **Secondary persona: "Niche Hobbyist Hugo"** — buys logbooks for specific hobbies:
  - Age: 30-60
  - Buys: fishing log, bird watching journal, wine tasting log, garden planner
  - Search behavior: very specific long-tail ("bass fishing log book with weather tracking")
  - Price sensitivity: $8.99-$14.99 (willing to pay more for specialized content)
  - What makes him buy: comprehensive interior layout, spiral-bound option, size appropriate for use
- [ ] **Tertiary persona: "New Year's Resolution Rachel"** — seasonal buyer:
  - Age: 25-40
  - Buys: fitness trackers, meal planners, budget planners, habit trackers
  - Peak buying: December-January (New Year), September (back to school)
  - Price sensitivity: $7.99-$9.99
  - Impulse buy trigger: "New Year, New Me" marketing + clean modern cover design
- [ ] Read 100+ reviews on top-selling books in each niche:
  - What do 5-star reviews praise? (layout? paper quality? size? cover?)
  - What do 1-3 star reviews complain about? (too thin? too few pages? useless layout?)

### Competitor Deep-Dive
- [ ] Buy top-selling book in each target niche ($6-$12 each, ~$30-$60 total research investment):
  - Analyze interior layout, paper quality, page count
  - Document what's good and what BiG's version can improve
- [ ] Identify top 5 KDP publishers in low-content niche:
  - How many books do they have? (typically 50-200+)
  - What's their publishing velocity?
  - Do they use AI-generated covers? What tools?
- [ ] Research cover design trends for 2026:
  - What styles are selling? (minimalist? illustrated? photo? typography-focused?)
  - Canva vs custom Pillow-generated covers — quality comparison

### Research Deliverables
- [ ] Niche validation matrix: niche × search volume × competition × margin × seasonal pattern
- [ ] Customer persona cards with buying triggers and search behavior
- [ ] Top competitor analysis: publisher × book count × avg BSR × avg reviews × price
- [ ] Interior layout requirements per niche (page count, features, size)
- [ ] Launch priority: which 3 books to publish first for fastest first sale

---

## Phase 1: Niche Research & Validation ← COMPLETE
- [x] Research top low-content book niches
- [x] Analyze competition levels and pricing
- [x] Identify 3-5 viable book concepts
- [x] Rank by demand × competition × ease

## Phase 2: Interior Generation
- [x] Build lined page generator
- [x] Build dot grid generator
- [x] Build template system for custom interiors
- [ ] Add weekly/monthly planner layouts
- [ ] Add tracker templates (habit, mood, fitness)
- [ ] Generate full PDF interiors with front/back matter

## Phase 3: Cover Design
- [ ] Create cover templates (Pillow-based)
- [ ] Implement text overlay with fonts
- [ ] Add background patterns/textures
- [ ] Generate spine text (based on page count)
- [ ] Output KDP-ready cover PDF (with bleed)

## Phase 4: KDP Publishing
- [ ] Automate KDP manuscript upload (Playwright)
- [ ] Auto-fill book details (title, description, keywords)
- [ ] Set pricing (cost + margin calculator)
- [ ] Track published books in SQLite

## Phase 5: Ads & Optimization
- [ ] Amazon Ads API integration
- [ ] Keyword bid automation
- [ ] Sales tracking and ROI analysis
- [ ] Auto-pause underperforming ads

## Top Niche Opportunities

### Tier 1 — Low Competition, Good Demand
1. **Specialized Logbooks** — fishing log, bird watching, wine tasting, garden planner
   - BSR top 10 often have <50 reviews, price $6.99-$9.99
2. **Gratitude Journals** — still growing, easy interior, $7.99-$12.99
3. **Password Organizers** — evergreen demand, simple layout, $5.99-$7.99

### Tier 2 — Medium Competition, High Demand
4. **Fitness/Workout Trackers** — $8.99-$12.99, needs good cover
5. **Budget Planners** — monthly expense trackers, $7.99-$9.99

### Tier 3 — Seasonal
6. **Academic Planners** — Aug-Jul cycle, high volume June-August
7. **Meal Planners** — New Year spike, steady otherwise

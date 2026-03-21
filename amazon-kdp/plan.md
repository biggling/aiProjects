# Amazon KDP — Implementation Plan

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

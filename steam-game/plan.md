# Steam Game — Implementation Plan

## Game: Sigil Spin (Working Title)
A roguelike slot machine where you spin magical sigils to cast spells against waves of enemies.

## Phase 0: Deep Market Research & Target Player (DO FIRST)

**Goal:** Validate Sigil Spin concept against real indie game market data and define exact target player profile.

### Market Sizing & Validation
- [ ] Research roguelike market on Steam:
  - Total roguelike games on Steam (SteamDB or SteamSpy data)
  - How many roguelike releases per month in 2025-2026?
  - Median revenue for indie roguelike at $4.99 (SteamSpy estimates)
- [ ] Research slot machine / luck-based mechanic games:
  - **Luck Be a Landlord**: total sales, reviews, revenue estimate, launch date
  - **Balatro**: same analysis (card-game roguelike, massive hit)
  - **Coin Crypt**: same (older, coin-based roguelike)
  - What made Balatro succeed? (marketing? streamer coverage? demo? game feel?)
- [ ] Research Steam launch benchmarks for solo indie devs:
  - Avg wishlist-to-sale conversion rate (typically 10-20%)
  - How many wishlists needed for a "good" launch? (5K-10K minimum)
  - What's a realistic first-week sales target for a $4.99 roguelike?
- [ ] Calculate development cost vs expected revenue:
  - BiG's time investment (hours × opportunity cost)
  - Asset costs (music, SFX, art — can these be free/cheap?)
  - Steam's 30% cut + taxes = net revenue per sale
  - Break-even analysis: how many copies to cover costs?
- [ ] Research Steam Next Fest and demo strategy:
  - When is the next Steam Next Fest? (quarterly — find closest date)
  - Does having a demo correlate with higher wishlists? (data from Steam Labs)

### Laser-Targeted Player Persona
- [ ] **Primary persona: "Roguelike Ron"** — dedicated roguelike/deckbuilder player:
  - Age: 20-35, male (80%+ of indie roguelike audience)
  - Plays: Slay the Spire, Balatro, Luck Be a Landlord, Vampire Survivors
  - Session length: 30-60 minutes (lunch break or evening wind-down)
  - What hooks him: "one more run" feeling, deep synergy systems, satisfying combo moments
  - What turns him off: unfair RNG (feels rigged), lack of depth, slow early game
  - Discovery: Steam Discovery Queue, YouTube (NorthernLion, Wanderbots), Reddit, Steam curator lists
  - Price sensitivity: $4.99-$9.99 is impulse buy territory
- [ ] **Secondary persona: "Casual Slot Spinner Cathy"** — broader audience:
  - Attracted by slot machine aesthetics (dopamine hits)
  - Plays: mobile games, casual Steam games
  - Lower tolerance for complexity — needs clear "spin and watch things happen" satisfaction
  - Would buy if: visuals are pretty, price is low, looks fun in a 30-second trailer
- [ ] Research what makes players wishlist vs buy:
  - Analyze top wishlisted roguelikes — what do their store pages have in common?
  - Study Steam store page best practices: capsule image, trailer, screenshots, tags, description
  - What tags should Sigil Spin use? (roguelike, slot machine, deckbuilding, strategy, indie)
- [ ] Study Balatro's launch strategy in detail:
  - Pre-launch marketing timeline
  - Streamer/YouTuber coverage strategy
  - Demo strategy
  - Pricing ($14.99 — higher than our target, but massive success)

### Competitor Deep-Dive
- [ ] Play and analyze the top 5 luck-based roguelikes:
  - Balatro, Luck Be a Landlord, Coin Crypt, Dicey Dungeons, Slot Quest
  - For each: core loop, session length, depth of synergies, review sentiment
- [ ] Identify what Sigil Spin does differently:
  - Slot machine + spell casting + enemy combat = unique combo?
  - Is this different enough from existing games to stand out?
- [ ] Read negative reviews of competitors: what are players asking for that doesn't exist?
- [ ] Research game jams — are there similar concepts in itch.io game jam entries?

### Player Discovery Channels
- [ ] Identify top 10 YouTubers/streamers who cover indie roguelikes
- [ ] Research r/roguelikes, r/IndieGaming, r/Steam community size and engagement
- [ ] Check Steam curator lists for roguelike/deckbuilder focus
- [ ] Research itch.io as a demo/pre-release platform

### Research Deliverables
- [ ] Competitive landscape matrix: game × reviews × sales estimate × price × unique mechanic
- [ ] Player persona card with buying triggers and discovery channels
- [ ] Revenue projection model: wishlists → sales at different conversion rates
- [ ] Marketing channel priority list for pre-launch
- [ ] "What makes Sigil Spin unique" positioning statement (1 sentence)

---

## Phase 1: Concept & Prototype ← COMPLETE
- [x] Research successful indie games
- [x] Brainstorm 3 concepts
- [x] Select best concept (Sigil Spin)
- [x] Write Game Design Document
- [x] Set up Godot project structure

## Phase 2: Core Mechanic
- [ ] Implement reel spinning system (3 reels, 5 sigil types)
- [ ] Implement sigil matching/combo detection
- [ ] Basic spell effects (damage, heal, shield)
- [ ] Enemy spawner with HP bars
- [ ] Gold/reward system
- [ ] Game over condition

## Phase 3: Progression & Meta
- [ ] Sigil upgrade system (common → rare → legendary)
- [ ] Shop between waves
- [ ] Sigil pool management (add/remove sigils from reels)
- [ ] Difficulty scaling per wave
- [ ] Score/leaderboard

## Phase 4: Content
- [ ] 20+ unique sigils with synergy effects
- [ ] 10+ enemy types with different behaviors
- [ ] 5 boss encounters
- [ ] 3 environment themes
- [ ] Sound effects and music

## Phase 5: Polish & Launch
- [ ] Steam Store page (screenshots, trailer, description)
- [ ] Achievements integration (Steamworks)
- [ ] Settings menu (audio, display, controls)
- [ ] Save/load system
- [ ] Beta testing
- [ ] Launch at $4.99

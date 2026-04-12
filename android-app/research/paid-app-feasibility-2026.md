# Paid Android App — Market Feasibility Research
_Last updated: 2026-04-05_

> **Goal:** Identify and rank viable paid Android app concepts for a solo developer (Kotlin expert, Bangkok-based, ~5 hrs/week). Focus on upfront paid or one-time IAP models — no subscription backend required.

---

## Context: Why Paid Apps Now

- **Subscription fatigue is real**: 2025 Google Play developer blog explicitly pushed new tooling for "one-time products" — market signal
- **Poweramp (paid music player)** is the #1 top-paid Android app in Thailand by downloads — proves Thai users DO buy paid apps
- **56% of Thai users** have purchased a smartphone app (2021 baseline; likely higher in 2025)
- Paid app revenue in Thailand: ~$60M/year (vs $484M ad revenue) — smaller but dedicated buyer segment
- Regional pricing on Play Store allows ~฿29–69 ($0.79–$1.99 USD) which dramatically increases Thai conversions

---

## Ranking Framework

Each concept is scored 1–5 on:

| Dimension | Description |
|-----------|-------------|
| **Market Size** | Addressable downloads in this category |
| **Competition** | Lower = better (1 = crowded, 5 = clear gap) |
| **Build Effort** | Solo dev, 5 hrs/week (5 = can ship in <4 weeks) |
| **Revenue Ceiling** | Max realistic monthly revenue at steady state |
| **Thai Fit** | Relevance to Thai/SEA Android market |
| **Differentiation** | Unique angle vs existing apps |

**Total = average of all 6 (max 30)**

---

## Candidate Products

### 1. QuickBlock — Daily Time Block Planner *(existing concept)*
> Free + AdMob + one-time IAP (~$2.99 unlock premium)

| Dimension | Score | Notes |
|-----------|-------|-------|
| Market Size | 3 | <200K total installs in niche — small but unclaimed |
| Competition | 5 | No Android-native time blocker; competitors have critical bugs |
| Build Effort | 2 | 5 screens + Room DB + widgets + streaks = 6–8 weeks minimum |
| Revenue Ceiling | 2 | Ad-supported: needs 1,000–2,000 Thai DAU for $100/mo |
| Thai Fit | 5 | No Thai-language time blocker exists; confirmed gap |
| Differentiation | 4 | Thai lang + crash-free + free recurring blocks = uncontested |
| **Total** | **21/30** | |

**Model verdict**: Ad-supported works only at scale. IAP conversion 2–5% is slim on small base. Better as portfolio/learning project than revenue vehicle short-term.

---

### 2. Sound Machine / White Noise — Premium Paid *(new)*
> One-time paid app ($1.49–$2.99) — offline ambient sound player, curated packs

| Dimension | Score | Notes |
|-----------|-------|-------|
| Market Size | 4 | Sleep/focus audio market growing; "Relax Melodies" has 10M+ installs |
| Competition | 2 | Highly saturated; Relax Melodies, Sleep Sounds, Noisli all established |
| Build Effort | 5 | Simple audio player + local assets; shippable in 2–3 weeks |
| Revenue Ceiling | 2 | Requires large volume; one-time paid = $0.40–$0.60 net per sale after Play cut |
| Thai Fit | 3 | Generic; no Thai-specific angle |
| Differentiation | 2 | Hard to stand out without unique sound packs or hook |
| **Total** | **18/30** | |

**Model verdict**: Easy to build but hard to discover. No organic growth engine. Skip unless you have a unique sound angle (Thai ambient sounds, workplace focus packs).

---

### 3. Offline Password Vault — One-Time Paid *(new)*
> Paid ~$1.99–$2.99 one-time; local-only, no sync, no subscription, no server

| Dimension | Score | Notes |
|-----------|-------|-------|
| Market Size | 4 | Password managers: 200M+ users globally; "local-only" is underserved |
| Competition | 3 | Cloud PMs dominate (Bitwarden free, LastPass); local-only niche is less crowded |
| Build Effort | 3 | Encryption (AES-256), biometric lock, import/export — 4–6 weeks |
| Revenue Ceiling | 3 | $1.99 × 500 sales/month = $600/mo possible if ranked well |
| Thai Fit | 3 | Thai users distrust cloud storage; local-only pitch resonates |
| Differentiation | 4 | "No subscription, no cloud, no account" — strong counter-positioning |
| **Total** | **20/30** | |

**Model verdict**: Viable. Trust narrative is strong — but security-critical apps face higher review scrutiny and user skepticism. Requires solid encryption UX. Better if bundled with export/backup.

---

### 4. ADHD/Visual Daily Planner — One-Time Paid *(new)*
> Paid ~$2.99–$4.99; hyper-visual, distraction-reduced, ADHD-friendly time planner

| Dimension | Score | Notes |
|-----------|-------|-------|
| Market Size | 3 | ADHD apps growing fast; Tiimo (iOS) breakout 2025; Android gap confirmed |
| Competition | 4 | Very few ADHD-specific paid planners on Android; Tiimo Android launched recently |
| Build Effort | 2 | Heavily visual/custom UI; 6–10 weeks to build properly |
| Revenue Ceiling | 4 | ADHD community pays premium; $4.99 one-time is accepted; niche but loyal |
| Thai Fit | 2 | ADHD diagnosis awareness lower in Thailand; niche too specific for Thai market |
| Differentiation | 4 | ADHD-specific UX (large targets, time-blindness features, minimal clutter) is novel |
| **Total** | **19/30** | |

**Model verdict**: Strong globally but weak Thai fit. Would need English-first strategy with ASO targeting "ADHD planner", "time blindness app". Not ideal for local-first approach.

---

### 5. Network/WiFi Analyzer — One-Time Paid *(new)*
> Paid ~$1.49–$2.99; offline WiFi scanner, IP info, port check, LAN tools

| Dimension | Score | Notes |
|-----------|-------|-------|
| Market Size | 3 | Technical utility; ~500K installs for Fing (free), Network Analyzer ($2.99) |
| Competition | 3 | Fing dominates free tier; Wifi Analyzer free; paid niche exists but thin |
| Build Effort | 4 | API-driven, no backend; WifiManager + network APIs; shippable in 3–4 weeks |
| Revenue Ceiling | 2 | Technical niche; low search volume; $200–500/month ceiling without breakout |
| Thai Fit | 3 | IT workers in Thailand; but Fing covers most needs for free |
| Differentiation | 3 | Could bundle: WiFi + Bluetooth + port scanner in one paid app |
| **Total** | **18/30** | |

**Model verdict**: Buildable fast but revenue ceiling is low. Good to add to portfolio, but not a primary income vehicle.

---

### 6. Habit Tracker — One-Time Paid, Offline-First *(new)*
> Paid ~$1.99–$3.99; minimal, offline, streak-based; counter to Loop (free/open-source) with richer analytics

| Dimension | Score | Notes |
|-----------|-------|-------|
| Market Size | 4 | Habit tracking: Habitify 3M+ users; consistent search volume; proven demand |
| Competition | 3 | Loop (free) dominates minimalist space; paid niche open for analytics-rich version |
| Build Effort | 4 | Simpler than QuickBlock; no time-based blocks; 3–4 weeks |
| Revenue Ceiling | 3 | $2.99 × 300 downloads/month = $540/mo; realistic with organic growth |
| Thai Fit | 3 | Universal use case; Thai-language support = ranking boost |
| Differentiation | 4 | Paid = ad-free forever promise; offline-first; richer charts than Loop |
| **Total** | **21/30** | |

**Model verdict**: Tied with QuickBlock at 21. Better revenue model (paid upfront vs ad-dependent). Faster to build. Lower risk. Strong candidate.

---

### 7. Markdown / Plain-Text Journal — One-Time Paid *(new)*
> Paid ~$2.99–$4.99; local markdown journal, encrypted, no cloud, no account

| Dimension | Score | Notes |
|-----------|-------|-------|
| Market Size | 3 | Journaling apps: Daylio 10M+ installs; paid market smaller but real |
| Competition | 3 | Obsidian (free PC-first), Notion (free/subscription), Journal apps saturated |
| Build Effort | 3 | Markdown rendering + local storage + encryption = 4–5 weeks |
| Revenue Ceiling | 3 | $2.99 × 400 sales/month = ~$720/mo ceiling if well-reviewed |
| Thai Fit | 2 | Journaling culture weaker in Thailand; English-first market |
| Differentiation | 3 | "Buy once, private forever" angle vs Notion subscription |
| **Total** | **17/30** | |

**Model verdict**: Competitive space. Obsidian + local note apps already well-covered. Not recommended unless you have a truly unique UI hook.

---

### 8. Interval Timer / Workout Timer — One-Time Paid *(new)*
> Paid ~$1.99; offline interval timer (HIIT, Tabata, custom), no ads, no subscription

| Dimension | Score | Notes |
|-----------|-------|-------|
| Market Size | 4 | Fitness app market booming; interval timers are evergreen utility |
| Competition | 2 | Many free apps; Seconds Pro ($4.99) is paid incumbent with 1M+ installs |
| Build Effort | 5 | Very simple: timer logic + audio cues + widget; shippable in 1–2 weeks |
| Revenue Ceiling | 2 | Low price ceiling; Seconds Pro already well-entrenched |
| Thai Fit | 3 | Fitness culture growing in Thailand; but free alternatives abundant |
| Differentiation | 2 | Hard to beat Seconds Pro without meaningful UI innovation |
| **Total** | **18/30** | |

**Model verdict**: Fastest to build but worst differentiation. Only viable with a strong design angle (e.g., minimalist, Muay Thai/Thai fitness theme).

---

### 9. Clipboard Manager — One-Time Paid *(new)*
> Paid ~$1.49–$1.99; persistent clipboard history, snippets, quick paste widget

| Dimension | Score | Notes |
|-----------|-------|-------|
| Market Size | 3 | Developer/power user tool; Clipper+ has 1M+ installs; Clip Stack (free) |
| Competition | 3 | Free tier dominated by Clip Stack; paid niche exists (Clipper+) |
| Build Effort | 4 | Accessibility service + overlay widget; 2–3 weeks; some OEM friction |
| Revenue Ceiling | 2 | Small TAM; $300–500/month realistic ceiling |
| Thai Fit | 2 | Power user tool; limited Thai-specific angle |
| Differentiation | 3 | "Privacy-first local clipboard" vs cloud solutions |
| **Total** | **17/30** | |

**Model verdict**: Decent build project but low revenue potential. Android 14+ accessibility service restrictions add maintenance burden.

---

### 10. Pomodoro + Task Combo — One-Time Paid *(new)*
> Paid ~$2.99–$4.99; Pomodoro timer tightly coupled to task list; offline; no subscription

| Dimension | Score | Notes |
|-----------|-------|-------|
| Market Size | 4 | Pomodoro apps: Focus To-Do 11M installs; proven demand |
| Competition | 3 | Focus To-Do owns this space but has many complaints ($1.99/mo paywall, no calendar sync) |
| Build Effort | 3 | Timer + task list + notifications = 4–5 weeks |
| Revenue Ceiling | 4 | $2.99 × 600 sales/month = ~$1,100/mo; strong upside if Focus To-Do users defect |
| Thai Fit | 4 | Focus To-Do is popular in Thailand; one-time paid version could outrank it |
| Differentiation | 4 | "Buy once, no subscription" vs Focus To-Do's $1.99/mo — direct counter-positioning |
| **Total** | **22/30** | **TOP RANKED** |

**Model verdict**: Highest score. Focus To-Do has 11M installs but a growing backlash against its subscription model. A one-time paid Pomodoro+Task app directly exploits that gap. Thai fit is strong (Focus To-Do is already popular here — users know the category).

---

## Summary Ranking

| Rank | App Concept | Score | Model | Est. Monthly Rev (steady state) | Build Time |
|------|-------------|-------|-------|----------------------------------|------------|
| **1** | Pomodoro + Task (one-time paid) | **22/30** | $2.99 one-time | $600–$1,100 | 4–5 weeks |
| **2** | QuickBlock (freemium + IAP) | **21/30** | Free + AdMob + $2.99 IAP | $100–$300 | 6–8 weeks |
| **2** | Habit Tracker (one-time paid) | **21/30** | $1.99–$2.99 one-time | $300–$540 | 3–4 weeks |
| **4** | Offline Password Vault | **20/30** | $1.99 one-time | $400–$600 | 4–6 weeks |
| **5** | ADHD Visual Planner | **19/30** | $3.99–$4.99 one-time | $500–$800 (global) | 6–10 weeks |
| **6** | Sound Machine | **18/30** | $1.49 one-time | $100–$200 | 2–3 weeks |
| **6** | Network/WiFi Analyzer | **18/30** | $1.49–$2.99 one-time | $200–$400 | 3–4 weeks |
| **6** | Interval Timer | **18/30** | $1.99 one-time | $100–$200 | 1–2 weeks |
| **9** | Markdown Journal | **17/30** | $2.99–$4.99 one-time | $400–$720 | 4–5 weeks |
| **9** | Clipboard Manager | **17/30** | $1.49 one-time | $100–$300 | 2–3 weeks |

---

## Head-to-Head: Top 3 vs QuickBlock

| Factor | QuickBlock | Pomodoro+Task | Habit Tracker |
|--------|-----------|--------------|---------------|
| Revenue model | AdMob + IAP | Paid upfront | Paid upfront |
| Revenue at 500 installs/mo | ~$15–50 (ad) | ~$900 (2% conversion) | ~$450 |
| Build complexity | High | Medium | Low |
| Time to first dollar | Weeks (needs DAU) | Day 1 | Day 1 |
| Thai market gap | Confirmed | Strong (Focus To-Do users) | Moderate |
| Organic discovery risk | Low (no Thai competitor) | Medium (busy category) | Medium |
| Maintenance burden | High (ads SDK, streak engine) | Low | Low |
| Competitive moat | Thai language + reliability | Price vs Focus To-Do | Offline + charts |

---

## Recommendation

### If starting fresh: **Pomodoro + Task (one-time paid, $2.99)**
- Fastest path to revenue (paid = earns on install #1)
- Focus To-Do has a documented subscription backlash — you can own that positioning
- Simpler architecture than QuickBlock (no block timeline, no weekly view)
- Thai users already familiar with Focus To-Do = category awareness exists

### If continuing QuickBlock: **Reframe as one-time paid ($2.99) not free+ads**
- Replace AdMob with a single $2.99 lifetime purchase
- Rationale: 1 sale = same as ~1,500 ad impressions at Thai eCPM; much simpler to maintain
- Free tier: basic blocks (5/day); Paid: unlimited + widget + recurring blocks
- This aligns with the #1 user request across all time-block competitors: "no subscription"

### Minimum viable paid app path (fastest): **Habit Tracker**
- Build in 3–4 weeks vs 6–8 for QuickBlock
- Simpler Room schema (habits, completions, streaks) vs time-based block system
- Proves the paid model before investing in QuickBlock's complexity
- Can share streak/gamification code with QuickBlock later

---

## Key Data Points to Retain

- **Poweramp** = #1 paid Android app in Thailand → proves paid apps sell in TH
- **Focus To-Do** = 11M installs, $1.99/mo subscription = top complaint target
- **Habit trackers**: HabitNow $9.99, Way of Life $4.99, Habitify $4.99 — all viable one-time paid
- **Thai willingness to pay**: 56% have paid for an app; regional pricing (50–70% discount) increases conversion
- **New Google Play tooling (2025)**: Explicit support for one-time purchase product management — platform endorsement
- **Revenue reality**: $500–$1,100/month realistic ceiling for a well-executed solo paid app; not full-time income, but sustainable passive revenue at 5 hrs/week maintenance

---

_Sources: AppBrain paid rankings, SensorTower, BusinessofApps, 42matters Thailand stats, Statista TH paid app data, Android Developers Blog (2025-07 one-time products), RevenueCat State of Subscriptions 2025_

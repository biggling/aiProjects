# android-app — Research Agent

## Agent Instructions

1. **Read `## Known Facts` below first.** Do not re-research any fact already listed there.
2. Focus only on questions marked ❓ (unknown) or facts that may have changed since their `[date]`.
3. After saving findings, **update `## Known Facts`** — add new facts, update changed ones, remove stale ones.
4. Keep Known Facts concise: one line per fact, with date and source URL.

---

## Known Facts
<!-- Agent updates this section after each run. Date format: YYYY-MM-DD -->

### Play Store Productivity Benchmarks
- [2026-03-24] Productivity is #3 fastest-growing Play Store category: 10.03% growth, 123,533 apps — BusinessofApps
- [2026-03-24] Top apps: Todoist (10M+, 4.4★), TickTick (5-10M+, 4.6★), Forest (10M+, 4.4★), Focus To-Do (10M+, 4.6★), Sectograph (6.9M, 4.64★) — AppBrain/AppFollow
- [2026-03-24] Freemium + subscription dominates: 82% of non-gaming Play Store revenue; subscriptions clearly winning — BusinessofApps
- [2026-03-24] Price sweet spot: Free core + $1.99–3.99/mo or $19.99/yr + lifetime unlock ~$29.99 — market analysis
- [2026-03-24] Ads during focus sessions = direct rating killer; top feature request is ad-free focus experience — Play Store reviews

### AdMob Revenue Benchmarks
- [2026-03-24] Thailand AdMob banner eCPM: ~$0.27; interstitial: $2.00–$3.78 (up 48% in 2024); Tier 3 market — AnyMind/Playwire
- [2026-03-24] Thai-majority productivity app needs 1,000–2,000 DAU to earn $100/month (interstitial focus, 70% fill) — calculated from AnyMind data
- [2026-03-24] AdMob mediation (AppLovin MAX + Meta AN) increases effective eCPM 20–40% over AdMob-only for Tier 3 — Tenjin 2025 report
- [2026-03-24] Productivity apps earn ~0.8x gaming eCPM; global interstitial $2.50–$5.00, rewarded $8–$18 — Playwire benchmarks
- [2026-03-24] Seasonal eCPM peak: September–November (back-to-school + pre-holiday ad spend)

### Competitor App Analysis
- [2026-03-24] **TimeBloc: iOS ONLY — no Android version exists** — major gap for Android users wanting visual time blocking — Play Store/JustUseApp
- [2026-03-24] Structured: Android launched Nov 2023 (very new); iOS-first; many features still Android-missing; recurring tasks paywalled; 4.8★ — AppBrain/JustUseApp
- [2026-03-24] Forest: 44M downloads, 4.4★ Android (vs 4.8★ iOS); free; top complaints: tree dies on any app switch, no pause/resume, battery-drain false errors — JustUseApp
- [2026-03-24] Sectograph: 6.8M downloads, 4.64★; one-time Pro purchase (no subscription); users explicitly praise no-sub model; complaints: widget too small, zero dev support — Play Store
- [2026-03-24] Focus To-Do: 11M downloads, 4.6★; $1.99/mo or $11.99 lifetime; top missing: calendar integration, multiple simultaneous timers — AppBrain/review
- [2026-03-24] Freedom: 1.7M downloads, 4.1★; $39.99/yr subscription; VPN-based blocking trivially bypassed; outdated UI — G2/Trustpilot
- [2026-03-24] Gap confirmed: no Android-native, no-subscription, widget-reliable daily time block planner; Android underserved vs iOS — cross-competitor analysis

### Kotlin / Jetpack Compose Updates
- [2026-03-24] Compose 1.10 (BOM 2025.12.00, Dec 2025): scroll parity with Views, pausable lazy prefetch, `retain` API — Android Developers blog
- [2026-03-24] Room 3.0 (alpha Mar 2026, `androidx.room3`): KSP-only, coroutines-first, KMP support; Room 2.x entering maintenance — Android Developers
- [2026-03-24] Android 15 (API 35): edge-to-edge enforced, FGS types required + 6h cap on dataSync/mediaProcessing, notification cooldown — Android release notes
- [2026-03-24] `POST_NOTIFICATIONS` runtime permission required since API 33 (must request contextually) — Android Developers
- [2026-03-24] `PACKAGE_USAGE_STATS` is NOT runtime permission — requires manual user grant via Settings; use `ACTION_USAGE_ACCESS_SETTINGS` intent
- [2026-03-24] Use WorkManager (not FGS) for background reminders to avoid Android 15 FGS restrictions — Android best practices
- [2026-03-24] **Play Store mandate**: All new apps/updates must target API 35+ (deadline was Aug 31, 2025, already passed) — QuickBlock must target API 35 from day one
- [2026-03-24] Kotlin 2.3.0 (Dec 2025) is latest stable; K2 compiler ~48% faster clean builds — JetBrains blog

### Thai Android Market
- [2026-03-24] Android market share Thailand: 65.91% (iOS: 33.68%) — Statcounter Feb 2026
- [2026-03-24] Thai-language productivity apps: gap confirmed, none dominant in Thai Play Store top charts — Tracxn/Play Store analysis
- [2026-03-24] Thai monetization: 39% devs use ads (vs 27% global); users expect productivity apps free; 2-3x lower WTP than West — 42matters
- [2026-03-24] Gaming IAP thriving: Thailand #1 in SEA at $162M Q1 2025 — Sensor Tower
- [2026-03-24] Google sideloading "Accountability Layer": Thailand is pilot country, Sept 2026 target → Play Store dominance reinforced — Google/MDES announcement
- [2026-03-24] Asia Day 1 retention: 27%; Day 7: **8.1%** — habit-forming mechanics (streaks, daily reminders) critical to retain users — DataReportal/42matters
- [2026-03-24] 78% of Thai consumers prioritize "ease and convenience" — minimal-friction UX is non-negotiable — Iconic Thai consumer insights

---

## Context
Android app for Play Store. Concept: "QuickBlock" — productivity/focus tool.
Stack: Kotlin + Jetpack Compose. Monetization: Google AdMob + optional in-app purchase.
Target: Thai + English-speaking Android users.

## Research Tasks

### 1. Play Store Productivity Apps — Benchmarks
Search: "Google Play productivity app revenue 2026", "focus app Play Store downloads", "best productivity Android apps 2026"
- What are the top productivity/focus apps on Play Store by downloads and rating?
- What features do users rate highest in competitor focus apps (timers, blocking, gamification)?
- Price models: free+ads vs. freemium vs. one-time purchase — what's winning?

### 2. AdMob Revenue Benchmarks
Search: "AdMob eCPM productivity app 2026", "Android app AdMob revenue calculator", "Thailand AdMob eCPM rate"
- Current AdMob eCPM for productivity app category (interstitial, banner, rewarded)?
- Thailand-specific eCPM rates (often lower than US — need volume data)?
- How many daily active users needed to earn $100/month from AdMob?

### 3. Competitor App Analysis — Focus/Block Apps
Search: "QuickBlock app Android", "app blocker Android 2026", "focus timer app Android review"
- What app blockers/focus apps exist on Play Store? (Forest, Freedom, etc.)
- What are their 1-star complaints (what do users hate)?
- What features are missing that users frequently request?
- Is there a gap for a simpler, no-subscription focus tool?

### 4. Kotlin + Jetpack Compose Updates
Search: "Jetpack Compose 2026 updates", "Android development best practices 2026", "Kotlin Compose performance tips"
- Any significant Compose or Android API changes in the last 90 days?
- Best libraries for: notification management, usage stats access, background services?
- Any new Android restrictions affecting app blocking functionality?

### 5. Thai Android Market
Search: "Thailand Android app market 2026", "Thai app Store ranking productivity", "Android users Thailand demographics"
- What types of apps do Thai Android users download most?
- Is there a gap for Thai-language productivity tools?
- Thai app stores or alternative distribution beyond Play Store?

## Sources to Check
- https://play.google.com/store/search?q=focus+app&c=apps (Play Store search)
- Reddit r/androiddev, r/productivity
- AppFollow or AppMagic free tier (app analytics)
- YouTube: "AdMob revenue 2026", "Jetpack Compose tutorial 2026"
- Pantip.com — search Thai app reviews

## Decision Triggers — Flag if Found
- Top competitor with >3-star average but major complaint about missing feature → build that feature
- AdMob eCPM drops significantly → reconsider pure ads model, add IAP
- Android API change restricting app usage stats access → core feature at risk, escalate
- Thai productivity gap confirmed → localize UI to Thai for better Play Store ranking in TH

## After Research — Update This File

After saving findings, edit this file (`android-app/research/AGENT.md`) and update `## Known Facts`:
- Add any new facts discovered (with date and source URL)
- Update facts that have changed (update the date)
- Mark ❓ any fact you couldn't verify this run
- Remove facts that are confirmed stale

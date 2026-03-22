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
<!-- No data yet -->

### AdMob Revenue Benchmarks
<!-- No data yet -->

### Competitor App Analysis
<!-- No data yet -->

### Kotlin / Jetpack Compose Updates
<!-- No data yet -->

### Thai Android Market
<!-- No data yet -->

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

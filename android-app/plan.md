# Android App — Implementation Plan

> **QuickBlock** — A minimalist daily time block planner for Android.
> Differentiator: Crash-free, fast startup (<2s), reliable notifications, streak gamification, Thai language support.
> Revenue: AdMob (free tier) + Premium IAP ($2.99/month — remove ads, themes, widget).

---

## Phase 0: Deep Market Research & Target Customer (DO FIRST)

**Goal:** Validate QuickBlock positioning with real Play Store data and build laser-focused user profiles.

### Market Sizing & Validation
- [ ] Pull exact install counts for all time-blocking apps on Play Store:
  - TimeBloc, blocos, TimeFinder, TimeTune, TimeBlocks — exact installs, rating, review count
  - Structured (iOS-first) — check Android version installs separately
- [ ] Analyze Play Store search volume for target keywords:
  - "time blocking app", "daily planner", "time block planner", "time management"
  - Use AppTweak, Sensor Tower, or data.ai free tier for keyword volume estimates
- [ ] Research total addressable market for Android productivity apps in Thailand:
  - How many Thai Android users use productivity apps? (% of 67.67% Android market share)
  - What's the avg revenue per user for productivity apps in Thailand?
- [ ] Calculate realistic AdMob revenue projections:
  - At 100 DAU, 500 DAU, 1000 DAU, 5000 DAU — what's monthly revenue?
  - Factor in Thailand eCPM (lower than US) vs global user mix
- [ ] Research premium IAP conversion rates for similar apps:
  - What % of free users upgrade? (industry avg 2-5% — verify for productivity)
  - What price point maximizes revenue? ($1.99/mo? $2.99/mo? $4.99/mo? one-time $9.99?)
- [ ] Check Google Play Developer Console trends for "productivity" category in Thailand

### Laser-Targeted Customer Persona
- [ ] **Primary persona: "Busy Bangkok Ben"** — Thai professional, 25-35:
  - Job: developer, designer, marketer, or student at Thai company or remote worker
  - Current tools: Google Calendar, LINE reminders, paper planner, or nothing
  - Phone: mid-range Android (Samsung Galaxy A series, Xiaomi, Oppo)
  - Language: Thai primary, English secondary
  - Pain points: day feels chaotic, can't track where time went, no structure
  - What would make them download: Thai language, free, simple, "just works"
  - What would make them pay premium: widgets, extra themes, no ads
  - Discovery: Play Store search, friend recommendation, Thai tech YouTube/TikTok
- [ ] **Secondary persona: "Productivity Priya"** — global English-speaking user:
  - Job: remote worker, freelancer, indie hacker
  - Currently uses: Structured (iOS), Notion, Todoist — looking for Android alternative
  - Pain points: existing time-block apps crash, paywall recurring blocks, slow
  - Higher price tolerance than Thai users
  - Discovery: Play Store search, r/productivity, YouTube reviews
- [ ] **Anti-persona: "Power Planner Pete"** — wants Google Calendar sync, team features, Notion integration:
  - Too complex for QuickBlock's scope — don't build for this persona
  - They want Structured or Sunsama, not a minimalist blocker
- [ ] Read 50+ reviews of TimeBloc, blocos, TimeBlocks on Play Store:
  - Extract exact pain points (use original language/quotes)
  - Note what features they praise vs complain about
  - Identify the #1 thing that would make them switch

### Competitor Deep-Dive
- [ ] Install and test every competing app for 1 week each:
  - TimeBloc: time to first block, crash frequency, notification reliability
  - blocos: same analysis
  - TimeBlocks: same analysis
  - Structured (if Android version exists): same analysis
- [ ] Document startup time for each app (target: QuickBlock < 2 seconds)
- [ ] Test notification reliability on Samsung and Xiaomi (common Thai phones, aggressive battery optimization)
- [ ] Check which competitors have widgets — quality, update frequency
- [ ] Analyze competitor ASO: titles, descriptions, screenshots, keywords
- [ ] Research Sectograph (6.9M downloads, 4.64 stars): why is it successful? What can QuickBlock learn?

### Customer Discovery Channels
- [ ] Monitor r/productivity and r/androidapps for "time blocking" posts — note what people want
- [ ] Search Thai tech Facebook groups for "แอปจัดตารางเวลา" (time management app) discussions
- [ ] Check Thai tech YouTube channels for productivity app reviews — note view counts
- [ ] Browse Play Store reviews in Thai language for competitor apps
- [ ] Research LINE Official Accounts for productivity tips — potential distribution channel in Thailand
- [ ] Survey 10 Bangkok-based professionals: "How do you plan your day?" (informal, via LINE or in-person)

### Research Deliverables
- [ ] Play Store competitive landscape spreadsheet: app × installs × rating × reviews × price × last update
- [ ] 2 customer persona cards with buying triggers, price sensitivity, discovery channels
- [ ] Revenue projection model: DAU scenarios × ad revenue + IAP conversion
- [ ] Top 20 user pain points extracted from competitor reviews (exact quotes)
- [ ] ASO keyword list: primary and long-tail keywords in English and Thai

---

## Tech Stack

| Layer | Tool |
|---|---|
| Language | Kotlin |
| UI | Jetpack Compose |
| Navigation | Compose Navigation |
| Local Storage | Room DB |
| Monetization | AdMob (GMA SDK v19.0.0+ with UMP SDK) |
| Min SDK | 26 (Android 8.0) |
| Target SDK | 36 (Android 16) |
| Architecture | MVVM + Repository pattern |
| DI | Hilt |

---

## Phase 1: Concept & Validation ← COMPLETE

- [x] Research Play Store utility app gaps
- [x] Select concept: QuickBlock (time block planner)
- [x] Analyze competitive landscape (TimeBloc, Structured, Planner Pro)
- [x] Create wireframes for 5 screens
- [x] Define tech stack and architecture

### Research Findings
- Time-blocking niche has <200K total installs — market is unclaimed
- Top 6 complaints across competitors: crashes/data loss, paywalled recurring tasks, broken notifications, no sync, no analytics, confusing UX
- QuickBlock wins by: reliability + free recurring blocks + Thai language = uncontested

---

## Phase 2: Project Scaffold & Core Architecture

**Goal:** Android project initialized with navigation, database, and theme ready.

### Tasks
- [ ] Initialize Android project (Kotlin + Compose) targeting API 36
- [ ] Set up Gradle with dependencies (Compose, Room, Hilt, Navigation)
- [ ] Configure Material 3 / Material You theme (auto-adapts to wallpaper)
- [ ] Set up Compose Navigation with 5 screens (Today, Editor, Weekly, Stats, Settings)
- [ ] Create Room database with entities:
  - `TimeBlock(id, dayPlanId, taskName, startTime, endTime, color, notes, isCompleted, isRecurring)`
  - `DayPlan(id, date, templateName?)`
  - `Streak(id, currentStreak, longestStreak, lastCompletionDate, freezesUsed)`
- [ ] Create Repository layer (TimeBlockRepository, StatsRepository)
- [ ] Create ViewModels (TodayViewModel, EditorViewModel, WeeklyViewModel, StatsViewModel)
- [ ] Set up Hilt dependency injection
- [ ] Ensure all layouts are orientation-agnostic (Android 16 enforces this)
- [ ] Write unit tests for Room DAOs

### Deliverable
App builds and navigates between 5 empty screens. DB initialized.

---

## Phase 3: Core Features — Today Screen & Block Editor

**Goal:** Users can create, view, edit, and complete time blocks for the current day.

### Tasks
- [ ] **Today screen:**
  - [ ] Display time blocks for current day in vertical timeline (06:00-23:00)
  - [ ] Color-coded blocks by category
  - [ ] Tap block to mark complete (checkbox toggle with animation)
  - [ ] Pre-filled template day on first launch (zero onboarding)
  - [ ] Floating action button to add new block
  - [ ] Swipe to delete block
- [ ] **Block Editor screen:**
  - [ ] Task name input
  - [ ] Start/end time pickers
  - [ ] Color picker (6 preset colors)
  - [ ] Notes field (optional)
  - [ ] Recurring toggle (daily/weekday/custom)
  - [ ] Save/Delete buttons
- [ ] Drag-to-reorder blocks on Today screen
- [ ] Persistent storage via Room (instant save on every change)
- [ ] Handle edge cases: overlapping blocks, midnight crossing

### Deliverable
Functional time blocking on Today screen. Blocks persist across app restarts.

---

## Phase 4: Gamification — Streaks & Stats

**Goal:** Add streak tracking and basic stats to drive daily retention.

### Tasks
- [ ] **Streak system:**
  - [ ] Daily "blocks completed" counter on Today screen
  - [ ] Streak counter: consecutive days with >=1 completed block
  - [ ] Streak visual (flame icon + count) in top bar
  - [ ] Streak Freeze: watch rewarded ad to protect a breaking streak
  - [ ] Streak milestone celebrations (7-day, 30-day, 100-day)
  - [ ] Push notification when streak is at risk (evening, configurable time)
- [ ] **Stats screen:**
  - [ ] Completion rate (% of blocks completed this week/month)
  - [ ] Current streak and longest streak
  - [ ] Most productive hours (heatmap or bar chart)
  - [ ] Weekly completion trend chart
- [ ] **Weekly View screen:**
  - [ ] 7-day calendar grid showing blocks per day
  - [ ] Color-coded by completion status (green = complete, gray = missed)
  - [ ] Tap a day to navigate to that day's blocks

### Deliverable
Streaks tracking. Stats screen with charts. Weekly overview functional.

---

## Phase 5: Notifications, Templates & Settings

**Goal:** Reliable notifications (top competitor complaint), template days, and polish.

### Tasks
- [ ] **Notifications:**
  - [ ] Per-block reminders (5 min before start — configurable)
  - [ ] Streak-at-risk evening notification
  - [ ] Use AlarmManager for exact timing (not WorkManager — more reliable)
  - [ ] Test notification reliability across Samsung, Xiaomi, Pixel (OEM battery optimization issues)
- [ ] **Template days:**
  - [ ] Save any day's layout as a named template
  - [ ] Apply template to future days
  - [ ] Pre-built templates: "Work Day", "Weekend", "Focus Day"
- [ ] **Settings screen:**
  - [ ] Dark mode toggle (follows system by default)
  - [ ] Notification preferences
  - [ ] Default block duration (30/45/60 min)
  - [ ] First day of week (Mon/Sun)
  - [ ] Data backup/restore (export/import JSON)
  - [ ] Thai/English language toggle
- [ ] Add Thai language strings (values-th/strings.xml)
- [ ] Add Thai-language Play Store metadata and keywords

### Deliverable
Reliable notifications. Template system. Thai language support. Settings complete.

---

## Phase 6: Monetization & Play Store Launch

**Goal:** AdMob integrated, Premium IAP live, published on Play Store.

### Tasks
- [ ] **AdMob integration:**
  - [ ] **CRITICAL: Use GMA SDK v19.0.0+ with UMP SDK** (TCF v2.3 mandatory since March 2026)
  - [ ] Banner ad on Today screen (bottom)
  - [ ] Interstitial ad on day completion (max 1/day)
  - [ ] Rewarded ad for Streak Freeze
  - [ ] Test ads with test device IDs before production
- [ ] **Premium IAP ($2.99/month or $24.99/year):**
  - [ ] Remove all ads
  - [ ] Extra themes (6+ color schemes)
  - [ ] Home screen widget (today's blocks at a glance)
  - [ ] Unlimited templates (free tier: 3 templates)
  - [ ] Google Play Billing Library v7+
- [ ] **Home screen widget:**
  - [ ] Today's blocks list (Glance Compose)
  - [ ] Tap block to open app to that block
- [ ] **Play Store listing:**
  - [ ] Screenshots for all 5 screens (phone + tablet)
  - [ ] Feature graphic (1024x500)
  - [ ] Short description (80 chars) + full description
  - [ ] Keywords: time blocking, daily planner, time management, productivity
  - [ ] Privacy policy page
  - [ ] Content rating questionnaire
- [ ] **Pre-launch:**
  - [ ] Internal testing track (10 testers)
  - [ ] Open testing for 7 days
  - [ ] Fix crash reports from testing
- [ ] **Launch** to production

### Deliverable
App live on Google Play Store. AdMob serving ads. Premium IAP purchasable.

---

## Phase 7: Post-Launch Optimization

**Goal:** Improve ratings, fix issues, add requested features.

### Tasks
- [ ] Monitor crash reports (Firebase Crashlytics)
- [ ] Respond to user reviews within 24h
- [ ] Track DAU/MAU, retention rates, ad revenue
- [ ] A/B test streak notification timing
- [ ] Add requested features from reviews (common: export to Google Calendar)
- [ ] API 36 migration if launched on API 35 (deadline: August 31, 2026)
- [ ] Consider Health Connect integration: log focus sessions as `ACTIVITY_INTENSITY`
- [ ] Optimize for foldable/tablet layouts
- [ ] Target: 4.5+ star rating, 1000+ installs in first 3 months

### Deliverable
Stable app with 4.5+ rating. Consistent daily active users.

---

## Key Research Insights Driving This Plan

- **Niche is unclaimed**: <200K total installs across all time-blocking apps
- **Every competitor has critical failures**: Crashes, data loss, broken notifications
- **Streaks are #1 retention mechanic**: 7-day streaks produce 3.6x higher long-term retention
- **Streak Freeze via rewarded ad**: Reduced churn 21% for at-risk users
- **TCF v2.3 mandatory**: GMA SDK v19.0.0+ with UMP SDK required or 60-80% CPM loss
- **Android 16 enforces adaptive layouts**: Must support portrait + landscape from Day 1
- **Thai market**: 67.67% Android market share, no Thai-language time-blocking app exists
- **Ling app proof**: Thai localization + gamification = 4.6 stars / 18.1K reviews
- **Play Store deadline**: API 36 target required by August 31, 2026

---

## Wireframes

### Screen 1: Today (Main)
```
+----------------------+
|  QuickBlock   Today  |
|  [fire] 12-day streak|
+----------------------+
| 06:00 ░░░░░░░░░░░░░ |
| 07:00 [x] Morning Run| <- completed
| 08:00 [ ] Deep Work  | <- active
| 09:00 [ ] Deep Work  |
| 10:00 ░░░░░░░░░░░░░ |
| 11:00 [ ] Meetings   |
| 12:00 [ ] Lunch      |
+----------------------+
| [+] Add Block        |
+----------------------+
| Today  Week  Stats  S|
+----------------------+
```

### Screen 2: Block Editor
```
+----------------------+
| < Edit Block         |
+----------------------+
| Task: [Deep Work    ]|
| Start: [08:00      ]|
| End:   [10:00      ]|
| Color: R B G Y W P  |
| Notes: [           ]|
| Recurring: [Daily v]|
|                      |
| [Delete]    [Save]   |
+----------------------+
```

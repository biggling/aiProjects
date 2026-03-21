# Android App — Implementation Plan

## App: QuickBlock — Daily Time Block Planner

## Phase 1: Concept & Validation ← COMPLETE
- [x] Research Play Store gaps in utility apps
- [x] Select concept: QuickBlock (time block planner)
- [x] Define MVP screens and user flow
- [x] Create wireframes

## Phase 2: Project Scaffold
- [ ] Initialize Android project (Kotlin + Compose)
- [ ] Set up Compose Navigation (5 screens)
- [ ] Configure Room database
- [ ] Create data models (TimeBlock, DayPlan)
- [ ] Set up theme and color scheme

## Phase 3: Core Features
- [ ] Today screen — display time blocks for current day
- [ ] Block editor — add/edit time blocks
- [ ] Drag to reorder blocks
- [ ] Block completion toggle (tap to mark done)
- [ ] Persistent storage via Room

## Phase 4: Extended Features
- [ ] Weekly view calendar
- [ ] Stats screen (completion rate, streaks)
- [ ] Notifications/reminders per block
- [ ] Template days (copy a day's layout)
- [ ] Dark mode

## Phase 5: Monetization & Launch
- [ ] AdMob integration (banner on Today, interstitial on day complete)
- [ ] Premium IAP: remove ads, extra themes, widget
- [ ] Home screen widget (today's blocks)
- [ ] Play Store listing (screenshots, description, keywords)
- [ ] Launch

## Research: Why QuickBlock

### Market Gap
- Top time block apps have 100K+ downloads but poor reviews (3.5-4.0 stars)
- Common complaints: too complex, slow startup, too many features
- Opportunity: fast, minimal, "just works" time blocker

### Competitive Landscape
| App | Downloads | Rating | Issue |
|-----|-----------|--------|-------|
| TimeBloc | 100K+ | 3.8 | Complex, slow |
| Structured | 500K+ | 4.2 | iOS-first, Android buggy |
| Planner Pro | 1M+ | 3.6 | Bloated, crashes |

### Differentiation
- Launch to usable in < 2 seconds
- Zero onboarding — pre-filled template day
- Material You design (auto-adapts to wallpaper colors)
- Offline-first (no account required)

## Wireframes

### Screen 1: Today (Main)
```
┌──────────────────────┐
│  QuickBlock   Today  │
├──────────────────────┤
│ 06:00 ░░░░░░░░░░░░░ │
│ 07:00 ▓ Morning Run  │ ← colored block
│ 08:00 ▓ Deep Work    │
│ 09:00 ▓ Deep Work    │
│ 10:00 ░░░░░░░░░░░░░ │
│ 11:00 ▓ Meetings     │
│ 12:00 ▓ Lunch        │
│ ...                  │
├──────────────────────┤
│ [+] Add Block        │
├──────────────────────┤
│ Today  Week  Stats ⚙ │
└──────────────────────┘
```

### Screen 2: Block Editor
```
┌──────────────────────┐
│ ← Edit Block         │
├──────────────────────┤
│ Task: [Deep Work    ]│
│ Start: [08:00      ]│
│ End:   [10:00      ]│
│ Color: 🔴🔵🟢🟡⚪   │
│ Notes: [           ]│
│                      │
│ [Delete]    [Save]   │
└──────────────────────┘
```

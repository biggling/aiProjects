# CLAUDE.md

## Project Purpose
Android utility app for Google Play Store — "QuickBlock" daily time block planner. Simple, ad-supported, daily use app.

## Commands
```bash
# Build debug APK
./gradlew assembleDebug

# Run tests
./gradlew test

# Install on connected device
./gradlew installDebug
```

## Architecture

### Tech Stack
- **Language:** Kotlin
- **UI:** Jetpack Compose
- **Navigation:** Compose Navigation
- **Local storage:** Room DB
- **Monetization:** AdMob (banner + interstitial)
- **Min SDK:** 26 (Android 8.0)
- **Target SDK:** 35

### App Concept: QuickBlock
A minimalist daily time block planner. Users divide their day into blocks (30-60 min each), assign tasks, and track completion. Clean UI, no bloat, starts fast.

### Screens
1. **Today** — Main view with time blocks for the current day
2. **Block Editor** — Add/edit a time block (time, task, color, notes)
3. **Weekly View** — Calendar overview of the week
4. **Stats** — Completion rate, streaks, most productive hours
5. **Settings** — Theme, notifications, backup, premium

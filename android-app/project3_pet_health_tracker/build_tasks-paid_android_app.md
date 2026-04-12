# Build Tasks — Pet Health Tracker (Paid Android App)

> **Prompt for Agent**: Generate a detailed, sequenced task list in `continue.md`.
> Each task must be completable by a Claude Code agent in **under 10 minutes**.
> Goal: Build a production-ready **Pet Health Tracker + Medication Reminder** paid Android app.

---

## Context for Agent

### Who is BiG (the developer)
- Solo developer based in Bangkok, Thailand (GMT+7)
- Full-time job; ~5 hours/week for side projects
- Experience: Go, Java, Python, Node.js, iOS, microservices, K8s
- Hardware: Mac Mini, VPS, Claude Pro subscription
- Has Google Play developer account ($25 one-time fee paid)
- Goal: multiple passive/semi-passive income streams via paid Android apps

### App Concept — Already Decided
**Pet Health Tracker + Medication Reminder** — Score: **26/30**

| Dimension       | Score | Why                                                        |
|-----------------|-------|------------------------------------------------------------|
| Market Size     | 5     | 67% of US households own a pet; $136B US pet industry      |
| Competition     | 4     | No strong one-time paid option (ZooMinder, Notepet, PetDesk all free/subscription) |
| Build Effort    | 4     | Local DB + notifications + PDF export = 4–6 weeks          |
| Revenue Ceiling | 4     | $3.99 × 0.4% of 1M pet owners = $2,000–$5,000/mo          |
| US Cultural Fit | 5     | "Fur baby" culture; vet records critical for boarding      |
| Differentiation | 4     | "Buy once, own your pet's health records forever"          |

### Revenue Model
- **$3.99 one-time purchase** (main app — 1 pet included)
- **$0.99 IAP** per additional pet unlock (free = 1 pet, paid = unlimited)
- No subscription. No ads. No cloud. No account required.

### Core Value Proposition
> "Your pet's complete health record — vaccinations, medications, vet visits, weight — all in one app. No vet portal login. No subscription. Buy once, own forever."

### Key Research Data (from `research.md`)
- US pet owners face **fragmented vet records across 3–5 practices** over a pet's lifetime
- PetDesk is free but **owned by veterinary chains** — users distrust it with full health picture
- Pet insurance claims require **precise medication/visit logs**
- US-specific features: vet visit cost tracker (HSA expense tag), flea/tick seasonal reminders, USDA rabies certificate reminder
- **Privacy angle**: "Your pet's medical data stays on YOUR phone — not in a vet chain's database"

### Project State
- Working directory: `project3_pet_health_tracker/`
- **No code written yet** — only `research.md` exists
- All output files go in THIS directory
- Tech stack: **Kotlin + Jetpack Compose + Room DB + Hilt + Material 3**
- Target SDK: **36 (Android 16)** — edge-to-edge mandatory, adaptive layouts required
- Min SDK: **26 (Android 8.0)**

### File References
| File | Purpose |
|------|---------|
| `research.md` | Market research, competitor analysis, feature scope — **READ FIRST** |
| `continue.md` | Session state + task list — **CREATE/UPDATE with generated tasks** |
| `Requirements.md` | Full requirements doc — **CREATE in Phase 1** |
| `CLAUDE.md` | Project-level instructions — **CREATE for this sub-project** |
| `TEST_PLAN.md` | Test case inventory — **CREATE in Phase 3** |
| `ASSETS.md` | Asset inventory — **CREATE in Phase 2** |

---

## Phase 1: Build Requirements.md

**Goal**: Create a comprehensive `Requirements.md` — the single source of truth for what we're building. Detailed enough that any developer can build the app from it alone.

### Task 1.1 — Research User-Needed Features
**Output**: Section in `Requirements.md` — Feature List (Required / Must-Have / Nice-to-Have)

**Instructions for agent**:
1. Read `research.md` thoroughly
2. Web search for "pet health tracker app" user complaints and feature requests (Reddit r/pets, r/dogs, r/cats, Play Store reviews of PetDesk, ZooMinder, Notepet, Pet First Aid)
3. Categorize features into three tiers:

   **Required (MVP — must ship or no one downloads)**:
   - Multi-pet profiles (name, species, breed, DOB, photo, weight, microchip #)
   - Vaccination log with due-date reminders
   - Medication schedule with daily/weekly reminders (notifications)
   - Vet visit log (date, vet name, reason, notes, cost)
   - Weight tracking with trend chart
   - Emergency vet contacts list

   **Must-Have (v1.0 — within 1 week of launch, or 1-star reviews)**:
   - PDF health summary export (for boarding, new vet, insurance claims)
   - Photo attachment per record (vaccine certificate photo, lab results)
   - Flea/tick/heartworm prevention schedule with seasonal reminders
   - Data backup/restore (local JSON export/import)
   - USDA rabies certificate reminder

   **Nice-to-Have (v1.1+ — post-launch based on feedback)**:
   - Home screen widget (next medication due)
   - Vet visit cost tracker with annual summary (HSA expense tag)
   - Feeding schedule & food brand log
   - Allergy/dietary restriction notes
   - Pet insurance policy reference (policy #, phone, claim URL)
   - Growth chart (puppies/kittens — expected vs actual weight)
   - Share pet profile with family member (local export, not cloud sync)

4. For each feature, note:
   - Why users need it (cite competitor reviews or Reddit posts)
   - Which competitor does it well / does it poorly
   - Estimated build effort (hours)

### Task 1.2 — Research Competitor Features Deep-Dive
**Output**: Section in `Requirements.md` — Competitor Analysis Matrix

**Instructions for agent**:
1. Web search for the top 5 direct competitors:
   - **PetDesk** — vet-chain-owned, free, cloud-based
   - **ZooMinder** — free + $2/mo subscription
   - **Notepet** — free, basic
   - **Pet First Aid (Red Cross)** — $0.99, emergency focused
   - **11Pets** — free, feature-rich but ad-heavy
2. For each competitor, document:
   - Play Store rating, install count, last update date
   - Monetization model
   - Core features list
   - Top 3 user complaints (from Play Store reviews)
   - Top 3 user praises
   - What they do better than us
   - What we can do better (our angle)
3. Create a **Feature Comparison Matrix** (table):
   - Rows = features, Columns = competitors + our app
   - Mark: has / missing / paid-only / broken
4. Identify the **#1 thing** that would make users switch to our app
5. Note table-stakes features (ALL competitors have → we MUST match)

### Task 1.3 — Research UX/UI Best Practices & Competitor Weaknesses
**Output**: Section in `Requirements.md` — UX/UI Strategy

**Instructions for agent**:
1. Web search for Material 3 design guidelines for pet/health/tracker app categories
2. Research competitor UX complaints (Play Store reviews, Reddit, app review blogs)
3. Define our **UX principles** (specific to pet health tracking):
   - Zero-config first launch: "Add Your First Pet" wizard (name + species + photo = done in 30 seconds)
   - Core action in 2 taps: open app → tap "Log Medication" → done
   - Sub-2-second cold start
   - Pet-switcher always visible (top bar avatar row for multi-pet households)
   - Warm, friendly tone — not clinical (this is a "fur baby" app, not a hospital portal)
   - High contrast, accessible text (pet owners skew older demographic too)
   - Thumb-friendly bottom navigation
4. Research and recommend:
   - **Color palette**: warm, trustworthy tones (teal/green for health + warm accent for pets). Material 3 dynamic color + fallback palette
   - **Typography**: Material 3 type system, readable at small sizes for medication names
   - **Icon style**: Material Symbols outlined, pet-themed custom icons where needed (paw, syringe, stethoscope)
   - **Animation**: Compose shared element transitions, subtle micro-interactions (checkmark on medication taken)
   - **Dark mode**: follows system default, user toggle in settings
5. List UI patterns:
   - Bottom sheet for quick-log actions (medication taken, weight entry)
   - Swipe to mark medication as taken
   - Empty states with friendly illustration ("Add your first pet to get started!")
   - Cards for pet profiles (photo, name, next-due medication)
   - Timeline/history view for vet visits
6. Note competitor UI mistakes to avoid (cite specific apps)

### Task 1.4 — Detail App Structure, Usage Flows & Features
**Output**: Section in `Requirements.md` — App Structure & User Flows

**Instructions for agent**:
1. Define the **screen list**:

   **Bottom Nav Tabs (4)**:
   - **Dashboard** — Overview of all pets, upcoming medications/appointments, alerts
   - **Health Log** — Timeline of all health events (meds, vet visits, vaccines, weight)
   - **Reminders** — All active medication/vaccine/prevention schedules
   - **Settings** — Theme, notifications, backup, purchase, about

   **Pushed Screens (not tabs)**:
   - **Pet Profile** — Single pet detail (photo, info, records)
   - **Add/Edit Pet** — Pet creation/edit form
   - **Add Vaccination** — Log a vaccine (name, date, next due, vet, photo)
   - **Add Medication** — Schedule a medication (name, dosage, frequency, start/end, reminders)
   - **Add Vet Visit** — Log a visit (date, vet, reason, diagnosis, notes, cost, photos)
   - **Log Weight** — Quick weight entry with chart view
   - **Emergency Contacts** — Vet phone numbers, poison control, nearest emergency vet
   - **PDF Export** — Preview and share pet health summary
   - **Multi-Pet Unlock** — IAP purchase screen (shown when adding 2nd pet on free tier)

2. Create **user flow diagrams** (text-based):
   - **First-time flow**: Install → "Add Your First Pet" wizard → Dashboard with sample reminder → first value moment
   - **Daily flow**: Open app → see "Buddy needs heartworm pill" → tap → mark as given → done (3 taps)
   - **Vet visit flow**: Open app → go to Health Log → tap "+" → select "Vet Visit" → fill form → attach photo of receipt → save
   - **Export flow**: Pet Profile → tap "Export PDF" → preview → share via email/message/AirDrop
   - **Purchase flow**: Add 2nd pet → "Unlock unlimited pets for $0.99" → Google Play purchase → pet added
   - **Boarding prep flow**: Pet Profile → Export PDF → send to boarding facility

3. For each screen, specify:
   - UI elements (every button, input, display)
   - Data displayed (which Room entities)
   - User actions (tap, swipe, long-press)
   - Navigation targets

4. Define **data model** (Room entities):
   ```
   Pet(id, name, species, breed, dob, photoUri, microchipId, weight, notes, createdAt, updatedAt)
   Vaccination(id, petId, name, dateGiven, nextDueDate, vetName, batchNumber, photoUri, notes)
   Medication(id, petId, name, dosage, frequency, startDate, endDate, reminderTime, isActive, notes)
   MedicationLog(id, medicationId, petId, takenAt, skipped, notes)
   VetVisit(id, petId, date, vetName, vetClinic, reason, diagnosis, treatment, cost, photoUris, notes)
   WeightEntry(id, petId, weight, unit, date, notes)
   EmergencyContact(id, name, phone, type, address, notes, isPrimary)
   ```
   - Relationships: Pet 1:N Vaccination, Medication, VetVisit, WeightEntry
   - Medication 1:N MedicationLog
   - Indexes: petId on all child tables, date columns for sorting

5. Define **state management**:
   - Room DB → Repository (coroutines + Flow) → ViewModel (StateFlow) → Compose UI
   - Each screen gets its own ViewModel
   - Shared state: selected pet ID lives in a shared ViewModel or SavedStateHandle

### Task 1.5 — Detail Look & Feel / Visual Design Spec
**Output**: Section in `Requirements.md` — Visual Design Specification

**Instructions for agent**:
1. Define **brand identity**:
   - **App name**: "PawTrack" (or research alternatives: PetVault, FurLog, PawHealth)
   - **Tagline**: "Your pet's health, in your hands"
   - **Personality**: Warm, trustworthy, simple — like a friendly vet receptionist
   - **App icon concept**: Paw print with a heart/plus symbol, teal/green background
   - **Primary color**: Teal (#009688) — health, trust, calm
   - **Secondary color**: Warm amber (#FFB300) — friendly, pet-associated
   - **Error color**: Soft red — for overdue medications/vaccines

2. Create **screen-by-screen wireframes** (ASCII/text-based):
   - Dashboard (populated + empty state)
   - Pet Profile
   - Add/Edit Pet form
   - Health Log timeline
   - Add Medication form
   - Reminders list
   - Settings
   - PDF Export preview
   - Show both light and dark mode for Dashboard

3. Define **component specs**:
   - Pet card: rounded corners (16dp), elevation 2dp, photo + name + species + next-due badge
   - Medication card: name, dosage, time, "Take" button (prominent), "Skip" secondary
   - Vet visit card: date, vet name, reason summary, cost (if logged), photo thumbnail
   - Weight chart: line chart with date axis, weight axis, tap point for details
   - Timeline: vertical line with event nodes (color-coded by type)

4. Define **animation specs**:
   - Screen transitions: shared element for pet photo (Dashboard → Pet Profile)
   - Medication taken: checkmark with haptic feedback + brief green highlight
   - Streak: consecutive days of medication adherence → small celebration
   - Loading: skeleton shimmer on Dashboard

5. Define **typography & spacing**:
   - Material 3 type scale
   - Pet names: Title Large
   - Medication names: Body Large (must be readable — medication errors are dangerous)
   - Grid: 8dp base unit
   - Content padding: 16dp horizontal, 8dp between cards

### Task 1.6 — Detail Error Handling, Analytics, Edge Cases & Non-Functional Requirements
**Output**: Section in `Requirements.md` — Technical Requirements

**Instructions for agent**:
1. **Error handling** (pet health context — errors matter more here):
   - **Medication reminder failure**: CRITICAL — use AlarmManager (exact alarms) not WorkManager. Test on Samsung/Xiaomi (aggressive battery optimization kills reminders). Fallback: persistent notification channel.
   - **Database corruption**: Room migration strategy. Auto-backup to local JSON weekly.
   - **Permission denials**: Notification permission (Android 13+), exact alarm (Android 12+), camera (photo attachment). Handle each gracefully with explanation.
   - **Photo storage**: Handle large photos (compress to 1024px max dimension). Handle deleted photos gracefully (show placeholder).
   - **Invalid input**: Pet weight can't be negative or >500kg. Medication dosage must be positive. Date validation (no future vet visits).
   - For each error: specify message text, recovery action, UI behavior

2. **Analytics** (privacy-respecting — align with "your data stays on your phone" pitch):
   - **Recommended**: Firebase Analytics (free tier) — anonymized only
   - Track: screen views, feature usage (which features used most), crash-free rate, retention
   - Do NOT track: pet names, medication names, vet names, photos, any PII
   - Key metrics post-launch:
     - DAU/MAU ratio (target: 20%+ — daily medication reminders drive this)
     - Day 1 / Day 7 / Day 30 retention
     - Crash-free rate (target: 99.5%+)
     - PDF export usage (validates core value prop)
     - Multi-pet IAP conversion rate

3. **Edge cases specific to pet health**:
   - **Timezone travel**: Pet owner travels — medication reminders must adjust or warn
   - **Pet death**: Sensitive — allow archiving a pet profile (don't say "delete")
   - **Multiple medications at same time**: Group notifications, don't spam
   - **Medication schedule changes**: Mid-course dosage change — log the change in history
   - **Very old pets**: 20+ years of records — Room query performance at scale
   - **Multi-pet households**: 5+ pets — UI must not become unusable
   - **Shared custody**: Divorced owners — export covers this (no cloud sync needed)

4. **Performance requirements**:
   - Cold start: < 2 seconds
   - Screen transitions: < 300ms
   - Database queries: < 100ms (index petId, date columns)
   - App size: < 20 MB APK (photos stored externally in app-specific storage)
   - Memory: < 100 MB runtime
   - Battery: medication reminders must fire reliably WITHOUT draining battery

5. **Security**:
   - ProGuard/R8 obfuscation
   - No hardcoded keys
   - Google Play Billing Library v7+ (for $0.99 multi-pet IAP)
   - Play Integrity API for license verification
   - Photos stored in app-specific internal storage (not public gallery)

6. **Testing requirements**:
   - Unit test coverage: 80%+ for business logic (medication scheduling logic is critical)
   - UI tests: all critical flows (add pet, log medication, export PDF)
   - Devices: Pixel 7 (stock), Samsung Galaxy A54, Xiaomi Redmi Note
   - Android versions: API 26, API 33, API 36
   - **Critical test**: medication reminders fire correctly on Samsung/Xiaomi after device reboot

7. **Localization**:
   - English only for v1.0 (US market first — $136B pet industry)
   - String externalization from Day 1 (prepare for Thai in v1.1)
   - Date/time format: respect locale
   - Weight units: lb (US default) + kg toggle in settings
   - Currency: USD for vet cost tracking

8. **Play Store requirements**:
   - Target API 36 (mandatory by August 31, 2026)
   - Edge-to-edge display (Android 16)
   - Adaptive layouts (tablets/foldables)
   - Data safety: "No data collected" or "Data stored locally only"
   - Privacy policy URL (required for paid apps)
   - Content rating: Everyone
   - App category: Medical (or Health & Fitness)

---

## Phase 2: Build the Android App

**Goal**: Build the app screen-by-screen, feature-by-feature. Each task is self-contained, compiles independently, and takes < 10 minutes.

### Task 2.1 — Generate Sub-Task List (Screen, Flow, Feature Breakdown)
**Output**: Detailed sub-task list added to `continue.md`

**Instructions for agent**:
1. Read the completed `Requirements.md`
2. Break the build into **< 10 minute tasks** in this order:

   **a) Project scaffold (2 tasks)**:
   - `BUILD-01`: Initialize Kotlin + Compose project, Gradle deps (Compose, Room, Hilt, Navigation, Material 3)
   - `BUILD-02`: Material 3 theme (teal/amber palette), navigation shell with 4 bottom tabs, empty screen stubs

   **b) Data layer (3 tasks)**:
   - `BUILD-03`: Room entities (Pet, Vaccination, Medication, MedicationLog, VetVisit, WeightEntry, EmergencyContact) + DAOs
   - `BUILD-04`: Database class + Repository classes (PetRepository, HealthRepository, ReminderRepository)
   - `BUILD-05`: ViewModels (DashboardVM, PetProfileVM, HealthLogVM, RemindersVM, SettingsVM) with basic StateFlow

   **c) Screens — one task per screen (9 tasks)**:
   - `BUILD-06`: Dashboard screen — pet cards, upcoming reminders, alerts
   - `BUILD-07`: Add/Edit Pet screen — form with photo picker, species/breed, DOB
   - `BUILD-08`: Pet Profile screen — pet detail with tabs (vaccines, meds, visits, weight)
   - `BUILD-09`: Add Vaccination screen — form with date picker, next-due, photo attach
   - `BUILD-10`: Add Medication screen — form with dosage, frequency, reminder time picker
   - `BUILD-11`: Add Vet Visit screen — form with cost, photos, diagnosis notes
   - `BUILD-12`: Weight Log screen — quick entry + line chart (Vico or similar charting lib)
   - `BUILD-13`: Health Log screen — timeline view of all events, filtered by type
   - `BUILD-14`: Reminders screen — list of all active schedules, toggle on/off

   **d) Features — one task per feature (6 tasks)**:
   - `BUILD-15`: Medication reminder notifications (AlarmManager, exact alarms, boot receiver)
   - `BUILD-16`: Vaccination due-date reminders + flea/tick seasonal reminders
   - `BUILD-17`: PDF health summary export (pet profile + vaccine history + med list)
   - `BUILD-18`: Emergency contacts screen (add/edit/call)
   - `BUILD-19`: Settings screen (theme, weight unit, notification prefs, backup/restore JSON)
   - `BUILD-20`: Data backup/restore (export all data as JSON, import from JSON)

   **e) Monetization (2 tasks)**:
   - `BUILD-21`: Google Play Billing Library — $3.99 app purchase verification + $0.99 multi-pet IAP
   - `BUILD-22`: Multi-pet unlock gate UI (shown when adding 2nd pet on free tier)

   **f) Polish (3 tasks)**:
   - `BUILD-23`: Empty states, loading skeletons, error states for all screens
   - `BUILD-24`: Animations (shared element pet photo, medication taken checkmark, screen transitions)
   - `BUILD-25`: Edge-to-edge + adaptive layout adjustments + accessibility (content descriptions, 48dp touch targets)

3. For each task, specify: ID, name, input dependencies, output files, acceptance criteria, estimated minutes

### Task 2.2 — List Required Assets
**Output**: `ASSETS.md` in project directory

**Instructions for agent**:
1. List every asset needed:
   - **App icon**: 512x512 (Play Store) + adaptive icon layers. Concept: paw + heart/plus, teal bg
   - **Feature graphic**: 1024x500 for Play Store listing
   - **Screenshots**: 5 screens × phone (1080x1920)
   - **In-app icons** (Material Symbols): pets, vaccines, medication, vet, weight, emergency, settings, export, add, edit, delete, calendar, notification, camera, share
   - **Empty state illustrations**: "Add your first pet" (friendly pet illustration), "No medications yet", "No vet visits"
   - **Splash screen**: paw icon + app name (Android 12+ SplashScreen API)
   - **Pet placeholder**: default avatar for pets without photo (by species: dog, cat, bird, fish, other)
2. For each: dimensions, format, where used, can AI generate it, P0 vs P1
3. Free sources: Material Symbols, Undraw.co, Unsplash (pet photos for mockups)

### Task 2.3 — Build the App (Execute BUILD-01 through BUILD-25)
**Output**: Working Android app, committed incrementally

**Instructions for agent** (apply to every BUILD task):

1. **Before writing code**:
   - Read `Requirements.md` for the relevant section
   - Read existing code this task depends on
   - Verify previous task compiles: `./gradlew assembleDebug`

2. **While writing code**:
   - MVVM + Repository pattern strictly
   - Hilt for all DI
   - Compose for all UI (no XML layouts)
   - Room for all persistence
   - Idiomatic Kotlin (data classes, sealed classes, coroutines, Flow)
   - Android 16: edge-to-edge, adaptive layouts
   - Material 3 theme for all components
   - KDoc only for public APIs and non-obvious logic

3. **After writing code**:
   - `./gradlew assembleDebug` — must pass
   - `./gradlew test` — if tests exist
   - Update `continue.md` — mark task done, note blockers

4. **Code quality**:
   - No hardcoded strings → `strings.xml`
   - No hardcoded colors → Material 3 theme
   - Max 200 lines per file
   - Single responsibility
   - `@Preview` for every composable screen

---

## Phase 3: Automated Testing

**Goal**: Comprehensive test suite that catches regressions — especially for medication reminders (safety-critical).

### Task 3.1 — Prepare Test Cases
**Output**: `TEST_PLAN.md` in project directory

**Instructions for agent**:
1. Read `Requirements.md` and all built code
2. Generate test cases by category:

   **Unit tests** (ViewModels, Repositories, business logic):
   - Every ViewModel public method
   - Every Repository CRUD operation
   - Every Room DAO query
   - Medication scheduling logic (daily/weekly/custom frequency)
   - Weight unit conversion (lb ↔ kg)
   - Date calculations (next vaccine due, medication end date)
   - Edge: empty data, max pets, null photo URI

   **Integration tests** (data layer):
   - Room DB creation + migration
   - Repository + DAO integration
   - ViewModel + Repository with fakes

   **UI tests** (Compose):
   - Every screen renders without crash
   - Add pet flow end-to-end
   - Log medication flow end-to-end
   - Export PDF flow
   - Multi-pet IAP flow (mock billing)
   - Dark mode rendering
   - Accessibility: TalkBack, content descriptions

   **Critical path tests** (medication safety):
   - Medication reminder fires at correct time
   - Reminder survives device reboot
   - Multiple medications at same time → grouped notification
   - Medication marked as taken → next reminder scheduled correctly
   - Medication skipped → logged with skip reason

3. For each test: ID, name, preconditions, steps, expected result, priority (P0/P1/P2)

### Task 3.2 — Build Automated Tests
**Output**: Test code in `app/src/test/` and `app/src/androidTest/`

**Instructions for agent**:
1. Implement in priority order (P0 first):
   - **Unit tests** (`src/test/`): JUnit 5 + Turbine + MockK
   - **UI tests** (`src/androidTest/`): Compose UI Test
   - **Integration tests** (`src/androidTest/`): Room MigrationTestHelper
2. Test quality:
   - Arrange-Act-Assert pattern
   - Descriptive names: `should_scheduleNextReminder_when_medicationMarkedAsTaken`
   - Test fixtures for pet/medication/vet test data
   - No flaky tests (no `Thread.sleep()`)

### Task 3.3 — Run Tests & Report
**Output**: Test report in `continue.md`

**Instructions for agent**:
1. Run:
   ```bash
   ./gradlew test --info
   ./gradlew connectedAndroidTest  # if emulator available
   ```
2. Report: total passed/failed/skipped, coverage %, list all failures with root cause
3. Fix all P0 failures immediately
4. Update `continue.md`:
   - Health: GREEN / YELLOW / RED
   - Coverage stats
   - Known P1/P2 issues
   - Status: "Phase 3: Testing — COMPLETE" or blockers

---

## Task Generation Rules for `continue.md`

When generating the task list in `continue.md`, follow these rules:

1. **Each task completable in < 10 minutes** by a Claude Code agent
2. **Sequential** — each task's output feeds the next
3. **Independently verifiable** — clear acceptance criteria per task
4. **Checkbox format**: `- [ ] TASK-ID: Description (~Xmin)`
5. **Grouped by phase**: Phase 1 (Requirements), Phase 2 (Build), Phase 3 (Test)
6. **Include dependencies** — note which tasks block which
7. **Total: 35-50 tasks**:
   - Phase 1: ~8-10 tasks (requirements + research)
   - Phase 2: ~20-30 tasks (build)
   - Phase 3: ~5-8 tasks (testing)
8. **Update session state** after listing:
   - Current Phase, Last Session date, Next 3 Actions, Blockers

---

## Decision Points for BiG

Flag these in `continue.md` under "Decisions Needed from BiG":

1. **App name**: "PawTrack"? "PetVault"? "FurLog"? (agent to recommend, BiG decides)
2. **Price point**: $3.99 as researched, or adjust? ($2.99 lower friction vs $4.99 higher ARPU)
3. **Free tier scope**: 1 pet free + IAP for more? Or pure paid $3.99 (no free tier)?
4. **Analytics**: Firebase Analytics (Google sees anonymized data) vs no analytics (stronger privacy pitch)?
5. **Weight units default**: lb (US-first) or kg (global)?
6. **Pet species supported**: Dogs + Cats only for v1? Or all species from Day 1?

---

## Success Criteria

The task list is complete when:
- [ ] `Requirements.md` exists with all 6 sub-sections (1.1 – 1.6)
- [ ] `continue.md` has 35-50 checkboxed tasks with IDs, time estimates, dependencies
- [ ] `CLAUDE.md` exists for this sub-project with Pet Health Tracker context
- [ ] Every task can be picked up by an agent independently and executed in < 10 minutes
- [ ] Executing all tasks sequentially produces a publishable paid Android app
- [ ] Medication reminder reliability is explicitly tested (safety-critical feature)

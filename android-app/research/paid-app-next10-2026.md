# Paid Android App — Next 10 Market Feasibility Rankings
_Research date: 2026-04-05 | Scope: Solo dev, Kotlin/Android, Bangkok, ~5 hrs/week_
_Continuation of paid-app-top20-2026.md — 10 new concepts not in original list_

---

## Scoring Framework (same as Top 20)

| Dimension | 1 (Worst) | 5 (Best) |
|-----------|-----------|----------|
| **Market Size** | Tiny niche (<10K realistic installs) | Large proven market (100K+ installs possible) |
| **Competition** | Dominated by free, well-funded apps | Clear gap, no strong paid incumbent |
| **Build Effort** | 10+ weeks solo | Under 3 weeks solo |
| **Revenue Ceiling** | <$200/mo steady state | >$1,000/mo steady state |
| **Thai Fit** | No Thai angle | Massive Thai-specific gap |
| **Differentiation** | Me-too product | Unique positioning hard to copy |

**Max score: 30**

---

## NEXT 10 RANKED

---

### #21 — Thai Lottery Tracker & Lucky Number Generator (Freemium + $0.99 unlock)
**Score: 24/30**

| Dimension | Score | Evidence |
|-----------|-------|---------|
| Market Size | 4 | 30M+ regular lottery participants in Thailand; lottery drawn 1st & 16th every month = 24 engagement events/year |
| Competition | 4 | Existing apps are ad-heavy, crash-prone, outdated UI; no clean paid option |
| Build Effort | 4 | Ticket number storage + result scraper + push notification = 2–3 weeks |
| Revenue Ceiling | 3 | Freemium: free 3 tickets → $0.99 unlock unlimited + notifications = $300–$500/mo |
| Thai Fit | 5 | Ultra-Thai; lottery is a cultural ritual — every adult Thai household participates |
| Differentiation | 4 | Clean UI + offline storage + instant push result alerts + lucky number stats |

**Key data**: Thailand Government Lottery Office draws twice monthly. Top 3 existing apps have 2.5–3.0 star ratings with "crashes", "too many ads", "no notifications" as #1 complaints. A clean, crash-free experience with push alerts is immediately differentiated.

**Revenue model**: Free (store 3 tickets, manual result check) → $0.99 one-time unlock (unlimited tickets, auto result check, push notifications on draw day).

**Build scope**: Ticket number input, lottery result API/scraper (government announces publicly), match checker, push notification on draw days, lucky number trend stats (which numbers won most). No backend needed beyond a simple result checker.

**Thai angle**: Add Chinese zodiac lucky number generator + birth-date-based lucky numbers (Thai numerology) as premium features. Unique globally, massive locally.

**Risk**: Government lottery result URL could change. Build with multiple result sources (Thai government website + secondary mirror) for resilience.

---

### #22 — Thai Astrology & Lucky Day Calculator (Freemium + $1.49 one-time)
**Score: 24/30**

| Dimension | Score | Evidence |
|-----------|-------|---------|
| Market Size | 4 | 60M Thai users; astrology/horoscope is deeply embedded in Thai-Buddhist culture — consulted before weddings, business decisions, major purchases |
| Competition | 4 | Thai astrology apps have 2.8–3.2 star averages; UI from 2014; no quality paid option |
| Build Effort | 4 | Thai calendar algorithms + Chinese zodiac + lucky day engine = 3–5 weeks |
| Revenue Ceiling | 3 | $1.49 × 400 sales/mo = $360/mo; or freemium with premium forecast pack |
| Thai Fit | 5 | Peak Thai-specific; Thai Buddhist calendar, Rahu/Ketu days, auspicious hours — Western astrology apps miss all of this |
| Differentiation | 4 | Thai Buddhist calendar + Chinese zodiac + Thai numerology + birth chart = no Western app can replicate |

**Key data**: Thai people consult astrology for: wedding dates, house move dates, business opening, car purchases. This is daily-use in Thailand, not novelty. Existing apps (เบอร์มงคล, ดูดวง series) are ad-stuffed and crash frequently. A clean, fast, offline Thai astrology tool fills a real gap.

**Revenue model**: Free (daily horoscope + current week) → $1.49 one-time unlocks full birth chart, auspicious date calculator, Thai numerology (เลขมงคล), daily Rahu hour table.

**Build scope**: Thai Buddhist calendar (overlaid on Gregorian), Chinese zodiac wheel, Thai birth chart calculation, auspicious day/time calculator (Thai traditional system), daily lucky colors + directions, phone number lucky digit analyzer (เบอร์มงคล — very popular in Thailand).

**Unique moat**: Thai phone number lucky digit analysis (เบอร์มงคล) is a standalone killer feature — Thai people pay for this from fortune tellers. No app does it cleanly.

**Risk**: Accuracy of traditional Thai astrological formulas requires research; errors damage credibility in this culturally sensitive category.

---

### #23 — Offline English-Thai Dictionary & Phrasebook (Paid $1.99 one-time)
**Score: 23/30**

| Dimension | Score | Evidence |
|-----------|-------|---------|
| Market Size | 4 | 18M+ tourists/yr + 100K+ expats in Thailand; every tourist needs translation help |
| Competition | 3 | Google Translate requires internet; offline Thai dictionaries are old, ugly, or free-with-ads |
| Build Effort | 4 | Lexitron DB (NECTEC, open license) + tones visualization + phrasebook = 3–5 weeks |
| Revenue Ceiling | 3 | $1.99 × 500 sales/mo = $600/mo; expats buy once and use daily |
| Thai Fit | 5 | Core use case is visitors to Thailand — 100% aligned |
| Differentiation | 4 | Full offline (works in rural Thailand with no signal) + Thai tone guide + tourist phrasebook + Thai script pronunciation |

**Key data**: NECTEC Lexitron dictionary (English-Thai, 80,000+ words) is free for non-commercial use with license available. Google Translate fails in rural Thailand, on flights, in subway dead zones. Tourists consistently report needing an offline option.

**Revenue model**: Paid $1.99 one-time. No backend. Optional $0.99 IAP packs: Isaan Dialect Pack, Medical Thai (hospitals), Legal Thai (visas/contracts).

**Build scope**: Lexitron dictionary search, Thai script rendering, tone marks visualization (rising/falling/etc.), romanization (RTGS system), categorized phrasebook (food/transport/emergency/market), offline-first (zero internet required), favorites list.

**Differentiator vs Google Translate**: Works 100% offline + Thai tone guide + tourist-specific phrasebooks. Google Translate has no tone visualization, no phrasebook structure.

**Risk**: NECTEC Lexitron license compliance must be verified carefully. Dictionary data quality is older (last major update ~2014) — supplemental word list needed for modern Thai slang.

---

### #24 — Calorie & Macro Tracker with Thai Food Database (Paid $2.99 one-time)
**Score: 22/30**

| Dimension | Score | Evidence |
|-----------|-------|---------|
| Market Size | 5 | MyFitnessPal has 200M+ registered users — one of the largest proven markets in health apps |
| Competition | 3 | MyFitnessPal $79.99/yr → barcode scanner moved behind paywall Oct 2025 = mass exodus; Cronometer free but no Thai foods |
| Build Effort | 3 | Open Food Facts DB (free, 3M+ products) + Thai food DB (build manually, 500 dishes) + barcode scan = 5–7 weeks |
| Revenue Ceiling | 4 | $2.99 × 700 sales/mo = $1,260/mo; massive total addressable market |
| Thai Fit | 3 | Thai food database (pad thai, som tam, khao man gai, etc. with accurate macros) = unique globally |
| Differentiation | 4 | No account required + offline barcode scan + Thai food DB + one-time paid vs $79.99/yr MFP |

**Key data**: MyFitnessPal moved barcode scanning behind paywall in October 2025. App store reviews immediately spiked with 1-star reviews: "looking for alternatives", "switching apps", "won't pay $80/yr for a calorie counter". This is a live, active opportunity.

**Revenue model**: Paid $2.99 one-time. Open Food Facts for international barcodes (free API, 3M+ products). Thai dishes entered manually (500 common dishes = strong differentiation, no other app has this).

**Build scope**: Food logging (meal + time), barcode scanner (ML Kit + Open Food Facts), Thai food database (manually curated), macro pie chart, calorie goal tracker, weekly trend chart, water intake log. Room DB, fully offline.

**Thai angle**: Accurate macros for pad thai, green curry, mango sticky rice, som tam, khao pad, etc. — every existing app has wildly inaccurate Thai food data or doesn't have it at all.

**Risk**: Open Food Facts data quality is inconsistent (user-submitted). Build a data validation layer. Thai food DB requires research time (~20 hrs) to compile accurately.

---

### #25 — Invoice Generator for Thai Freelancers (Paid $2.99 one-time)
**Score: 22/30**

| Dimension | Score | Evidence |
|-----------|-------|---------|
| Market Size | 3 | 4.5M freelancers in Thailand (2025); growing digital economy; every freelancer needs invoicing |
| Competition | 4 | No Thai-VAT-aware, offline, one-time paid invoice app; Wave/Billdu require cloud accounts + subscriptions |
| Build Effort | 4 | PDF generation + client DB + Thai tax logic + THB formatting = 3–4 weeks |
| Revenue Ceiling | 3 | $2.99 × 400 sales/mo = $720/mo; B2B angle = higher willingness to pay |
| Thai Fit | 4 | Thai VAT (7%), withholding tax (3%), Thai company/ID number fields, Thai Baht — no app handles this natively |
| Differentiation | 4 | Thai-tax-aware + offline-first + one-time paid vs subscription-based competitors |

**Key data**: Thai freelancers must issue invoices with: client's Thai company registration number, withholding tax (ภาษีหัก ณ ที่จ่าย) at 3%, VAT at 7%, and a formal Thai-language invoice format recognized by Thai Revenue Department. No existing mobile app handles this correctly out of the box.

**Revenue model**: Paid $2.99 one-time. PDF invoices generated locally (no cloud). Optional $1.99 IAP: Thai Revenue Department e-Tax invoice templates.

**Build scope**: Client management, invoice line items, Thai tax calculation (VAT + WHT), PDF generation (iTextG library), email/share invoice, invoice history, Thai + English language toggle. No backend needed.

**Unique moat**: Thai withholding tax logic is specific enough that no international invoice app handles it. A developer based in Bangkok can build this correctly — impossible for US/EU developers to get right without living it.

**Risk**: Thai tax law changes require app updates. Track Thai Revenue Department announcements.

---

### #26 — Document Scanner: Offline, No Cloud (Paid $2.99 one-time)
**Score: 21/30**

| Dimension | Score | Evidence |
|-----------|-------|---------|
| Market Size | 4 | CamScanner has 100M+ downloads — one of the most-downloaded utility apps ever |
| Competition | 3 | CamScanner subscription backlash; Adobe Scan (free but requires Adobe account + cloud); Microsoft Lens (requires Microsoft account) |
| Build Effort | 3 | ML Kit document detection + perspective correction + PDF output = 4–6 weeks |
| Revenue Ceiling | 4 | $2.99 × 600 sales/mo = $1,080/mo |
| Thai Fit | 3 | Thai OCR as unique feature; Thai ID card scanning is a real use case |
| Differentiation | 4 | "Scan. No account. No cloud. No subscription. Buy once." — direct counter to CamScanner |

**Key data**: CamScanner was free for years, then moved core features behind a $4.99/mo subscription in 2024. Adobe Scan is free but requires Adobe account and uploads to Adobe cloud (privacy concern). Microsoft Lens requires Microsoft account. All three require internet. There is a clear gap for a privacy-first, offline-only document scanner.

**Revenue model**: Paid $2.99 one-time. No backend. PDF files saved to device/SD card only. No manifest INTERNET permission (trust signal visible in Play Store).

**Build scope**: Camera capture with auto-edge detection (ML Kit), perspective warp correction, brightness/contrast enhancement, multi-page PDF creation, local file management, Share via (email, WhatsApp, Drive — user's choice), Thai ID card scanning mode (pre-sized crop guide).

**Risk**: ML Kit document detection quality matters — invest time in tuning edge detection accuracy. Poor scan quality = 1-star reviews.

---

### #27 — Workout & Strength Training Log (Offline, Paid $1.99 one-time)
**Score: 21/30**

| Dimension | Score | Evidence |
|-----------|-------|---------|
| Market Size | 4 | Strong (iOS paid) has 4M+ users at $9.99/mo; massive proven demand for gym logging |
| Competition | 3 | Strong iOS dominant; Hevy Android is free but limited; no dominant paid Android gym log |
| Build Effort | 4 | Exercise DB + sets/reps + 1RM calculator + progress charts = 3–5 weeks |
| Revenue Ceiling | 3 | $1.99 × 500 sales/mo = $600/mo; gym community pays for quality tools |
| Thai Fit | 3 | Bangkok gym culture is strong; Muay Thai conditioning log as unique angle |
| Differentiation | 4 | One-time paid; offline-first; Muay Thai training mode (rounds, knees, kicks logged separately) |

**Key data**: Strong app (iOS) charges $9.99/month and has millions of users — proves gym enthusiasts pay for logging tools. On Android, Hevy is free but frequently complained about for lacking offline mode, slow syncs, and pushing Pro ($9.99/mo). A $1.99 offline-first, one-time paid alternative fills the gap.

**Revenue model**: Paid $1.99 one-time. No backend. Optional $0.99 IAP: Muay Thai training log mode (pad work sessions, sparring rounds, conditioning circuits).

**Build scope**: Exercise library (300+ exercises with illustrations), workout builder, sets/reps/weight logger, 1RM calculator, personal record tracker, muscle group heat map, weekly volume chart, rest timer with notification, CSV export.

**Muay Thai angle**: Bangkok has 100+ Muay Thai gyms. Muay Thai-specific training log (rounds, techniques, sparring partners) is a unique feature no gym app has — targetable via Thai fitness Facebook groups for free marketing.

---

### #28 — Screen Time Controller & App Blocker (Paid $2.99 one-time)
**Score: 20/30**

| Dimension | Score | Evidence |
|-----------|-------|---------|
| Market Size | 4 | Thai average daily screen time = 8+ hours; Freedom app (subscription) has 3M+ users globally |
| Competition | 3 | Android Digital Wellbeing is built-in but basic; Freedom $6.99/mo; one-time paid gap clear |
| Build Effort | 3 | UsageStatsManager + AccessibilityService + scheduling = 4–6 weeks |
| Revenue Ceiling | 3 | $2.99 × 400 sales/mo = $720/mo |
| Thai Fit | 3 | Thai screen time is among highest globally; parents want to limit kids' TikTok/YouTube |
| Differentiation | 4 | "Pay once, focus forever" vs Freedom $6.99/mo; parental mode; works offline; no account |

**Key data**: Freedom charges $6.99/month or $39.99/year to block distracting apps. Android's built-in Digital Wellbeing has no scheduled blocking, no strict mode, and is easily bypassed by children. A $2.99 one-time alternative with: scheduled block times, parent PIN lock, and bedtime mode is immediately compelling.

**Revenue model**: Paid $2.99 one-time. No backend. Optional $1.99 IAP: Parental Dashboard (parent PIN, report on child's app usage).

**Build scope**: App selection for blocking, schedule builder (block TikTok 10pm–6am), strict mode (cannot be bypassed without PIN), daily usage stats per app, bedtime mode (auto-blocks all except alarms + calls), widget showing today's screen time.

**Android constraint**: Accessibility Service required — Google Play has tightened these restrictions in 2024. Must write a clear declaration of use for Play Store review.

**Risk**: Android 15+ accessibility service policy changes could affect functionality. Monitor Google policy updates carefully.

---

### #29 — Plant Care Tracker for Thai & Tropical Plants (Paid $1.99 one-time)
**Score: 19/30**

| Dimension | Score | Evidence |
|-----------|-------|---------|
| Market Size | 3 | PictureThis 50M+ downloads proves plant app appetite; houseplant market booming post-COVID |
| Competition | 4 | PictureThis $39.99/yr backlash is strong; PlantNet free but identification-only; no care-focused paid option |
| Build Effort | 3 | Plant DB + watering reminders + care logs = 3–5 weeks (no AI identification needed) |
| Revenue Ceiling | 3 | $1.99 × 400 sales/mo = $480/mo |
| Thai Fit | 3 | Orchids, tropical ferns, Thai herbs (holy basil, kaffir lime, galangal), bougainvillea — no app has these |
| Differentiation | 3 | Skip AI identification; focus on care tracking + Thai tropical plant database + offline reminders |

**Key data**: PictureThis built its brand on AI plant identification, but charges $39.99/yr for it. Users who already know their plants and just want care reminders don't need identification — they need watering schedules and seasonal care notes. A focused, cheap, one-time paid care tracker is a clear sub-segment.

**Revenue model**: Paid $1.99 one-time. Optional $0.99 IAP: Thai Herbs & Edible Plants pack (basil types, galangal, lemongrass, kaffir lime with Thai cooking use notes).

**Build scope**: Plant library (500 common tropical + houseplants with care schedules), add custom plants, watering + fertilizing reminder system (WorkManager), seasonal care tips, health log (photo diary of plant over time), humidity/sunlight requirement display.

**Positioning**: "Not an identifier. A plant care diary — for people who already know what they're growing."

---

### #30 — Metronome + Tuner Pro (One-Time Paid $1.99)
**Score: 18/30**

| Dimension | Score | Evidence |
|-----------|-------|---------|
| Market Size | 3 | Metronome Beats 10M+ free downloads; musicians globally |
| Competition | 3 | Metronome Beats (free, ad-supported); Pro Metronome (subscription); paid one-time gap |
| Build Effort | 5 | Audio DSP + pitch detection + metronome logic = 2–3 weeks |
| Revenue Ceiling | 2 | $1.99 × 300 sales/mo = $360/mo ceiling |
| Thai Fit | 2 | Musicians; Thai classical instrument scales as bonus feature |
| Differentiation | 3 | One-time paid + Thai classical scales (ranat, khim tuning) + offline |

**Key data**: Tonal Energy Tuner (iOS) is a paid success — musicians pay for quality audio tools. Android equivalent is fragmented: Metronome Beats free (ads), Pro Metronome (subscription). A clean, one-time-paid metronome + chromatic tuner bundle fills the niche.

**Revenue model**: Paid $1.99 one-time. Includes: metronome (40–208 BPM, subdivision support, tap tempo), chromatic tuner (±1 cent accuracy), drone tone generator, Thai classical instrument tuning presets (ranat ek, khim).

**Build scope**: Metronome with visual pulse + audio, BPM tap detect, subdivision patterns (quarter/eighth/triplet), chromatic tuner via microphone (FFT pitch detection), drone generator, setlist mode (multiple BPMs in sequence). Minimal permissions.

**Risk**: Lowest revenue ceiling of the 10 — consider this a "fast win" to ship in 2–3 weeks and prove the paid model before tackling larger apps.

---

## Master Ranking Table (Next 10)

| Rank | App Concept | Score | Model | Est. Monthly Rev | Build (weeks) |
|------|-------------|-------|-------|-----------------|---------------|
| 21 | **Thai Lottery Tracker** | 24/30 | $0.99 freemium unlock | $300–$500 | 2–3 |
| 22 | **Thai Astrology & Lucky Day** | 24/30 | $1.49 one-time | $300–$600 | 3–5 |
| 23 | **Offline English-Thai Dictionary** | 23/30 | $1.99 one-time | $400–$600 | 3–5 |
| 24 | **Calorie & Macro Tracker (Thai Food DB)** | 22/30 | $2.99 one-time | $800–$1,200 | 5–7 |
| 25 | **Invoice Generator (Thai Freelancers)** | 22/30 | $2.99 one-time | $500–$700 | 3–4 |
| 26 | **Document Scanner (Offline, No Cloud)** | 21/30 | $2.99 one-time | $700–$1,000 | 4–6 |
| 27 | **Workout & Strength Training Log** | 21/30 | $1.99 one-time | $400–$600 | 3–5 |
| 28 | **Screen Time Controller / App Blocker** | 20/30 | $2.99 one-time | $500–$700 | 4–6 |
| 29 | **Plant Care Tracker (Thai Plants)** | 19/30 | $1.99 one-time | $300–$480 | 3–5 |
| 30 | **Metronome + Tuner Pro** | 18/30 | $1.99 one-time | $200–$360 | 2–3 |

---

## Combined Top 30 Strategic Analysis

### New Tier 1 Additions (Score 22+, strong ROI)
| # | App | Why This Ranks High |
|---|-----|---------------------|
| 21 | Thai Lottery Tracker | Fastest to build in this list; 30M engaged users; cultural ritual = daily use |
| 22 | Thai Astrology & Lucky Day | Unique Thai moat; เบอร์มงคล feature is standalone viral hook; high daily engagement |
| 23 | Offline English-Thai Dictionary | 100% offline + Lexitron free DB + no app does Thai tones correctly |
| 24 | Calorie Tracker (Thai Food DB) | Biggest TAM in the list; MyFitnessPal paywall exodus is live right now |
| 25 | Invoice Generator (Thai) | No competition in Thai-tax-aware space; B2B = higher price tolerance |

### Highest-Conviction New Entry
**Thai Lottery Tracker (#21)** is the single best new discovery:
- 2–3 week build (fastest on the list)
- 30M active users checking results twice monthly
- Existing apps are genuinely terrible (2.5 stars)
- Thai cultural moat: no Western developer will compete here
- $0.99 price is frictionless for Thai users

If the goal is shipping fast and proving the paid model, Thai Lottery Tracker before Habit Tracker.

### Updated Sequential Build Recommendation
1. **Thai Lottery Tracker** (2–3 wks) — fastest revenue proof, Thai moat, low risk
2. **Habit Tracker** (3–4 wks) — proves $1.99 paid model on universal use case
3. **Thai Astrology & Lucky Day** (3–5 wks) — high engagement, cultural lock-in
4. **Calorie Tracker with Thai Food DB** (5–7 wks) — biggest TAM, live MFP exodus
5. **Thai Language Learning** (10–12 wks) — highest long-term ceiling

---

## Key Market Forces Confirmed (2026)

1. **Subscription fatigue is real and accelerating**: Consumers demanding one-time purchase clarity. Weekly subscriptions now generate 55% of app revenue but retain less than 5% past 6 months — churn is structural.

2. **MyFitnessPal paywall move = active opportunity**: Barcode scanner behind paywall October 2025 triggered mass user exodus. This is a 6-month window to capture switchers.

3. **Thai market is genuinely underserved**: 1,228 Thai Android developers active on Google Play — tiny relative to 60M Thai smartphone users. Quality gap is large.

4. **Thai daily screen time = 8+ hours**: Highest in Southeast Asia. Both opportunity (screen time app, digital wellbeing) and distribution advantage (social media marketing is highly effective).

---

_Sources: AppBrain paid rankings, 42matters Thailand App Market Statistics 2025, Adapty State of In-App Subscriptions 2026, RevenueCat State of Subscription Apps 2026, influencers-time.com subscription fatigue series, MyFitnessPal pricing blog + App Store reviews, PictureThis review analysis, NECTEC Lexitron dictionary (NECTEC.or.th), Thai Revenue Department freelancer requirements, Soundbrenner metronome Play Store, Google Play Store rankings April 2026, SimilarWeb Thailand top apps_

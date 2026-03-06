# Business Research: GenCNX (gencnx.com)

**Purpose:** Understand GenCNX's business model to design better competing/complementary web services
**Research Date:** 2026-03-06
**Research Method:** JavaScript bundle reverse-engineering (SPA — server returns only analytics shell)
**Status:** Complete — data extracted from `/assets/index-CqtAHi0K.js` (2.2MB bundle)

---

## 1. Company Overview

| Field | Data |
|---|---|
| Domain | gencnx.com |
| Brand Name | GenCNX |
| Meta Description | "AI-powered creative platform for images, videos, and music" |
| Language | Thai (primary) + English (bilingual UI) |
| Market | Thailand / Southeast Asia |
| Analytics | Google Analytics 4 — `G-GDHCZ80L9R` |
| Twitter | @GenCNX |
| Backend | Supabase (BaaS — Auth + DB) |
| Frontend | React (Vite SPA) |
| Target Users | Content creators, YouTubers, TikTokers, Thai-market businesses |

**Name Interpretation:**
- **Gen** = Generate / Generation
- **CNX** = Chiang Mai (IATA airport code CNX) — suggesting Chiang Mai, Thailand origin

---

## 2. Business Model

GenCNX is an **AI-powered creative platform** operating two parallel monetization models:

### Model A: Credit-Based AI Generation (Core Platform)
- Users buy credit packages and spend credits to generate AI content
- Credit consumption varies by AI model and output quality
- Credits never expire (implied from top-up model)

### Model B: One-Time Product Purchases (Software Licenses)
- Standalone tools sold as one-time purchases (not subscriptions)
- Includes Chrome extensions and custom automation systems
- Higher-ticket items include free GenCNX credits as bonus

---

## 3. Core AI Generation Services (Credit-Based)

All services accessible from the **Generate** menu, priced in GenCNX credits:

### Video Generation
| Service | AI Model | Key Details |
|---|---|---|
| Veo 3 Video | Google Veo 3.1 | 8-second videos, Text or Image to Video |
| Sora 2 Video | OpenAI Sora 2 | 10–15 second highly realistic videos |
| Grok AI Video | xAI Grok | Text/Image to Video + image generation |
| Sora Watermark Remover | — | Instantly remove Sora 2 watermarks |
| Dance Video | — | Add dance moves to images (character animation) |
| Transition Video | Google Veo 3.1 | Transition clip between 2 images |
| Alternative Video | — | Affordable 10s video generation (lower cost model) |
| Professional Video | — | Templates + advanced settings for polished output |
| Batch Video | — | Multiple videos at once from line-separated prompts |
| Viral Auto-Video | — | Select character, category, language, quantity → auto-generate |
| Video Merge | — | Merge 2–5 video files into single output |
| Gemini Chat | Google Gemini AI | Chat, image analysis, clone images/videos |

### Image Generation
| Service | AI Models Supported |
|---|---|
| Image Generation | GPT Image (OpenAI), Seedream 4.5, Nano Banana, Nano Banana Pro |
| Cover Generator | YouTube / Facebook covers with AI + ready-made templates |
| Prompt Generator | AI analyzes uploaded image → generates style-mimicking prompts |
| Background Remover | AI background removal → transparent PNG output |
| Watermark Tool | Add custom watermarks to videos or images |
| Batch Image | Multiple images at once from prompts or CSV/TXT file upload |

### Audio / Speech
| Service | AI Model | Key Details |
|---|---|
| Music Generation | Suno V5 | Vocal + instrumental tracks |
| Text to Speech | ElevenLabs | Multi-language, customizable voice settings |
| Conversation Generator | ElevenLabs | 2-speaker realistic conversations with emotions |

### Utilities / Productivity
| Service | Description |
|---|---|
| AI Assistant | Personal assistant for prompts, scripts, problem-solving |
| History | Full generation history |
| Dashboard | Usage overview, credit balance |

---

## 4. Credit Pricing Structure

### Credit Consumption by Feature (confirmed from source)
| Feature | Credits |
|---|---|
| Music Generation | Starting from 30 credits |
| Clone Video / Review Submission | 110 credits |
| Sora 2 (15s video) | ~70 credits default |
| Video Upscale 720p | 80 credits |
| Video Upscale 1080p | 140 credits |
| Standard generation default | ~100 credits |

### Credit Package Pricing (THB)
Credit packages are configured by admin with cost-per-1,000-credits tracked for profit calculation. Packages are sold to users via an in-platform purchase flow.

**Cost structure visible in admin:**
- Admin sets "Cost per 1,000 Credits (฿)" — used to calculate profit per package
- Users see package list with credit amounts (e.g., 1 Credit test, bulk packages)
- New-user bonus credits offered at registration

---

## 5. One-Time Purchase Products

Sold via a product/shop section — one-time payment, not subscription:

### Product 1: AI Video Pro — **1,990 THB**
- License: 2 devices
- **Features:**
  - Video upscaling to Full HD (HD → Full HD, same clarity, metadata-compatible)
  - Auto crop black bars
  - Merge multiple video files
  - Add custom watermarks
  - Multi-format support
- **Target:** YouTubers, TikTokers, Facebook video creators
- **Marked as Popular** in product listing

### Product 2: Veo3 Auto Extension — **1,490 THB**
- License: 2 devices
- Chrome browser extension
- **Features:**
  - Schedule auto-generation (set time, walk away)
  - Auto-download completed videos
  - Queue system for continuous batch jobs
  - Notifications on completion
- **Target:** Creators using Google Veo3 who need automation

### Product 3: YouTube Spy Pro — **19,990 THB** + 10,000 free GenCNX credits
- **Features:**
  - Unlimited YouTube channel tracking
  - Keyword-based search
  - Real-time viral clip alerts (spike detection on unusual view growth)
  - Trend analysis and statistics
  - Data export
- **Target:** Content strategists, growth hackers, competitive research

### Product 4: Custom Automation Program — **99,000 THB** + 50,000 free GenCNX credits
- **Features:**
  - Fully custom-built automation system for business requirements
  - Examples: auto video editing, cross-platform content posting, big data management
  - Full source code delivered — 100% ownership
  - Extensible for future development
- **Target:** Businesses, agencies wanting proprietary automation

---

## 6. Revenue Model Summary

| Stream | Type | Price Range |
|---|---|---|
| Credit Packages | Recurring / Top-up | Small (30 credits) to large packages |
| AI Video Pro | One-time license | 1,990 THB (~$55) |
| Veo3 Auto Extension | One-time license | 1,490 THB (~$41) |
| YouTube Spy Pro | One-time license | 19,990 THB (~$555) |
| Custom Automation | One-time development | 99,000 THB (~$2,750) |

**Revenue Concentration Risk:** Heavily tied to third-party AI API access (Google Veo, OpenAI Sora, ElevenLabs, Suno). Model pricing changes upstream directly impact margins.

---

## 7. Cost Structure Analysis

| Cost Category | Estimate | Basis |
|---|---|---|
| AI API costs | 50–70% of COGS | Google Veo3, OpenAI Sora2, ElevenLabs, Suno V5 |
| Supabase BaaS | Low-Medium | Auth + DB + storage |
| CDN / Video storage | Medium | Generated video files |
| Engineering | Fixed | Likely small team (startup-scale) |
| Credit cost tracking | Built-in | Admin panel tracks cost-per-1000-credits |

---

## 8. Operations & Tech Stack

| Component | Technology |
|---|---|
| Frontend | React (Vite, JSX), SPA |
| UI Components | Radix UI, Tailwind CSS, Sonner (toasts) |
| State Management | React Context |
| Routing | React Router (client-side) |
| Backend / Auth / DB | Supabase (GoTrue Auth v2.89.0) |
| Analytics | Google Analytics 4 |
| AI Models | Google Veo 3.1, OpenAI Sora 2, GPT Image, xAI Grok, ElevenLabs, Suno V5, Gemini AI, Seedream 4.5 |
| SEO | Poor — full SPA, no SSR, not indexed by search engines |

---

## 9. Competitive Analysis

### GenCNX vs. Global Competitors

| Platform | GenCNX | HeyGen | Synthesia | Invideo AI |
|---|---|---|---|---|
| Market focus | Thailand/SEA | Global | Enterprise | Global |
| Pricing model | Credits + one-time | Subscription | Subscription | Subscription |
| AI avatars | No | Yes | Yes | No |
| Multi-language | Thai + English | 175+ langs | 140+ langs | 50+ langs |
| Video AI models | Veo3, Sora2, Grok | Custom | Custom | Custom |
| Music generation | Yes (Suno V5) | No | No | No |
| Background removal | Yes | No | No | Limited |
| YouTube spy tool | Yes | No | No | No |
| Custom automation | Yes (99k THB) | No | No | No |
| SEO visibility | Minimal | Strong | Strong | Strong |

### GenCNX Unique Strengths
1. **Aggregates latest AI models** — Veo3, Sora2, Grok, Suno V5 all in one platform
2. **Thai language native** — underserved market with lower competition
3. **One-time purchase option** — avoids subscription fatigue for tools
4. **YouTube Spy** — competitive intelligence not available in most AI video platforms
5. **Source code ownership** — attractive for businesses wanting full control

### GenCNX Weaknesses / Gaps
1. **No SSR / SEO** — SPA means zero organic search traffic
2. **Credit system opacity** — pricing unclear without creating account
3. **No social posting integration** — generates content but doesn't auto-post
4. **No template marketplace** — templates only from platform, no community-created
5. **No affiliate/reseller program** — growth limited to direct acquisition
6. **Single-language UI priority** — English secondary; limits global reach
7. **No analytics for generated content** — can't track performance of posted videos

---

## 10. Opportunities: Building a Better Service

### 10.1 Product Gaps to Fill

| Gap | Opportunity |
|---|---|
| No auto-posting | Build generate-to-schedule-to-post pipeline (TikTok, YouTube, IG, FB) |
| No content analytics | Add performance tracking: views, CTR, watch-time per generated video |
| No affiliate program | Implement 30% recurring affiliate commission |
| No template marketplace | Allow creators to sell templates — community flywheel |
| No SEO / blog | Build educational content for SEO traffic acquisition |
| No video A/B testing | Auto-generate 3 variants, track winner, scale it |
| No white-label | Enterprise reseller program for agencies |

### 10.2 Technical Improvements

1. **Server-Side Rendering (SSR)** — Next.js/Nuxt for SEO + faster initial load
2. **Real-time progress** — WebSocket video generation status instead of polling
3. **API-first architecture** — Expose REST/GraphQL API for developer integration
4. **Better credit UX** — Show estimated credits before generating, not after
5. **Offline Chrome extension** — Local queue management without cloud dependency

### 10.3 Business Model Improvements

1. **Freemium tier** — 50 free credits/month with watermark → viral growth
2. **Monthly subscription** — Flat-rate unlimited for power users (vs. pure credits)
3. **Team plans** — Shared credit pool for agencies and businesses
4. **API pricing** — Developers pay per API call (separate from credit system)
5. **Revenue share model** — Partner with content creators who use the platform

### 10.4 Market Expansion

1. **ASEAN localization** — Vietnamese, Indonesian, Malay UI
2. **Vertical SaaS** — E-commerce product video, real estate listing videos
3. **TikTok Shop integration** — Auto-generate product review videos from product URL
4. **Education sector** — Course intro videos, explainer generation
5. **Enterprise compliance** — Data residency for regulated industries

---

## 11. SWOT Summary

| | Strengths | Weaknesses |
|---|---|---|
| **GenCNX** | All-in-one AI model aggregator; Thai-native; one-time purchase option; YouTube intelligence tool | No SSR/SEO; opaque credit pricing; no auto-posting; no analytics; small team capacity |

| Opportunities | Threats |
|---|---|
| Underserved Thai/ASEAN market | Google/OpenAI launching direct consumer tools |
| TikTok/Reels driving massive demand for short video | Rapid commoditization of AI video models |
| Businesses wanting automation with source code ownership | API pricing increases from Sora/Veo/ElevenLabs upstream |
| No strong local competitor in Thai AI video | Larger global platforms entering SEA |

---

## 12. Action Plan: Building a Better Service

### Phase 1: Foundation
- [ ] Sign up on GenCNX — document UX, credit pricing, generation quality
- [ ] Generate test videos using Veo3, Sora2 via GenCNX — compare quality and cost per video
- [ ] Map all credit costs for every feature type
- [ ] Interview 3–5 Thai content creators about pain points with GenCNX

### Phase 2: Differentiate
- [ ] Choose primary niche: TikTok auto-video? YouTube auto-channel? E-commerce?
- [ ] Define killer feature missing from GenCNX (auto-posting pipeline recommended)
- [ ] Design credit pricing that is transparent pre-generation
- [ ] Plan SEO content strategy (blog, tutorials) — GenCNX has none

### Phase 3: Build (→ prompt_auto_gen_video.md → plan_build_auto_gen_video.md)
- [ ] MVP: URL/topic → AI script → AI video → auto-post to TikTok/YouTube
- [ ] Add credit transparency and usage dashboard
- [ ] Launch freemium with watermark → convert to paid

---

## References

- GenCNX JavaScript source: `https://www.gencnx.com/assets/index-CqtAHi0K.js` (2.2MB, analyzed 2026-03-06)
- Meta tag: `GenCNX - แพลตฟอร์มสร้างสรรค์ด้วย AI สำหรับรูปภาพ วิดีโอ และเพลง`
- [HeyGen](https://www.heygen.com/) — AI avatar video platform
- [Synthesia](https://www.synthesia.io/) — Enterprise AI video
- [ElevenLabs](https://elevenlabs.io/) — TTS provider used by GenCNX
- [Suno](https://suno.com/) — AI music provider used by GenCNX
- [Google Veo](https://deepmind.google/models/veo/) — Video AI used by GenCNX
- [OpenAI Sora](https://openai.com/sora) — Video AI used by GenCNX

# YouTube Content — Implementation Plan

> Dev tutorial YouTube channel. Record what BiG is already building. Zero extra prep.
> Revenue: YouTube AdSense + affiliate links + cross-sell digital products (Gumroad).
> Monetization threshold: 1,000 subscribers + 4,000 watch hours.

---

## Phase 0: Deep Market Research & Target Audience (DO FIRST)

**Goal:** Validate which video topics have highest search demand with lowest competition, and define exact viewer profile.

### Market Sizing & Validation
- [ ] Research YouTube search volume for target keywords (use TubeBuddy or vidIQ free tier):
  - "Claude Code tutorial" — monthly searches, competition score
  - "MCP server tutorial" — same
  - "build MCP server TypeScript" — same
  - "crypto trading bot tutorial" — same
  - "Godot 4 tutorial" — same
  - "Claude Code setup" — same
- [ ] Analyze top 10 results for each keyword: view count, channel size, upload date, engagement rate
- [ ] Identify "blue ocean" topics: >1K monthly searches + <10 competing videos with >10K views
- [ ] Research YouTube dev tutorial benchmarks:
  - What's avg CPM for programming tutorials? ($5-$15 US — verify for global audience)
  - What's avg view count for a new dev channel's first 10 videos?
  - How long until a new channel reaches 1K subscribers? (typical: 3-6 months with weekly uploads)
- [ ] Check YouTube Partner Program requirements: 1K subs + 4K watch hours in last 12 months
- [ ] Research affiliate program rates: Claude Pro, Railway, Vercel, Digital Ocean referrals

### Laser-Targeted Viewer Persona
- [ ] **Primary persona: "Dev Dan"** — English-speaking developer wanting to learn Claude Code:
  - Age: 22-35, male (75%+ of dev tutorial audience)
  - Experience: intermediate (2-5 years) — knows how to code, new to Claude Code
  - Watching on: laptop/desktop (not mobile — dev tutorials)
  - Search behavior: "how to [specific task] Claude Code" (problem-driven, not browsing)
  - What makes them click: clear title with outcome + time ("Build an MCP Server in 20 Min")
  - What makes them subscribe: practical, no fluff, real code, real results
  - What makes them leave: too slow intro, too basic, or too advanced without context
- [ ] **Secondary persona: "Indie Hacker Ian"** — building side projects with AI tools:
  - Wants to see real projects being built, not toy examples
  - Higher engagement (comments, shares) — community-oriented
  - More likely to buy digital products (Gumroad cross-sell opportunity)
  - Discovery: Hacker News, r/SideProject, Indie Hackers, Twitter/X
- [ ] Analyze top Claude Code YouTube channels:
  - Who are the top 5 creators covering Claude Code?
  - What video format works: screen-only? face+screen? voiceover? long-form vs shorts?
  - Which of their videos got the most views? (indicates highest-demand topics)
- [ ] Research r/ClaudeCode: what tutorial topics do people REQUEST but nobody has made yet?

### Competitor Channel Analysis
- [ ] Identify 5 dev tutorial channels in the Claude Code / AI tools niche
- [ ] For each: subscriber count, avg views per video, upload frequency, monetization signals
- [ ] What content gaps exist? (nobody does X, or existing videos on X are bad)
- [ ] Study their thumbnails: what style gets highest CTR in dev tutorials?
- [ ] Analyze their video descriptions: affiliate links, product links, community links

### Audience Discovery Channels
- [ ] Monitor r/ClaudeCode for "tutorial request" posts
- [ ] Check YouTube comments on competitor videos — what do viewers ask for?
- [ ] Monitor Hacker News for Claude Code / MCP discussions
- [ ] Check X/Twitter for "Claude Code" mentions — note common questions
- [ ] Research dev podcast audience overlap (potential guest appearance opportunity later)

### Research Deliverables
- [ ] Keyword priority matrix: topic × search volume × competition × BiG's expertise match
- [ ] Top 5 video topics ranked by "views per effort" potential
- [ ] Viewer persona card with discovery channels and content preferences
- [ ] Competitor channel analysis spreadsheet
- [ ] First 4-video content calendar based on research

---

## Content Strategy

Record BiG's actual dev workflow. Evergreen tutorials > trending content.

### Tier A — High Search Volume (English, Global Dev Audience)
1. "Claude Code multi-agent automation from scratch"
2. "Building an MCP server with TypeScript — full walkthrough"
3. "Crypto trading bot in Go — backtesting setup"
4. "Godot 4 indie game — slot mechanic tutorial"

### Tier B — Niche, Lower Competition
1. "Claude Code + crontab: automated side project runner"
2. "Polymarket data pipeline with Python"
3. "Shopee affiliate automation — Thailand"
4. "Go microservice on Railway in 20 minutes"

---

## Tooling

| Purpose | Tool | Cost |
|---------|------|------|
| Screen recording | macOS built-in + QuickTime | Free |
| Editor | CapCut or DaVinci Resolve | Free |
| Upload | YouTube Studio | Free |
| Thumbnails | Canva free tier | Free |

**Total cost: $0**

---

## Phase 1: Record First Video (During MCP-Apps Build)

**Goal:** Record raw footage of building the first MCP server. No extra prep needed.

### Tasks
- [ ] Hit record before starting mcp-apps Phase 1 build session
- [ ] Record full screen + microphone (no face cam needed initially)
- [ ] Aim for 30-60 minutes of raw footage (will edit to 10-15 min)
- [ ] Save raw recording to `youtube-content/raw/`

### Deliverable
Raw video recording of a real build session.

---

## Phase 2: Edit, Publish & Channel Setup

**Goal:** First video published. Channel configured for discoverability.

### Tasks
- [ ] Create YouTube channel (use existing Google account)
- [ ] Set channel name, description, banner, profile picture
- [ ] Edit raw footage to 10-15 minute tutorial:
  - [ ] Cut dead time, mistakes, waiting
  - [ ] Add chapter markers (timestamps in description)
  - [ ] Add text overlays for key commands/URLs
  - [ ] Add intro (5 seconds max) and outro with subscribe CTA
- [ ] Create thumbnail: face/screen + number ("Build an MCP Server in 20 Min")
- [ ] Write title (keyword-optimized, <60 chars)
- [ ] Write description with:
  - [ ] Timestamps/chapters
  - [ ] Links to code repo
  - [ ] Affiliate links (Claude Pro, Railway, tools used)
  - [ ] Link to Gumroad digital products (cross-sell)
- [ ] Add tags: Claude Code, MCP server, TypeScript tutorial, AI tools
- [ ] Publish video
- [ ] Share on r/ClaudeCode, X/Twitter, Hacker News

### Deliverable
First video published. Channel live.

---

## Phase 3: Publish 4 Videos (Monetization Application)

**Goal:** Meet YouTube Partner Program requirements (1K subs + 4K watch hours).

### Tasks
- [ ] Record and publish 4 videos over 4-8 weeks:
  - [ ] Video 1: MCP server build (from Phase 1)
  - [ ] Video 2: Claude Code automation setup (crontab + agents)
  - [ ] Video 3: Crypto trading bot backtest walkthrough
  - [ ] Video 4: Best video based on channel analytics feedback
- [ ] 10-minute minimum per video (ad mid-roll eligible)
- [ ] Cross-post clips to TikTok/Reels/Shorts (synergy with tiktok project)
- [ ] Engage with comments on every video
- [ ] Track: views, watch time, subscriber growth, CTR
- [ ] Apply for YouTube Partner Program when eligible

### Deliverable
4+ videos published. Progressing toward 1K subs / 4K watch hours.

---

## Phase 4: Monetize & Cross-Sell

**Goal:** Revenue from ads + affiliate links + digital product sales.

### Tasks
- [ ] Enable YouTube ads once approved for Partner Program
- [ ] Add affiliate links to all video descriptions:
  - [ ] Claude Pro ($20/month referral)
  - [ ] Railway (hosting referral)
  - [ ] Any tools used in tutorials
- [ ] Cross-link Gumroad digital products in every description
- [ ] Create "Resources" page/video linking to all products
- [ ] Analyze which videos drive most Gumroad sales — make more like those
- [ ] Consider sponsored content once at 5K+ subscribers

### Deliverable
Multiple revenue streams from each video (ads + affiliates + digital product sales).

---

## Key Principles

- **10-minute videos** perform best for tutorials (ad mid-roll eligible)
- **English titles** rank globally; Thai titles only for Thai-specific content
- **Thumbnail formula**: face/screen + number + bold text
- **Evergreen > trending** — tutorials stay relevant for years
- **Record during normal work** — zero additional time investment
- **First video doesn't need to be perfect** — publish and iterate

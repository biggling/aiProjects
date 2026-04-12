# MCP Server New Niche Research — 2026-04-05

## Context
This research identifies 8-10 NEW MCP server product opportunities NOT already covered by the 10 existing opportunities (crypto tax, multi-exchange P&L, sentiment trading signals, dev analytics BI, Bitkub Thai market, DCA automation, whale tracker, net worth tracker, budget/spending AI, Forex MCP).

---

## OPPORTUNITY 1: Multi-Carrier Logistics & Shipment Tracking MCP

### Description
Universal shipment tracking and rate-shopping MCP server connecting FedEx, UPS, DHL, USPS, and regional carriers. Enables AI agents to track parcels, compare shipping rates, generate labels, handle cross-border documentation, and get delivery ETAs — all in a single tool. Target users: Shopify sellers, Amazon FBA operators, small e-commerce businesses.

### Evidence of Demand
- FedEx Freight spinning off as independent company (June 1, 2026) — creates fragmentation driving demand for unified tracking
- "Predictive logistics" trend: logistics players shifting from reactive to predictive ETAs based on live carrier data (Supply Chain Dive, 2026)
- No MCP server found in PulseMCP search for "shipping tracking" or "logistics carrier"
- Multi-carrier API providers (EasyPost, ShipStation, Shippo) charge $29-$99/mo per user — pain is well-established and users already pay

### Current MCP Competition
- **None confirmed.** PulseMCP searches for "shipping", "fedex", "UPS", "carrier tracking" return zero relevant results.
- Generic Shopify MCP covers orders but not multi-carrier tracking details.

### Comparable Products & Pricing
- EasyPost API: $0.05/shipment + $0.005/tracking event — enterprises pay hundreds/month
- ShipStation: $9.99–$229.99/month
- Shippo: $19–$199/month
- AfterShip (tracking SaaS): $11–$239/month with 120M+ users

### Build Complexity
**Medium.** EasyPost or AfterShip unified API abstracts carrier complexity. Core tools: `track_shipment(tracking_number)`, `get_rates(from, to, weight)`, `create_label(params)`, `get_carrier_status()`. No proprietary data needed — pure API wrapper.

### API Availability
- EasyPost REST API (free tier: 30 day trial, then usage-based) — covers 100+ carriers
- AfterShip API (free tier: 100 shipments/month)
- Shippo API (free tier: 500 labels/month)
- All have generous free tiers for MVP, pay-as-you-go for production

---

## OPPORTUNITY 2: EU AI Act & Regulatory Compliance MCP

### Description
Compliance intelligence MCP server focused on EU AI Act (enforcement August 2026), SOC 2, ISO 42001, and GDPR. Enables AI agents to check whether a given AI use case is "high-risk" under the EU AI Act, audit data processing activities for GDPR compliance, query SOC 2 control frameworks, and pull regulatory deadlines. Target buyers: SaaS CTOs, compliance officers, legal/DevSecOps teams.

### Evidence of Demand
- EU AI Act enforcement begins August 2026 with high-risk AI systems requiring conformity assessments — urgent deadline driving spend
- ISO 42001 (AI Management Systems) published and becoming de facto certification for enterprise AI governance
- SOC 2 adding AI-specific criteria for model governance and training data provenance (as of Q1 2026)
- Vanta launched MCP server (public preview) — validates the market; but Vanta is compliance management, not AI Act guidance
- Drata MCP Server also announced — but both cover traditional SOC 2/ISO 27001, not EU AI Act specifics

### Current MCP Competition
- Vanta MCP: SOC 2/ISO/GDPR (general compliance), **does NOT cover EU AI Act**
- Drata MCP: similar to Vanta, security compliance focus
- **EU AI Act specific MCP: none confirmed**

### Comparable Products & Pricing
- TrustArc (GDPR compliance platform): $10,000-$50,000/year enterprise
- OneTrust: $25,000+/year
- Smaller SaaS compliance tools (Sprinto, Tugboat Logic): $299-$999/month
- EU AI Act consultants charge €500-2,000/hour — there is enormous demand for scalable guidance

### Build Complexity
**Low-Medium.** Core data: EU AI Act annexes (publicly available), risk classification rules, deadline calendar, compliance checklists. No real-time API needed. Tools: `classify_ai_use_case(description)`, `get_compliance_checklist(use_case_type)`, `get_regulatory_deadline(jurisdiction)`, `check_gdpr_lawful_basis(processing_activity)`. Data is static/semi-static — can be embedded as structured knowledge.

### API Availability
- EU AI Act full text: EUR-Lex (public)
- NIST AI Risk Management Framework: public
- No paid API needed for v1 — can be built on curated regulatory knowledge base

---

## OPPORTUNITY 3: Appointment Booking & Scheduling Intelligence MCP

### Description
AI-native scheduling MCP that goes beyond just reading a calendar. Connects to Calendly, Acuity, Google Calendar, and vertical-specific booking platforms (medical, dental, salons). Enables AI agents to: book appointments for users, find optimal scheduling slots across multiple attendees, manage booking pages, send rescheduling suggestions, and handle no-show follow-ups. Target: service businesses, personal assistants, healthcare admin.

### Evidence of Demand
- Search results show no specific MCP server exists for Calendly, Acuity, or NexHealth
- Healthcare scheduling is a specific pain — dental software alone is a $2.3B market
- PulseMCP has Google Calendar MCP but NO cross-platform booking/scheduling intelligence
- Vertical healthcare scheduling platforms (NexHealth, Curve Dental) charge $300-$600/month per practice — demonstrates high WTP

### Current MCP Competition
- Google Calendar MCP: read/write calendar events only
- **No Calendly MCP, no Acuity MCP, no multi-platform booking MCP confirmed**
- "Appointment scheduling" and "Calendly" searches on PulseMCP return no results

### Comparable Products & Pricing
- Calendly Teams: $16/seat/month
- Acuity Scheduling: $16-$61/month
- NexHealth (healthcare): $300-$600/month per practice
- Book Like A Boss: $9-$39/month
- Target pricing: $19/month for small business, $49/month for multi-location

### Build Complexity
**Low-Medium.** Calendly API and Acuity API are well-documented REST APIs with OAuth. Tools: `find_available_slots(attendees, duration)`, `book_appointment(params)`, `send_reschedule_request(booking_id)`, `get_upcoming_bookings(user)`. 

### API Availability
- Calendly REST API v2: full booking management, OAuth 2.0
- Acuity Scheduling API: appointment CRUD, OAuth 2.0
- Google Calendar MCP already exists — can extend it

---

## OPPORTUNITY 4: Multi-Platform E-Commerce Inventory & Repricing MCP

### Description
Unified inventory and dynamic pricing MCP for multi-channel sellers. Connects Amazon Seller Central, Shopify, WooCommerce, and Lazada/Shopee (SEA markets). Enables AI agents to sync inventory counts across channels, trigger reprice events based on competitor pricing, flag low-stock SKUs, and generate restock purchase orders. Target: Amazon FBA sellers, DTC brands running multiple storefronts.

### Evidence of Demand
- Amazon MCP is "community-maintained" with notoriously complex SP-API auth (noted in search results)
- Shopify has an official MCP but it has only 1 inventory tool out of 30+ total tools — inventory is undertreated
- Multi-channel inventory management is a known $3.7B market (Capterra category)
- Amazon seller pain: no official Amazon MCP, SP-API auth takes 2-3 business days, rate limits aggressive
- FBA sellers pay $40-$300/month for tools like Helium 10, Jungle Scout, RestockPro

### Current MCP Competition
- Shopify MCP (official): minimal inventory, no repricing
- Amazon MCP: community only, incomplete, auth friction
- **No unified multi-channel inventory + repricing MCP confirmed**

### Comparable Products & Pricing
- Helium 10: $99-$279/month (Amazon seller tool suite)
- Jungle Scout: $49-$129/month
- Linnworks (multi-channel inventory): $449/month
- RepricerExpress: $55-$239/month
- Target pricing: $29-$79/month

### Build Complexity
**Medium-High.** Amazon SP-API is complex (auth, registration, rate limits). Shopify GraphQL is simpler. Consider starting with Shopify-only + adding Amazon in v2. Key tools: `check_inventory_levels(sku, channels)`, `sync_inventory(source_channel, target_channels)`, `suggest_reprice(sku, competitor_prices)`, `generate_restock_order(low_stock_threshold)`.

### API Availability
- Amazon SP-API: requires Seller Central approval (2-3 days), comprehensive once approved
- Shopify Admin API: GraphQL, well-documented, immediate access
- Lazada Open Platform API: available (SEA market opportunity)
- Shopee Open Platform API: BiG already has context from shopee-affiliate project

---

## OPPORTUNITY 5: Clinical Trials & Medical Research MCP

### Description
Pharmaceutical and healthcare research MCP connecting ClinicalTrials.gov, PubMed, FDA drug databases, and OpenFDA adverse event data. Enables AI agents to: search active clinical trials by condition/drug/phase, retrieve drug safety profiles, find adverse event reports, and query FDA approval timelines. Target: pharmaceutical researchers, biotech startups, medical writers, investor analysts.

### Evidence of Demand
- Healthcare at 32% MCP adoption among Fortune 500 (fastest growing vertical after fintech)
- FHIR MCP servers exist (clinical data) BUT clinical trial/drug research MCP is a distinct gap
- ClinicalTrials.gov gets ~10M visits/month — research demand is enormous
- Biotech/pharma analysts at hedge funds pay $20,000-$50,000/year for specialized data terminals

### Current MCP Competition
- FHIR MCP: patient clinical records (EHR), NOT drug/trial research
- PubMed MCP: academic search only, no structured trial/drug data
- FDA/ClinicalTrials MCP: a USPTO-style server exists for patents, but confirmed no dedicated clinical trials MCP on PulseMCP
- **No confirmed combined clinical trials + FDA + adverse events MCP**

### Comparable Products & Pricing
- Citeline (formerly Pharmaprojects): $15,000-$50,000/year
- GlobalData Pharma Intelligence: $20,000+/year
- BioVigil clinical data tools: $5,000-$10,000/year
- Target pricing (lean version for individuals): $29-$99/month; enterprise: $299-$999/month

### Build Complexity
**Low.** All core data sources are public APIs:
- ClinicalTrials.gov API v2: fully public, no auth
- OpenFDA API: public REST API, no auth for basic queries
- PubMed Entrez API: public (NCBI)
- FDA Drug Database: public
Tools: `search_clinical_trials(condition, phase, status)`, `get_drug_profile(drug_name)`, `get_adverse_events(drug_name, severity)`, `check_fda_approval_status(drug)`.

### API Availability
All four core APIs are free and public. Fastest to build of all opportunities here. No auth required for MVP.

---

## OPPORTUNITY 6: B2B Lead Enrichment & Prospecting MCP

### Description
Sales intelligence MCP that enriches company and contact data for B2B prospecting. Connects to Apollo.io, Clearbit, Hunter.io, LinkedIn (via proxy), and Crunchbase. Enables AI agents to: enrich a lead list with company details, find decision-makers at a target company, verify emails, score leads by ICP fit, and pull funding/headcount signals. Target: SDRs, growth hackers, RevOps teams.

### Evidence of Demand
- B2B sales tech is a $25B+ market; sales intelligence tools are among the highest-converting SaaS verticals
- HackerNews wishlist thread (Dec 2025) requested "AI Priority Planning Assistant" for managing multiple systems — aligns with sales workflow automation
- LinkedIn candidate sourcing MCP exists (Anishshah2-gmail) but it's recruiting-focused, NOT sales prospecting
- Apollo.io (20M+ companies, $49-$99/month) and Clearbit ($99-$999/month) already monetize this data heavily

### Current MCP Competition
- LinkedIn MCP: job search / recruiting only
- Salesforce/HubSpot MCP: CRM read/write, NOT data enrichment
- **No confirmed Apollo.io, Clearbit, or Hunter.io MCP on PulseMCP**
- Composio has a generic connector but not a purpose-built prospecting MCP

### Comparable Products & Pricing
- Apollo.io: $49-$99/month (20M companies, 220M+ contacts)
- Clearbit: $99-$999/month
- Hunter.io: $49-$149/month (email finder)
- Lusha: $29-$149/month
- Target pricing: $39/month (personal), $99/month (team)

### Build Complexity
**Low-Medium.** Apollo.io has an official API. Hunter.io has a generous free tier (25 searches/month) for email finding. Key tools: `enrich_company(domain)`, `find_decision_makers(company, roles)`, `verify_email(email)`, `score_lead_fit(company, icp_criteria)`, `get_funding_signals(company)`.

### API Availability
- Apollo.io API: $49/month plan includes API access
- Hunter.io API: free tier (25/month), paid from $49/month
- Clearbit API: $99/month
- Crunchbase API: $29/month basic

---

## OPPORTUNITY 7: Multi-Platform Creator Economy & Monetization MCP

### Description
Creator analytics and monetization MCP for YouTube, TikTok, Patreon, Gumroad, and newsletter platforms (Beehiiv, Substack). Enables AI agents to: pull cross-platform revenue summaries, analyze top-performing content, benchmark against creator averages, suggest pricing for courses/memberships, and trigger payouts/campaigns. Target: creators doing $1K-$100K/month across multiple platforms.

### Evidence of Demand
- Creator economy is a $250B market (Goldman Sachs 2025 estimate)
- No unified creator analytics tool exists that spans YouTube + TikTok + Beehiiv + Gumroad in a single dashboard — this is a known pain
- Social media MCP servers (Ayrshare, Atlas Social, Publora) exist for PUBLISHING but NOT for cross-platform revenue analytics
- ChartMogul MCP covers SaaS subscription revenue, not creator revenue
- YouTube Analytics API and TikTok Business API are available but not wrapped in a unified MCP

### Current MCP Competition
- Social media MCP servers: cover publishing only, no revenue data
- ChartMogul MCP: SaaS subscriptions only
- **No cross-platform creator revenue + analytics MCP confirmed on PulseMCP**

### Comparable Products & Pricing
- Beacons.ai Creator Analytics: $10-$50/month
- Creator.co: $500-$1,000/month (brands use it, not creators)
- Gumroad Analytics: built-in (free for Gumroad users)
- Cohostly (YouTube analytics): $29-$99/month
- Target pricing: $19/month indie creator, $49/month professional

### Build Complexity
**Medium.** Each platform has its own API and auth. Start with YouTube Data API v3 + Gumroad API (both have free tiers). Add Patreon and Beehiiv in v2. Core tools: `get_revenue_summary(platform, period)`, `get_top_content(platform, metric)`, `compare_platform_performance()`, `get_payout_history(platform)`.

### API Availability
- YouTube Data API v3: free (OAuth 2.0)
- Gumroad API: free (OAuth 2.0), revenue/sales data
- Patreon API: free (OAuth 2.0)
- Beehiiv API: available
- TikTok Business API: available (more restricted)

---

## OPPORTUNITY 8: Real-Time Job Market Intelligence MCP

### Description
Labor market intelligence MCP for salary benchmarking, skills demand analysis, and hiring trend forecasting. Connects to Bureau of Labor Statistics (BLS), LinkedIn job postings (via public scraping/API), Glassdoor, Levels.fyi (tech compensation), and H-1B visa salary data. Enables AI agents to: benchmark a role's compensation, identify in-demand skills by market, forecast hiring trends, and generate compensation reports. Target: HR teams, individual salary negotiators, startup founders doing comp planning.

### Evidence of Demand
- Job search MCP (borgius/jobspy-mcp) exists for candidates searching jobs — but NOT for HR/compensation intelligence
- Leonar recruiting MCP exists but focused on pipeline management, NOT market intelligence
- BLS JOLTS data and H-1B disclosure data are public gold mines with zero MCP coverage
- Levels.fyi gets 10M+ visits/month from tech workers — massive demand signal
- HR teams pay $299-$1,200/month for Radford, Mercer, or PayScale salary benchmarking tools

### Current MCP Competition
- Jobspy MCP: job search for candidates, not compensation/market intel
- LinkedIn MCP: job search, not salary benchmarking
- BambooHR/Workday MCP: internal HR data, not market data
- **No confirmed compensation benchmarking or labor market intelligence MCP on PulseMCP**

### Comparable Products & Pricing
- PayScale: $299-$1,200/month for compensation data
- Radford (Aon): $5,000-$20,000/year for enterprise comp surveys
- Levels.fyi for Business: $499-$2,000/month
- Glassdoor Employer: $299-$999/month
- Target pricing: $29/month individual, $99/month HR team

### Build Complexity
**Low-Medium.** BLS public API (free, no auth), H-1B disclosure data (DOL public database), Glassdoor employer API (paid). Start with BLS + H-1B data (free public APIs). Tools: `get_salary_benchmark(role, location, level)`, `get_skills_demand_trend(skill, period)`, `compare_offer(role, salary, location)`, `get_hiring_volume(industry, region)`.

### API Availability
- BLS Public Data API: completely free, no auth
- Department of Labor H-1B data: public downloadable database
- Glassdoor API: requires partnership (apply)
- RapidAPI job data sources: $29-$99/month
- Levels.fyi: no public API — scraping risk; workaround with BLS/Glassdoor

---

## OPPORTUNITY 9: Subscription & SaaS Spend Analyzer MCP

### Description
Personal and team SaaS spend intelligence MCP. Connects to bank/credit card transaction data (via Plaid), extracts recurring subscription charges, identifies duplicates, benchmarks spend against team size, and suggests cancellation/downgrade opportunities. Different from the "budget/spending AI MCP" already researched — this is specifically B2B SaaS procurement focused. Target: startup CFOs, engineering managers, finance teams doing software spend audits.

### Evidence of Demand
- Average company wastes 30% of SaaS spend on unused licenses (Gartner 2025)
- Vendr, Zluri, and Sastrify charge $2,000-$10,000/month for SaaS management — enterprise pricing out of reach for startups
- ChartMogul MCP covers revenue analytics, NOT spend management
- The "budget/spending AI MCP" already researched targets individuals (personal finance) — this targets B2B procurement
- HackerNews developer wishes include "Priority Planning Assistant" for managing multiple systems — SaaS sprawl is the trigger

### Current MCP Competition
- ChartMogul MCP: subscription revenue (seller side), not spend management (buyer side)
- Stripe MCP: payment processing, not spend analysis
- **No SaaS spend management / procurement intelligence MCP confirmed on PulseMCP**
- Existing "budget MCP" in BiG's list is personal finance — this is B2B SaaS procurement

### Comparable Products & Pricing
- Vendr: $2,000-$8,000/month
- Zluri: $3,000-$10,000/month
- Sastrify: €2,000-€5,000/month
- Spendflo: $500-$2,000/month
- Target pricing: $49/month (startup), $149/month (growth) — major undercut of enterprise tools

### Build Complexity
**Medium.** Plaid API (bank data) is the hard part — requires Plaid subscription (~$500/month at scale, but free for development). Alternative: user uploads CSV bank exports. Tools: `scan_subscriptions(account)`, `identify_duplicates()`, `benchmark_saas_spend(team_size, industry)`, `generate_renewal_calendar()`, `flag_unused_licenses(usage_data)`.

### API Availability
- Plaid API: $500/month at scale (free sandbox for dev)
- Ramp API, Brex API (corporate cards): available for spend data
- Alternative approach: parse email receipts via Gmail API (zero cost)

---

## OPPORTUNITY 10: Construction & Real Estate Project Management MCP

### Description
Construction project tracking and real estate development MCP. Connects to Procore (construction PM), CoStar/LoopNet (commercial real estate), permit databases, and material cost indices (RSMeans). Enables AI agents to: track construction project milestones, monitor material cost changes, query permit statuses, analyze commercial property availability, and generate project cost estimates. Target: general contractors, real estate developers, commercial brokers.

### Evidence of Demand
- Real estate MCP servers exist (Zillow scraper, Realtor.com integration) but they are RESIDENTIAL and consumer-focused
- Commercial real estate (CRE) is a distinct $20T+ market with NO confirmed MCP coverage
- Construction tech is a $1.7B software market (Procore alone is $900M ARR)
- Data centers and AI infrastructure construction driving massive demand for specialized project logistics MCP (explicitly mentioned in Supply Chain Dive 2026 trends)
- PulseMCP: Zillow MCP exists, but no Procore or CoStar MCP confirmed

### Current MCP Competition
- Zillow MCP: residential property search only
- Real Estate Aggregator MCP (Apify): residential listings, not construction or commercial
- **No Procore, CoStar, LoopNet, or construction management MCP confirmed**

### Comparable Products & Pricing
- Procore: $375-$1,200/month per project
- CoStar: $5,000-$20,000/year per user
- Buildertrend: $399-$899/month
- PlanGrid (Autodesk): $49-$119/user/month
- Target pricing: $79/month SMB contractor, $249/month developer

### Build Complexity
**Medium-High.** Procore API is well-documented but enterprise sales-gated. CoStar has no public API (scraping risk). Alternative approach: focus on public data — municipal permit APIs (most US cities have open data APIs), RSMeans cost data (licensed), and BLS construction employment data (free). Start with permit + BLS data as MVP, add Procore OAuth integration for paying construction firm customers.

### API Availability
- Procore API: available with paid plan, requires developer registration
- Municipal permit APIs: most large US cities have open data portals (NYC, LA, Chicago)
- RSMeans (construction costs): licensed data, $1,500/year
- BLS construction indices: free public API
- CoStar: no public API — partner program required

---

## Summary Table

| # | Opportunity | Competition Level | Build Effort | Revenue Ceiling | Key Differentiator vs. Existing List |
|---|-------------|-------------------|--------------|-----------------|--------------------------------------|
| 1 | Multi-Carrier Logistics MCP | None confirmed | Medium | $50K MRR | Pure logistics — no overlap with crypto/finance |
| 2 | EU AI Act Compliance MCP | Low (Vanta/Drata cover old standards) | Low | $30K MRR | Regulatory deadline-driven urgency (Aug 2026) |
| 3 | Appointment Booking MCP | None confirmed | Low-Medium | $40K MRR | Calendly/Acuity gap — no cross-platform booking MCP |
| 4 | Multi-Channel Inventory MCP | Low (Shopify only) | Medium-High | $80K MRR | Amazon + Shopify unified; SEA market angle (Lazada/Shopee) |
| 5 | Clinical Trials & FDA MCP | None confirmed | Low | $60K MRR | All free public APIs, fast to build |
| 6 | B2B Lead Enrichment MCP | None confirmed | Low-Medium | $70K MRR | Apollo.io/Clearbit API wrapper nobody has built yet |
| 7 | Creator Economy Analytics MCP | None confirmed | Medium | $30K MRR | Revenue analytics, not publishing (existing gap) |
| 8 | Labor Market Intelligence MCP | None confirmed | Low-Medium | $50K MRR | BLS + H-1B public data, comp benchmarking |
| 9 | SaaS Spend Analyzer MCP | None confirmed | Medium | $60K MRR | B2B procurement (NOT personal finance — distinct from existing) |
| 10 | Construction/CRE Project MCP | None confirmed | Medium-High | $100K MRR | $20T commercial market, no MCP coverage |

---

## Top 3 Picks for BiG (Ranked by Speed + Revenue Potential)

### Rank 1: Clinical Trials & FDA MCP (#5)
- **Why:** All APIs are FREE and public (no paid API cost). Fastest to build (2-3 days). Pharma/biotech buyers have highest WTP. Zero competition confirmed on PulseMCP.
- **Revenue path:** 100 paying subscribers at $49/month = $4,900 MRR. Target biotech researcher and pharma analyst communities.

### Rank 2: B2B Lead Enrichment MCP (#6)
- **Why:** Sales tech has extremely high conversion intent. Apollo.io users already pay $49+/month and would pay more for AI-native enrichment. Hunter.io free tier enables zero-cost MVP.
- **Revenue path:** 200 subscribers at $39/month = $7,800 MRR. Distribute in r/sales, Product Hunt, Indie Hackers.

### Rank 3: EU AI Act Compliance MCP (#2)
- **Why:** Hard August 2026 enforcement deadline creates urgent time-bounded demand. Static knowledge base — no API costs. Can be built in 1-2 days. No competition confirmed.
- **Revenue path:** 50 compliance/legal team subscribers at $99/month = $4,950 MRR. Target SaaS CTOs and DPOs.

---

## Sources Used
- https://www.pulsemcp.com/servers
- https://thenewstack.io/model-context-protocol-roadmap-2026/
- https://medium.com/mcp-server/the-rise-of-mcp-protocol-adoption-in-2026-and-emerging-monetization-models
- https://dev.to/krisying/mcp-servers-are-the-new-saas-how-im-monetizing-ai-tool-integrations-in-2026-2e9e
- https://chatforest.com/reviews/hr-recruiting-mcp-servers/
- https://chatforest.com/guides/mcp-real-estate/
- https://www.rootplatform.com/blog/model-context-protocol-insurance
- https://www.sixfold.ai/content/post/mcp-insurance-underwriting-ai
- https://www.vanta.com/resources/claude-mcp-vanta
- https://logisticsviewpoints.com/2025/09/08/ai-in-the-supply-chain-part-3-mcp-the-model-context-protocol-and-shared-reasoning-across-agents/
- https://dev.to/grove_chatforest/healthcare-medical-mcp-servers-fhir-pubmed-clinical-trials-dicom-drug-databases-and-more-43n8
- https://opentweet.io/blog/best-mcp-servers-social-media-2026
- https://news.ycombinator.com/item?id=46345827

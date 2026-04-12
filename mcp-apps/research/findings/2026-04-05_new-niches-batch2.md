# MCP Server New Niche Research — Batch 2 (2026-04-05)

## Context
10 NEW MCP server product opportunities, completely distinct from the 20 already analyzed (see prompt). Global English-speaking market. Solo dev, <5 hours/week. Target $10–200/month subscriptions. Favors free/cheap APIs.

### Scoring Formula
**Opportunity Score = (API Availability + Willingness to Pay) - (Competition + Build Effort)**
- Competition: 1=zero MCP competition, 5=crowded
- API Availability: 5=multiple free/cheap APIs
- WTP: 5=users already paying $50+/mo for analogues
- Build Effort: 1=weekend, 5=months

---

## OPPORTUNITY 1: Sports & Betting Intelligence MCP

### One-Line Description
Multi-sport odds, player stats, and betting analytics MCP — connecting live odds from 40+ bookmakers with historical player/team performance data across NBA, NFL, EPL, and 17+ other leagues.

### Evidence of Demand
- The Odds API MCP (pulsemcp.com/servers/kitchenchem-sports-odds) exists but is a thin wrapper with minimal tools — real gap is **combining odds with stats context** for AI-driven line analysis
- BALLDONTLIE has an official MCP (pulsemcp.com/servers/balldontlie) — 200+ endpoints, 20 leagues — but it's stats-only, no odds
- Sports betting is a $100B+ global market (2026); prediction market volume growing rapidly (Kalshi, Polymarket institutional adoption)
- HackerNews threads on sports betting + AI: multiple requests for "LLM that can tell me if a line is sharp" (HN item 41659458)
- DraftKings, FanDuel, and Pinnacle bettors pay $99–$299/month for sharp-line tools (RebelBetting, OddsPortal Pro)
- API-Sports has 10M+ API calls/month — developer demand is real

### Current MCP Competition
- BALLDONTLIE MCP: stats only, no odds, no betting context — **confirmed on PulseMCP**
- The Odds API MCP: odds only, no stats, no combined analysis — **confirmed on PulseMCP**
- **No combined odds + stats + value-bet analysis MCP confirmed anywhere**
- Gap: neither server connects the two datasets; no server does line movement tracking or sharp money signals

### Comparable Paid Products & Pricing
- RebelBetting: $99–$189/month (value bet finder)
- OddsPortal Pro: $45/month
- SportsDataIO: $200–$500/month (enterprise)
- Betaminic: $49–$99/month (betting model builder)
- Pinnacle odds API: enterprise pricing

### Best Free/Cheap APIs
- **The Odds API**: free tier = 500 credits/month; paid from $30/month for historical data — covers 70+ sports, 40+ bookmakers
- **BALLDONTLIE**: free tier = 5 req/min across 20 leagues; ALL-STAR at $9.99/month; GOAT at $39.99/month
- **API-Sports**: free tier = 100 req/day; paid from $10/month — covers football (soccer), basketball, etc.
- Total API cost for MVP: ~$40–50/month

### Build Complexity
**2** — Two well-documented APIs with existing MCP wrappers as reference. Core tools: `get_odds(sport, market, bookmakers)`, `get_player_stats(player, season, splits)`, `analyze_line_value(event_id)`, `get_line_movement(event_id)`, `compare_bookmaker_margins()`. Weekend-scale for v1.

### Target Buyer & Distribution
- **Buyer**: Recreational sports bettors wanting AI-powered line analysis in Claude; fantasy sports players; prediction market traders
- **Distribution**: r/sportsbook (2.5M members), r/fantasyfootball, Discord betting servers, Product Hunt, X/Twitter sports analytics community

### Scores
| Metric | Score |
|--------|-------|
| Competition | 2 (two thin wrappers exist; no combined product) |
| API Availability | 5 (The Odds API + BALLDONTLIE = excellent free tiers) |
| Willingness to Pay | 4 (bettors pay $49–$189/month for analogues) |
| Build Effort | 2 (two documented REST APIs, reference code exists) |
| **Opportunity Score** | **(5+4) - (2+2) = +5** |

---

## OPPORTUNITY 2: Media Monitoring & Brand Mention Intelligence MCP

### One-Line Description
Real-time brand mention and media monitoring MCP — tracks a company or keyword across news, Reddit, X/Twitter, LinkedIn, Hacker News, and podcasts, returning sentiment-scored alerts and trend summaries.

### Evidence of Demand
- Octolens (B2B SaaS brand monitoring) explicitly launched MCP server support on all plans — confirms market demand and MCP viability; their cheapest plan with MCP access is $149/month
- Awario: $39–$399/month; BrandMentions: $49–$299/month — both lack MCP integration as of April 2026
- B2B founders consistently cite "knowing when competitors are mentioned" as top pain — r/SaaS, r/startups threads weekly
- Brand monitoring in 2026 generates $10B+ in SaaS revenue globally (Mention, Brandwatch, Sprinklr)
- Octolens review: "covers Reddit, X/Twitter, LinkedIn, GitHub, HN, YouTube, Bluesky, news, newsletters, podcasts" — shows scope of demand
- **No dedicated multi-platform brand monitoring MCP beyond Octolens' own native integration**

### Current MCP Competition
- Octolens: has native MCP server but it is **tied to Octolens subscription ($149+/month)** — not a standalone MCP
- NewsAPI aggregator MCP (PulseMCP): news headlines only, no brand tracking, no cross-platform social
- RSS MCP (PulseMCP): RSS feeds only, no sentiment, no social
- **No standalone brand monitoring MCP that wraps multiple free/cheap APIs** — confirmed gap

### Comparable Paid Products & Pricing
- Octolens Pro: $149/month (MCP included)
- Awario Pro: $119/month
- BrandMentions Growing: $79/month
- Mention Solo: $29/month (limited)
- Brandwatch: $1,000+/month (enterprise)

### Best Free/Cheap APIs
- **NewsData.io**: free tier = 200 req/day; paid from $49/month — covers 100+ countries, real-time news
- **Google News RSS**: completely free, unlimited
- **Reddit API (PRAW)**: free for read-only access — 60 req/min
- **Hacker News API (Algolia)**: completely free, full-text search
- **Mention API**: monitoring API, $29+/month base
- **X (Twitter) API Basic**: $100/month for 10K reads (cost risk — may limit margins)
- Strategy: Build MVP on NewsData + Google News + Reddit + HN (all free/cheap); offer X as premium add-on

### Build Complexity
**2** — Google News RSS + Reddit PRAW + HN Algolia API cover 80% of value with zero cost. Core tools: `monitor_brand(keyword, channels)`, `get_recent_mentions(keyword, since)`, `get_sentiment_summary(keyword, period)`, `set_alert_threshold(keyword, sentiment_score)`, `get_competitor_mentions(competitors)`. Simple polling + sentiment scoring.

### Target Buyer & Distribution
- **Buyer**: B2B SaaS founders, indie hackers, startup marketing teams — anyone who currently uses Awario/BrandMentions manually
- **Distribution**: r/SaaS, Indie Hackers, Product Hunt, B2B marketing communities, X/Twitter

### Scores
| Metric | Score |
|--------|-------|
| Competition | 2 (Octolens MCP is platform-locked; no standalone MCP) |
| API Availability | 5 (Google News + Reddit + HN all free; NewsData.io cheap) |
| Willingness to Pay | 4 (users pay $49–$149/month for existing tools) |
| Build Effort | 2 (RSS + REST APIs, no auth complexity for MVP) |
| **Opportunity Score** | **(5+4) - (2+2) = +5** |

---

## OPPORTUNITY 3: Visa & Travel Requirements Intelligence MCP

### One-Line Description
Visa requirements, entry rules, and travel restriction MCP — answers "Can I travel from [country A] to [country B] with [passport]?" with current visa-on-arrival, eVisa, vaccination, and document requirements.

### Evidence of Demand
- No dedicated visa/travel requirements MCP found on PulseMCP — only the Google Maps Travel Planner MCP mentions visa as a side feature, not primary
- Sherpa.io serves 200+ airlines and travel platforms with their Requirements API — proves enterprise-grade demand
- "Visa requirements" is one of the top 10 travel search queries globally (Google Trends consistent)
- Digital nomads, frequent business travelers, and immigration consultants all need this data — and current LLM responses are often outdated or wrong
- Travel and immigration communities (r/solotravel 2.1M, r/digitalnomad 2.3M) frequently request up-to-date visa info from AI tools
- Travel Buddy AI offers visa API with free tier — signals the data can be monetized

### Current MCP Competition
- Google Maps Travel Planner MCP (PulseMCP): mentions visa as one feature among 20+ — not dedicated, not reliable for complex routing
- **No standalone visa/entry requirements MCP confirmed on PulseMCP or Smithery**
- The Visa Acceptance MCP on PulseMCP is Visa the payment network, not visa entry requirements — common confusion

### Comparable Paid Products & Pricing
- Sherpa API: enterprise only (pricing not public, but used by Expedia, Booking.com, Lufthansa)
- VisaHQ Pro: $79–$299/month for business users
- iVisa B2B: $50–$150/month
- Immigration law firms: $300–$500/hour — shows WTP for accurate requirements
- Target pricing: $9/month personal (occasional traveler), $29/month professional (frequent travelers, immigration consultants)

### Best Free/Cheap APIs
- **Travel Buddy AI API** (travel-buddy.ai/api): free tier — 200+ passports, 210 destinations, visa + eVisa + eTA rules
- **VisaDB.io API**: real-time requirements, free tier available
- **Sherpa Requirements API**: requires partnership (apply at joinsherpa.com/api) — paid but comprehensive
- **Passport Index dataset**: GitHub, public, updated February 2026 — 199 countries, all visa categories
- MVP feasible on Travel Buddy free tier + Passport Index static dataset at zero API cost

### Build Complexity
**1** — Static dataset (Passport Index) covers 90% of queries. Dynamic layer via Travel Buddy API for real-time restrictions. Core tools: `check_visa_requirement(passport_country, destination_country)`, `get_entry_requirements(destination, passport)`, `get_evisa_links(destination)`, `check_vaccination_requirements(destination)`, `get_travel_restrictions(destination, date)`. True weekend project.

### Target Buyer & Distribution
- **Buyer**: Digital nomads, frequent business travelers, immigration consultants, travel agencies
- **Distribution**: r/digitalnomad, r/solotravel, Nomad List community, travel Facebook groups, Product Hunt

### Scores
| Metric | Score |
|--------|-------|
| Competition | 1 (zero standalone MCP confirmed) |
| API Availability | 5 (Passport Index free; Travel Buddy free tier; VisaDB free tier) |
| Willingness to Pay | 3 (consumers underpay, but immigration consultants and travel agencies pay) |
| Build Effort | 1 (static dataset + 1 REST API = true weekend project) |
| **Opportunity Score** | **(5+3) - (1+1) = +6** |

---

## OPPORTUNITY 4: Energy & Carbon Intelligence MCP

### One-Line Description
Energy price and carbon intensity MCP — queries live electricity prices by region, carbon grid intensity, renewable energy mix, and CO2 emission factors for cloud/travel/procurement activities.

### Evidence of Demand
- Energy-mcp-server exists (ecoailab on LobeHub/Glama) but is narrow: simulates energy systems for KEPCO (Korea) only — not a general-purpose tool
- Climatiq MCP (PulseMCP) covers carbon emissions calculations — confirms niche has traction
- EU Corporate Sustainability Reporting Directive (CSRD) mandates Scope 1/2/3 emissions reporting for 50,000+ companies starting 2026 — massive compliance driver
- "Carbon footprint of cloud computing" is a top query from DevOps teams in 2026
- Electricity Maps serves major enterprises (Google, Microsoft, AWS) for carbon-aware computing — proves high WTP
- No MCP combining real-time electricity prices + carbon intensity + EIA commodity data confirmed

### Current MCP Competition
- Climatiq MCP (PulseMCP): carbon calculations only, no electricity prices, no EIA data
- Energy-mcp-server (Glama): Korea-focused, simulation-oriented, not global real-time data
- Octopus Energy Japan MCP (PulseMCP): single utility, Japan only
- **No global energy price + carbon intensity + EIA MCP confirmed** — significant gap

### Comparable Paid Products & Pricing
- Electricity Maps API: starts at €500/month (commercial)
- Climatiq API: $49–$499/month
- WattTime API (carbon signal for demand response): $49–$199/month
- Urjanet (utility data): $500+/month enterprise
- Carbon accounting SaaS (Watershed, Persefoni): $30,000–$100,000/year enterprise

### Best Free/Cheap APIs
- **EIA Open Data API** (eia.gov/opendata): completely free, no auth — US electricity prices, generation mix, CO2 emissions, natural gas, petroleum
- **Electricity Maps free tier**: live carbon intensity for 200+ regions, personal/non-commercial use
- **Ember Energy API** (ember-energy.org/data/api): open access — annual/monthly electricity data for 200+ countries
- **Open-Meteo**: free solar/wind resource data (no API key needed)
- **Climatiq API**: free tier for carbon calculations
- Total API cost for MVP: $0 (all free tiers cover a functional product)

### Build Complexity
**2** — EIA API + Electricity Maps free tier cover the core use cases. Core tools: `get_electricity_price(region, timeframe)`, `get_carbon_intensity(region)`, `calculate_emission_factor(activity_type, amount, unit)`, `get_renewable_mix(region)`, `get_eia_commodity_price(commodity)`. Well-documented REST APIs.

### Target Buyer & Distribution
- **Buyer**: DevOps/platform engineers doing carbon-aware computing, sustainability managers, CSRD compliance teams, data center operators
- **Distribution**: HackerNews (green computing threads), r/devops, sustainability Slack communities, Product Hunt

### Scores
| Metric | Score |
|--------|-------|
| Competition | 2 (Climatiq MCP exists but narrow; no combined energy+carbon MCP) |
| API Availability | 5 (EIA free, Electricity Maps free tier, Ember free — $0 API cost for MVP) |
| Willingness to Pay | 4 (CSRD compliance buyers pay $30K+/year; individual DevOps teams pay $49–$199/month) |
| Build Effort | 2 (multiple free REST APIs, straightforward integration) |
| **Opportunity Score** | **(5+4) - (2+2) = +5** |

---

## OPPORTUNITY 5: Grant Discovery & Funding Intelligence MCP

### One-Line Description
Nonprofit and researcher grant discovery MCP — searches federal (Grants.gov), foundation (Candid/Foundation Directory), and private databases for funding opportunities matching an organization's mission, budget, and geography.

### Evidence of Demand
- No grant discovery MCP found anywhere on PulseMCP, Smithery, or mcpservers.org — confirmed zero competition
- Grants.gov processes $800B+ in federal grants annually; 40,000+ active opportunities at any time
- Instrumentl raised $55M from Summit Partners in 2026 to expand AI grant discovery — validates the market
- Grant writers charge $50–$150/hour; nonprofits pay Instrumentl $299–$499/month — strong WTP confirmed
- 1.5M+ nonprofits in the US alone, most understaffed, all need grant discovery
- Foundation Directory Online (Candid) charges $179/month for what is essentially a search interface — ripe for AI disruption
- Grants.gov has a completely free public API — zero data cost

### Current MCP Competition
- **None confirmed on PulseMCP, Smithery, or mcpservers.org** — searched "grant", "nonprofit", "foundation" — zero results
- Closest: US Legal MCP (Congress.gov) covers legislation but not grant funding
- This is a genuine white space

### Comparable Paid Products & Pricing
- Instrumentl: $299–$499/month
- Foundation Directory Online (Candid): $179/month
- GrantWatch: $49–$239/month
- GrantStation: $699/year (~$58/month)
- Amplify Grant Portal: custom enterprise pricing
- Target pricing: $29/month (small nonprofits), $79/month (grant consultants)

### Best Free/Cheap APIs
- **Grants.gov API** (grants.gov/web/grants/search-grants.html): completely free, no auth — all US federal grants, 40,000+ opportunities, keyword search, deadline filtering
- **USASpending.gov API**: completely free — historical award data, agency spending, recipient lookup
- **Candid/Foundation Directory**: $179/month subscription (required for foundation search — can be cost-passed to users)
- **SAM.gov API**: free — federal contracting and grant opportunities
- MVP is fully feasible on Grants.gov + USASpending.gov at $0 API cost. Foundation search requires Candid subscription or manual data.

### Build Complexity
**2** — Grants.gov REST API is well-documented and free. Core tools: `search_grants(keywords, cfda_number, agency, deadline_range)`, `get_grant_details(opportunity_id)`, `match_grants_to_mission(organization_description, budget_range)`, `get_federal_award_history(recipient, agency)`, `track_grant_deadline(opportunity_id)`. Weekend project for federal grants layer.

### Target Buyer & Distribution
- **Buyer**: Nonprofit grant writers, foundation relations officers, academic research administrators, government contractors
- **Distribution**: r/nonprofit, Foundation Center community, GrantProfessionals Association forums, Nonprofit Technology Conference (NTC), Product Hunt

### Scores
| Metric | Score |
|--------|-------|
| Competition | 1 (zero MCP competition confirmed) |
| API Availability | 4 (Grants.gov + USASpending free; Candid requires subscription) |
| Willingness to Pay | 4 (users pay $49–$499/month for existing tools) |
| Build Effort | 2 (Grants.gov API is simple and free) |
| **Opportunity Score** | **(4+4) - (1+2) = +5** |

---

## OPPORTUNITY 6: Wearable Health & Fitness Intelligence MCP

### One-Line Description
Unified wearable health MCP that queries Apple Health, Garmin Connect, Whoop, and Google Health Connect data — exposing steps, HRV, sleep stages, VO2max, strain scores, and nutrition logs to AI agents for personalized coaching.

### Evidence of Demand
- Apple Health MCP (the-momentum/apple-health-mcp-server on GitHub: 100+ stars) exists but is **local-only, requires manual XML export** — friction kills it for non-technical users
- Open Wearables v0.3 (Feb 2026) added MCP server support + Android/Google Health Connect — but it is a **self-hosted platform**, not a managed service
- Nori.ai HealthMCP: exists but no pricing transparency; appears limited to Apple Health
- Garmin MCP (github.com/Taxuspt/garmin_mcp): community project, incomplete, no Whoop/Polar
- Wearables market: $94B in 2025, growing to $120B by 2031 — massive user base with no polished AI integration
- ChatForest notes "100+ community wearable MCP servers" — but fragmented; no unified paid product

### Current MCP Competition
- Apple Health MCP (Momentum): local-only, no managed service version
- Garmin MCP (Taxuspt): community, incomplete
- Open Wearables MCP: self-hosted, requires technical setup
- Nori.ai HealthMCP: limited scope, unclear pricing
- **No polished, managed, multi-device health MCP with subscription billing confirmed** — the gap is productization

### Comparable Paid Products & Pricing
- Whoop membership: $30/month (device + platform)
- Training Peaks Premium: $19/month
- Garmin Connect Premium: $6/month
- MyFitnessPal Premium: $20/month
- Levels Health (CGM + metabolic): $199/month
- Target pricing: $12/month (basic wearable query), $29/month (multi-device + nutrition + AI coaching layer)

### Best Free/Cheap APIs
- **Apple HealthKit** (via Open Wearables open-source library): free for developers
- **Garmin Health API** (developer.garmin.com): free with partner registration
- **Google Health Connect API** (Android): free
- **Whoop API**: available to researchers and developers (free tier)
- **Open-source stack**: Open Wearables library handles all device normalization for free
- Total API cost: $0 — device APIs are free; monetize the managed service layer

### Build Complexity
**3** — Open Wearables open-source library handles the hard part (device normalization). Challenge is building the managed cloud sync (user data storage, OAuth per device, privacy compliance). Core tools: `get_activity_summary(device, date_range)`, `get_sleep_analysis(device, date_range)`, `get_hrv_trend(device, days)`, `get_strain_score(date)`, `log_nutrition(meal, macros)`. HIPAA-lite compliance needed if storing health data.

### Target Buyer & Distribution
- **Buyer**: Fitness-obsessed professionals, competitive athletes, biohackers, personal trainers who coach clients with wearable data
- **Distribution**: r/whoop, r/Garmin, r/QuantifiedSelf (161K members), fitness Twitter/X, Apple Health communities

### Scores
| Metric | Score |
|--------|-------|
| Competition | 3 (multiple partial solutions exist; polished managed product gap) |
| API Availability | 5 (all device APIs free; Open Wearables OSS handles normalization) |
| Willingness to Pay | 4 (users pay $6–$199/month for individual fitness apps) |
| Build Effort | 3 (OSS library helps; managed service infra is real work) |
| **Opportunity Score** | **(5+4) - (3+3) = +3** |

---

## OPPORTUNITY 7: Multi-Cloud Infrastructure Cost Optimizer MCP

### One-Line Description
Cross-cloud FinOps MCP that queries AWS Cost Explorer, GCP Billing, and Azure Cost Management to surface spending anomalies, right-sizing recommendations, and savings plan opportunities — then compares against current market pricing.

### Evidence of Demand
- AWS Cost Explorer MCP exists (PulseMCP: hteek-aws-cost-explorer, aws-official) — but AWS only; no GCP or Azure; no cross-cloud comparison
- AWS Billing and Cost Management MCP Server officially announced by AWS (2026) — validates market
- Average company wastes 32% of cloud spend (Gartner 2025); FinOps is a $500M+ SaaS market
- HackerNews threads on cloud cost management: hundreds of comments, high engagement; "cloud cost optimization" searches spiked 3x in 2025
- CloudHealth (VMware), Apptio Cloudability, Spot.io all charge $500–$5,000/month for multi-cloud FinOps

### Current MCP Competition
- AWS Cost Explorer MCP (hteek): AWS only — **confirmed on PulseMCP**
- AWS official Billing MCP (awslabs): AWS only, official but limited to AWS — **confirmed on PulseMCP**
- AWS Pricing MCP (awslabs): estimates only, no actual billing data — **confirmed**
- **No multi-cloud (AWS + GCP + Azure) combined FinOps MCP confirmed** — clear gap

### Comparable Paid Products & Pricing
- CloudHealth by VMware: $500–$2,000/month
- Apptio Cloudability: $1,000–$5,000/month
- Spot.io (NetApp): $500–$2,000/month
- Infracost (open source + cloud): $50–$500/month
- Target pricing: $49/month startup (AWS-only), $99/month (multi-cloud)

### Best Free/Cheap APIs
- **AWS Cost Explorer API**: $0.01/request (negligible); free with AWS account
- **GCP Cloud Billing API**: free with GCP account; OAuth via service account
- **Azure Cost Management API**: free with Azure subscription
- **AWS Compute Optimizer API**: free
- Total API cost for MVP: ~$1–5/month (Cost Explorer API calls), everything else free

### Build Complexity
**3** — AWS is well-documented (reference code exists). GCP and Azure billing APIs are straightforward but require multi-tenant OAuth setup. Core tools: `get_cost_summary(provider, account, period)`, `find_cost_anomalies(provider, threshold)`, `get_rightsizing_recommendations(provider)`, `compare_reserved_vs_ondemand(provider, service)`, `estimate_savings_plan_impact(provider)`. Real challenge is multi-tenant credential management.

### Target Buyer & Distribution
- **Buyer**: DevOps engineers, platform engineers, startup CTOs and CFOs, FinOps practitioners
- **Distribution**: r/devops, r/aws, HackerNews, FinOps Foundation community (finops.org), CloudHealth/Infracost alternative seekers

### Scores
| Metric | Score |
|--------|-------|
| Competition | 2 (AWS-only MCPs exist; no multi-cloud confirmed) |
| API Availability | 5 (all three cloud billing APIs are free with account credentials) |
| Willingness to Pay | 4 (companies pay $500–$5,000/month for FinOps tools; even $49/month is compelling for startups) |
| Build Effort | 3 (multi-tenant OAuth + 3 cloud APIs = real complexity) |
| **Opportunity Score** | **(5+4) - (2+3) = +4** |

---

## OPPORTUNITY 8: Academic & Scientific Literature Intelligence MCP

### One-Line Description
Unified academic research MCP aggregating Semantic Scholar, arXiv, PubMed, CrossRef, and OpenAlex — enabling AI agents to search papers, trace citation networks, find related researchers, and generate literature review summaries.

### Evidence of Demand
- Academic Paper Search MCP (afrise, PulseMCP) exists — Semantic Scholar + CrossRef only — **confirmed but narrow**
- Academix (GitHub: xingyulu23) aggregates 5 sources (OpenAlex, DBLP, Semantic Scholar, arXiv, CrossRef) — **open source, no managed service**
- 200M+ academic papers in OpenAlex; 100M+ in Semantic Scholar — enormous search volume
- Researchers, PhD students, biotech analysts, and journalists all use academic search heavily
- Existing tools (Elsevier SciVal: $5,000+/year; Web of Science: $1,000+/year; Scite.ai: $20/month) are expensive or limited
- No paid managed MCP service with multi-source aggregation + citation network analysis confirmed

### Current MCP Competition
- Academic Paper Search MCP (afrise): Semantic Scholar + CrossRef only, no citation network, no PubMed — **confirmed on PulseMCP**
- Semantic Scholar MCP (two versions on PulseMCP): single-source, no aggregation
- Academix: open source self-hosted, no managed product
- **No unified, managed, multi-source academic MCP with citation analysis confirmed**
- Gap: nobody has productized the Academix aggregation concept with billing

### Comparable Paid Products & Pricing
- Scite.ai: $20/month (citation context analysis)
- Elsevier SciVal: $5,000+/year
- Web of Science: $1,000+/year
- Research Rabbit: free (VC-funded, unsustainable)
- Connected Papers: $6/month (visual citation mapping)
- Target pricing: $15/month researcher, $49/month team/institutional

### Best Free/Cheap APIs
- **OpenAlex API** (openalex.org): completely free, 100K+ calls/day — 200M+ works, citations, authors, institutions
- **Semantic Scholar API**: free, 100 req/sec with key — AI-powered recommendations
- **arXiv API**: completely free, unlimited — 2M+ preprints
- **PubMed Entrez API (NCBI)**: completely free — 34M+ biomedical papers
- **CrossRef API**: completely free — DOI resolution, metadata for 130M+ works
- **DBLP API**: completely free — CS-focused
- Total API cost for MVP: $0 — all sources are free

### Build Complexity
**2** — All APIs are free and well-documented. Academix open-source code exists as reference. Core tools: `search_papers(query, sources, date_range)`, `get_citation_network(paper_id, depth)`, `find_related_papers(paper_id)`, `get_author_profile(name_or_id)`, `summarize_literature(topic, date_range)`. Main challenge: deduplication across sources and response size management (25K token limit).

### Target Buyer & Distribution
- **Buyer**: PhD students, academic researchers, biotech/pharma analysts, science journalists, competitive intelligence analysts
- **Distribution**: r/academia, r/MachineLearning, r/PhD, biotech Slack communities, Research Gate, Twitter/X academic communities (#AcademicChatter)

### Scores
| Metric | Score |
|--------|-------|
| Competition | 2 (partial MCPs exist; no managed multi-source product) |
| API Availability | 5 (all sources completely free, no API cost at all) |
| Willingness to Pay | 3 (academics underpay; biotech analysts pay well; indie pricing harder) |
| Build Effort | 2 (all free documented APIs + OSS reference code) |
| **Opportunity Score** | **(5+3) - (2+2) = +4** |

---

## OPPORTUNITY 9: Security Vulnerability & CVE Intelligence MCP

### One-Line Description
Threat intelligence MCP that queries NVD/CVE databases, CISA KEV catalog, EPSS exploit probability scores, and GitHub Advisory Database — enabling AI agents to assess patch urgency, search vulnerabilities by product, and generate remediation checklists.

### Evidence of Demand
- NVD (National Vulnerability Database) MCP by Marco Graziano exists on PulseMCP — but it is NVD only, no EPSS, no CISA KEV, no exploitability context
- CVE-Search MCP (roadwy) on PulseMCP — single-source CVE search only
- 30+ CVEs filed against MCP servers themselves in Q1 2026 (HackerNews: MCP Security 2026 — 30 CVEs in 60 Days) — security teams are actively watching this space
- 82% of MCP implementations have path traversal vulnerabilities (survey of 2,614 MCP servers) — security demand is urgent
- Snyk, Sonatype, and Tenable charge $49–$500/month for vulnerability management
- DevSecOps teams at every company need vulnerability triage — this is a universal workflow

### Current MCP Competition
- NVD MCP (marcoeg, PulseMCP): NVD search only — **confirmed**
- CVE-Search MCP (roadwy, PulseMCP): CVE search only — **confirmed**
- **No MCP combining NVD + EPSS + CISA KEV + GitHub Advisory + OSV confirmed** — gap is contextual prioritization
- Gap: existing MCPs answer "what is CVE-X?" but not "should I patch this today or next week?"

### Comparable Paid Products & Pricing
- Snyk: $49–$99/month developer tier
- Tenable.io: $2,500+/year
- Qualys VMDR: $3,000+/year
- VulnDB (Risk Based Security): $2,000+/year
- GreyNoise: $99/month
- Target pricing: $19/month (developer), $49/month (security team)

### Best Free/Cheap APIs
- **NVD API v2** (nvd.nist.gov/developers): completely free, 50 req/30sec (with API key) — full CVE database
- **CISA KEV Catalog API**: completely free — actively exploited vulnerabilities catalog
- **EPSS API** (first.org/epss): completely free — exploit probability scoring for all CVEs
- **GitHub Advisory Database API** (graphql.github.com): free with GitHub token
- **OSV API** (osv.dev): completely free — unified open source vulnerability data
- Total API cost for MVP: $0 — all five sources are free

### Build Complexity
**2** — Five free APIs, all well-documented. Core tools: `search_vulnerabilities(product, version, severity)`, `get_cve_details(cve_id)`, `get_exploit_probability(cve_id)`, `check_if_actively_exploited(cve_id)`, `generate_patch_priority_list(product_list)`, `get_affected_packages(cve_id)`. Main challenge: combining EPSS + KEV data for prioritization logic.

### Target Buyer & Distribution
- **Buyer**: DevSecOps engineers, security analysts, platform engineers doing dependency audits, CISO teams at SMBs
- **Distribution**: r/netsec (400K members), r/devops, HackerNews, DevSecOps Slack communities, OWASP community, security-focused newsletters (tl;dr sec)

### Scores
| Metric | Score |
|--------|-------|
| Competition | 2 (single-source MCPs exist; no combined contextual prioritization MCP) |
| API Availability | 5 (NVD + CISA + EPSS + GitHub + OSV all completely free) |
| Willingness to Pay | 4 (security teams pay $49–$500/month for Snyk/Tenable) |
| Build Effort | 2 (five free documented APIs, clear tool structure) |
| **Opportunity Score** | **(5+4) - (2+2) = +5** |

---

## OPPORTUNITY 10: Patent Search & IP Intelligence MCP

### One-Line Description
Patent research MCP combining USPTO, Google Patents, and EPO databases — enabling AI agents to search prior art, check freedom-to-operate, track competitor patent filings, and analyze patent landscapes for a technology area.

### Evidence of Demand
- patent_mcp_server (riemannzeta, PulseMCP/LobeHub) exists — USPTO only, focuses on prosecution history and PTAB proceedings
- patents-mcp (openpharma-org, GitHub) exists — USPTO + Google Patents, open source but no managed service
- Patent Connector (patent.dev) — a dedicated commercial MCP product launched, charging for AI-powered patent research
- Patent attorneys charge $300–$500/hour for prior art searches; IP firms pay $20,000+/year for Derwent Innovation
- 10M+ patent filings globally per year; startup founders, R&D teams, and law firms all need this
- PatentsView API was shut down March 20, 2026 — created a data gap that the new USPTO ODP fills, but no polished MCP wraps it yet

### Current MCP Competition
- patent_mcp_server (riemannzeta): USPTO prosecution/PTAB focus, not prior art search or competitor tracking — **confirmed on PulseMCP**
- patents-mcp (openpharma-org): open source, no managed product, requires self-hosting — **confirmed on GitHub**
- patent-mcp-server (PyPI): open source, unclear maintenance status
- Patent Connector (patent.dev): commercial product exists — **this is the main competitor to assess**
- **Gap remains**: competitor patent filing tracking, cross-jurisdiction search (USPTO + EPO + WIPO), landscape analysis

### Comparable Paid Products & Pricing
- Derwent Innovation (Clarivate): $20,000+/year
- PatSnap: $5,000–$20,000/year
- Lens.org: free for basic, $100+/month for bulk access
- Patent Connector MCP: pricing not public (developer preview)
- LexisNexis PatentOptimizer: $2,000+/year
- Target pricing: $29/month (startup/indie researcher), $149/month (IP law firm team)

### Best Free/Cheap APIs
- **USPTO Open Data Portal API** (data.uspto.gov): free with API key — patent file wrappers, assignments, PTAB, litigation
- **USPTO Patent Public Search API**: free, no key required — full-text search
- **Google Patents via Lens.org**: free for basic access
- **EPO OPS API** (ops.epo.org): free tier = 4,000 req/day — European patent search
- **WIPO PATENTSCOPE API**: free — international PCT applications
- Total API cost for MVP: $0 — USPTO + EPO + WIPO all have free tiers

### Build Complexity
**3** — USPTO ODP is new (April 2026) and documentation is in flux; PatentsView was just shut down. EPO OPS API has quirky XML responses. Core tools: `search_prior_art(claims_text, cpc_class, date_range)`, `get_patent_details(patent_number)`, `track_competitor_filings(assignee_name, date_range)`, `check_freedom_to_operate(technology_description)`, `get_patent_landscape(technology_area)`. Complexity is in parsing patent XML and building useful prior art ranking.

### Target Buyer & Distribution
- **Buyer**: Startup founders doing patentability checks, R&D engineers, IP paralegals, patent attorneys (efficiency tool), biotech/medtech firms
- **Distribution**: r/patents, r/legaladvice (for outreach, not solicitation), IP law firm communities, startup accelerator networks (YC alumni, Techstars), LinkedIn IP professional groups

### Scores
| Metric | Score |
|--------|-------|
| Competition | 3 (open-source MCPs + Patent Connector commercial exist; no full-feature managed product confirmed) |
| API Availability | 4 (USPTO + EPO + WIPO all free; some XML parsing friction) |
| Willingness to Pay | 5 (IP firms pay $2,000–$20,000+/year for existing tools; even $29/month is a steal) |
| Build Effort | 3 (multiple APIs with XML, new USPTO ODP in flux) |
| **Opportunity Score** | **(4+5) - (3+3) = +3** |

---

## Master Summary Table

| # | Product Name | Comp | API | WTP | Build | **Score** | Best Angle |
|---|-------------|------|-----|-----|-------|-----------|------------|
| 3 | Visa & Travel Requirements MCP | 1 | 5 | 3 | 1 | **+6** | Zero competition, weekend build, global demand |
| 1 | Sports & Betting Intelligence MCP | 2 | 5 | 4 | 2 | **+5** | Combine two thin existing MCPs into one premium product |
| 2 | Media Monitoring & Brand Mention MCP | 2 | 5 | 4 | 2 | **+5** | Standalone alternative to $149/month Octolens |
| 4 | Energy & Carbon Intelligence MCP | 2 | 5 | 4 | 2 | **+5** | CSRD compliance demand, $0 API cost |
| 5 | Grant Discovery & Funding MCP | 1 | 4 | 4 | 2 | **+5** | Zero competition, $0 Grants.gov API, Instrumentl $55M raise validates market |
| 9 | CVE & Security Intelligence MCP | 2 | 5 | 4 | 2 | **+5** | All 5 APIs free, security teams already pay $49-$500/month |
| 7 | Multi-Cloud FinOps MCP | 2 | 5 | 4 | 3 | **+4** | AWS MCPs exist but no multi-cloud; FinOps market is $500M+ |
| 8 | Academic Literature Intelligence MCP | 2 | 5 | 3 | 2 | **+4** | All APIs free, but WTP limited to biotech/pharma angle |
| 6 | Wearable Health & Fitness MCP | 3 | 5 | 4 | 3 | **+3** | OSS lib exists; productization gap; health data privacy risk |
| 10 | Patent Search & IP Intelligence MCP | 3 | 4 | 5 | 3 | **+3** | Highest WTP ceiling; most competition; hardest APIs |

---

## Top 3 Picks for BiG (Ranked by Speed + Fit)

### Rank 1: Visa & Travel Requirements MCP (+6)
- **Why:** True weekend build. Passport Index dataset (GitHub, free) covers 90% of queries. Zero MCP competition. 4M+ combined readers in r/digitalnomad + r/solotravel. First-mover wins.
- **Risk:** WTP is lower on consumer side — price at $9/month personal, $29/month for immigration consultants/travel agents. Upsell with Sherpa enterprise API for real-time restrictions.
- **Revenue path:** 300 subscribers at $9/month = $2,700 MRR. 50 professional at $29 = $1,450. Total: $4,150 MRR.

### Rank 2: CVE & Security Intelligence MCP (+5)
- **Why:** All five APIs are free ($0 cost forever). Security teams already pay for Snyk/Tenable. 30+ CVEs in MCP servers themselves means security is top of mind in the MCP community — perfect distribution fit. Differentiation over existing single-source MCPs is clear (EPSS + KEV prioritization).
- **Revenue path:** 200 developers at $19/month = $3,800 MRR. 50 security teams at $49/month = $2,450. Total: $6,250 MRR.

### Rank 3: Grant Discovery & Funding MCP (+5)
- **Why:** Zero competition anywhere. Grants.gov API is free and simple. Instrumentl's $55M raise proves 2026 is the year grant tech gets funded — right timing. Grant writers are professional buyers with clear budgets.
- **Revenue path:** 100 nonprofits at $29/month = $2,900 MRR. 50 grant consultants at $79/month = $3,950. Total: $6,850 MRR.

---

## Sources
- https://www.pulsemcp.com/servers/kitchenchem-sports-odds
- https://www.pulsemcp.com/servers/balldontlie
- https://www.balldontlie.io/
- https://the-odds-api.com/
- https://octolens.com/pricing
- https://awario.com/pricing/
- https://www.saasworthy.com/product/brandmentions/pricing
- https://travel-buddy.ai/api/
- https://github.com/ilyankou/passport-index-dataset
- https://www.joinsherpa.com/solutions
- https://www.electricitymaps.com/free-tier-api
- https://www.eia.gov/opendata/
- https://ember-energy.org/data/api/
- https://www.pulsemcp.com/servers/jagan-shanmugam-climatiq
- https://www.instrumentl.com/pricing
- https://github.com/xingyulu23/Academix
- https://www.pulsemcp.com/servers/afrise-academic-search
- https://www.pulsemcp.com/servers/marcoeg-nvd
- https://www.pulsemcp.com/servers/roadwy-cve-search
- https://nvd.nist.gov/
- https://www.first.org/epss/
- https://github.com/riemannzeta/patent_mcp_server
- https://github.com/openpharma-org/patents-mcp
- https://patent.dev/patent-connector-mcp-server-for-ai-powered-patent-research/
- https://data.uspto.gov/apis/patent-file-wrapper/search
- https://www.pulsemcp.com/servers/hteek-aws-cost-explorer
- https://aws.amazon.com/blogs/aws-cloud-financial-management/aws-announces-billing-and-cost-management-mcp-server/
- https://www.themomentum.ai/blog/open-wearables-0-3-alpha-flutter-sdk-for-apple-health-and-mcp-server-now-available
- https://nori.ai/health-mcp
- https://news.ycombinator.com/item?id=47356600

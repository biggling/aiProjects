# POD Automation Dataflow Diagram

---

## Pipeline Overview

```mermaid
graph TD
    P1[Phase 1 Trend Research] --> P2[Phase 2 AI Design Pipeline]
    P2 --> P3[Phase 3 AI Copywriting]
    P3 --> P4[Phase 4 Upload and Automation]
    P4 --> P5[Phase 5 Analytics]
    P5 -->|weekly recommendations| P1
    BEAT[Celery Beat 19 scheduled tasks] -->|crontab triggers| P1
    BEAT -->|crontab triggers| P2
    BEAT -->|crontab triggers| P3
    BEAT -->|crontab triggers| P4
    BEAT -->|crontab triggers| P5
    DASH[FastAPI Dashboard] -->|send_task| REDIS[(Redis broker)]
    REDIS -->|dispatch| WORKER[Celery Worker]
    WORKER -->|run| P1
    WORKER -->|run| P2
    WORKER -->|run| P3
    WORKER -->|run| P4
    WORKER -->|run| P5
    WORKER -->|writes| TLOG[task_logs table]
    DASH -->|reads| TLOG
```

---

## Phase 1 Trend Research

Mon / Wed / Fri 00:00 to 01:00 UTC

```mermaid
graph LR
    subgraph EXT1 [External Sources]
        GT[Google Trends pytrends]
        RD[Reddit praw]
        EP[Etsy Playwright]
    end

    subgraph TOOLS1 [Phase 1 Tools]
        TS[trend_scraper.py]
        RS[reddit_scraper.py]
        ES[etsy_scraper.py]
        NS[niche_scorer.py]
    end

    subgraph WRITE1 [niches table writes]
        W1A[keyword]
        W1B[trend_score avg of 90d values]
        W1C[velocity recent vs older avg]
        W1D[competition sales density 0 to 1]
        W1E[final_score = trend x vel div comp normalized 0-100]
        W1F[status = killed if final_score lt 10]
    end

    GT -->|interest_over_time 90d<br>related_queries rising| TS
    RD -->|rising posts r/Etsy r/printondemand| RS
    RS -->|Claude extracts keywords| RS
    EP -->|bestseller page titles + sales| ES

    TS --> W1A
    TS --> W1B
    TS --> W1C
    RS --> W1C
    ES --> W1D
    W1B --> NS
    W1C --> NS
    W1D --> NS
    NS --> W1E
    NS --> W1F
```

**Log:** `data/logs/trend_scraper.log`, `data/logs/reddit_scraper.log`, `data/logs/etsy_scraper.log`, `data/logs/niche_scorer.log`

---

## Phase 2 AI Design Pipeline

Mon / Wed / Fri 02:00 to 09:30 UTC

```mermaid
graph LR
    subgraph READ2 [Reads from DB]
        R2A[niches WHERE status=active ORDER BY final_score DESC LIMIT 10]
        R2B[prompts WHERE status=pending LIMIT 20]
        R2C[designs WHERE status=generated]
        R2D[designs WHERE status=processed]
        R2E[designs WHERE status=approved AND mockup_path IS NULL]
    end

    subgraph TOOLS2 [Phase 2 Tools]
        PG[prompt_generator.py]
        IG[image_generator.py]
        IP[image_processor.py]
        CF[clip_filter.py]
        MG[mockup_generator.py]
    end

    subgraph WRITE2 [Writes]
        W2A[prompts table: prompt_text status=pending]
        W2B[designs table: raw_path status=generated]
        W2C[designs table: processed_path status=processed]
        W2D[designs table: clip_score status=approved or rejected]
        W2E[designs table: mockup_path status=mockup_ready]
    end

    subgraph FILES2 [File Paths]
        F2A[data/designs/raw/niche_id/prompt_id.png]
        F2B[data/designs/processed/design_id.png 4500x5400]
        F2C[data/designs/mockups/design_id.png]
    end

    subgraph APIS2 [External APIs]
        CLA[Claude API 50 prompts per niche]
        SDAI[Stability AI SDXL-1024 or DALL-E 3]
        CLIPM[CLIP ViT-B/32 local cosine similarity]
        PAPI[Printify Mockup API blueprint 5]
    end

    R2A --> PG
    CLA --> PG
    PG --> W2A
    R2B --> IG
    SDAI --> IG
    IG --> W2B
    IG --> F2A
    R2C --> IP
    IP --> W2C
    IP --> F2B
    R2D --> CF
    CLIPM --> CF
    CF --> W2D
    R2E --> MG
    PAPI --> MG
    MG --> W2E
    MG --> F2C
```

**Log:** `data/logs/prompt_gen.log`, `data/logs/image_gen.log`, `data/logs/image_processor.log`, `data/logs/clip_filter.log`, `data/logs/mockup_gen.log`

---

## Phase 3 AI Copywriting

Mon / Wed / Fri / Sat 10:00 to 11:00 UTC

```mermaid
graph LR
    subgraph READ3 [Reads from DB]
        R3A[designs WHERE status=mockup_ready joins niches for keyword]
        R3B[listings WHERE title IS NOT NULL AND caption IS NULL]
    end

    subgraph TOOLS3 [Phase 3 Tools]
        CG[copy_generator.py]
        CAP[caption_generator.py]
    end

    subgraph WRITE3 [listings table writes]
        W3A[title max 140 chars front-loaded keywords]
        W3B[description 800 chars 5 bullet points]
        W3C[tags JSON array of 13 strings]
        W3D[status = copy_ready]
        W3E[caption max 200 chars with 3-5 hashtags]
    end

    CLA[Claude API] --> CG
    CLA --> CAP
    R3A --> CG
    CG --> W3A
    CG --> W3B
    CG --> W3C
    CG --> W3D
    R3B --> CAP
    CAP --> W3E
```

**Log:** `data/logs/copy_gen.log`, `data/logs/caption_gen.log`

---

## Phase 4 Upload and Automation

Mon to Sat 13:00 to 16:00 UTC

```mermaid
graph LR
    subgraph READ4 [Reads from DB]
        R4A[listings WHERE status=copy_ready AND printify_product_id IS NULL]
        R4B[listings WHERE printify_product_id IS NOT NULL AND etsy_listing_id IS NULL]
        R4C[listings WHERE status=live AND social_posted IS NULL LIMIT 5]
        R4D[listings WHERE status=live for price comparison]
    end

    subgraph TOOLS4 [Phase 4 Tools]
        PP[printify_publisher.py]
        EU[etsy_uploader.py]
        OR[order_router.py FastAPI webhook]
        SP[social_poster.py]
        PA[price_adjuster.py]
    end

    subgraph WRITE4 [listings table writes]
        W4A[printify_product_id]
        W4B[etsy_listing_id]
        W4C[status = live]
        W4D[uploaded_at]
        W4E[social_posted timestamp]
    end

    subgraph APIS4 [External APIs]
        PAPI[Printify POST /v1/shops/products blueprint 5 provider 29]
        EAPI[Etsy POST /v3/application/listings state=active]
        EORD[Etsy order webhook POST /webhook/etsy-order]
        BUF[Buffer API mockup image + caption]
        EPL[Etsy Playwright top 20 results per niche]
    end

    subgraph FILES4 [File Reads]
        F4A[data/designs/processed/design_id.png sent to Printify]
        F4B[data/designs/mockups/design_id.png sent to Etsy]
        F4C[data/logs/price_report_date.txt written by price_adjuster]
    end

    R4A --> PP
    F4A --> PP
    PP --> PAPI
    PP --> W4A

    R4B --> EU
    F4B --> EU
    EU --> EAPI
    EU --> W4B
    EU --> W4C
    EU --> W4D

    EORD --> OR
    OR --> PAPI

    R4C --> SP
    SP --> BUF
    SP --> W4E

    R4D --> PA
    EPL --> PA
    PA --> F4C
```

**Log:** `data/logs/printify_publish.log`, `data/logs/etsy_uploader.log`, `data/logs/social_post.log`, `data/logs/price_check.log`

---

## Phase 5 Analytics

Daily 20:00 UTC / Friday 20:00 UTC

```mermaid
graph LR
    subgraph READ5 [Reads from DB]
        R5A[listings WHERE etsy_listing_id IS NOT NULL]
        R5B[listings WHERE uploaded_at lt now minus 7 days]
        R5C[listings + niches joined for weekly totals]
    end

    subgraph TOOLS5 [Phase 5 Tools]
        AP[analytics_puller.py]
        PF[performance_flagger.py]
        WR[weekly_report.py Friday only]
    end

    subgraph WRITE5 [listings table writes]
        W5A[views]
        W5B[favorites]
        W5C[sales]
        W5D[revenue]
        W5E[status = underperforming if views lt 50 AND favorites lt 3]
    end

    subgraph FILES5 [File Writes]
        F5A[data/logs/report_YYYY-MM-DD.md]
    end

    EAPI[Etsy GET /v3/application/listings/id/stats] --> AP
    R5A --> AP
    AP --> W5A
    AP --> W5B
    AP --> W5C
    AP --> W5D

    R5B --> PF
    PF --> W5E
    PF -->|Apprise| TG[Telegram notification]

    R5C --> WR
    CLA[Claude API summary + recommendations] --> WR
    WR --> F5A
    WR -->|Apprise| TG
```

**Log:** `data/logs/analytics_pull.log`, `data/logs/performance_flag.log`, `data/logs/weekly_report.log`

---

## Design and Listing Status Lifecycles

```mermaid
graph LR
    subgraph DSM [designs.status]
        D1[pending] --> D2[generated]
        D2 --> D3[processed]
        D3 -->|clip_score gte 0.20| D4[approved]
        D3 -->|clip_score lt 0.20| D5[rejected]
        D4 --> D6[mockup_ready]
    end

    subgraph LSM [listings.status]
        L1[pending] --> L2[copy_ready]
        L2 --> L3[uploaded]
        L3 --> L4[live]
        L4 -->|7d low stats| L5[underperforming]
        L4 -->|human action| L6[paused]
    end
```

---

## Daily Schedule UTC

```mermaid
gantt
    title Automation Schedule Mon Wed Fri
    dateFormat HH:mm
    axisFormat %H:%M

    section Phase 1 Trend
    trend_scraper          :00:00, 30m
    reddit_scraper         :00:30, 30m
    niche_scorer           :01:00, 30m

    section Phase 2 Design
    prompt_generator       :02:00, 60m
    image_generator        :03:00, 180m
    image_processor        :06:00, 60m
    clip_filter            :07:00, 60m
    etsy_scraper daily     :09:00, 30m
    mockup_generator       :09:30, 30m

    section Phase 3 Copy
    copy_generator         :10:00, 60m
    caption_generator      :11:00, 30m

    section Phase 4 Upload
    printify_publisher     :13:00, 60m
    etsy_uploader          :14:00, 60m
    social_poster          :16:00, 30m

    section Phase 5 Analytics
    analytics_puller       :20:00, 30m
    performance_flagger    :20:30, 15m
    weekly_report Fri only :20:00, 30m

    section Maintenance
    price_check            :22:00, 30m
    backup Sun only        :22:30, 15m
```

---

## Data Artifacts per Phase

| Phase | Tool | Reads | Writes DB | Writes Files |
|-------|------|-------|-----------|--------------|
| 1.1 | trend_scraper | `config.SEED_KEYWORDS` | `niches.keyword` `niches.trend_score` `niches.velocity` | `data/logs/trend_scraper.log` |
| 1.2 | reddit_scraper | Reddit API | `niches.velocity` | `data/logs/reddit_scraper.log` |
| 1.3 | etsy_scraper | Etsy bestseller pages | `niches.competition` | `data/logs/etsy_scraper.log` |
| 1.4 | niche_scorer | `niches` all rows | `niches.final_score` `niches.status` | `data/logs/niche_scorer.log` |
| 2.1 | prompt_generator | `niches` top 10 by `final_score` | `prompts.prompt_text` `prompts.status=pending` | `data/logs/prompt_gen.log` |
| 2.2 | image_generator | `prompts` where `status=pending` limit 20 | `designs.raw_path` `designs.status=generated` | `data/designs/raw/<niche_id>/<prompt_id>.png` |
| 2.3 | image_processor | `designs` where `status=generated` | `designs.processed_path` `designs.status=processed` | `data/designs/processed/<design_id>.png` |
| 2.4 | clip_filter | `designs` where `status=processed` | `designs.clip_score` `designs.status=approved/rejected` | `data/logs/clip_filter.log` |
| 2.5 | mockup_generator | `designs` where `status=approved` | `designs.mockup_path` `designs.status=mockup_ready` | `data/designs/mockups/<design_id>.png` |
| 3.1 | copy_generator | `designs` where `status=mockup_ready` | `listings.title` `listings.description` `listings.tags` `listings.status=copy_ready` | `data/logs/copy_gen.log` |
| 3.2 | caption_generator | `listings` where `caption IS NULL` | `listings.caption` | `data/logs/caption_gen.log` |
| 4.1 | printify_publisher | `listings` where `status=copy_ready` | `listings.printify_product_id` | `data/logs/printify_publish.log` |
| 4.2 | etsy_uploader | `listings` where `printify_product_id` set | `listings.etsy_listing_id` `listings.status=live` `listings.uploaded_at` | `data/logs/etsy_uploader.log` |
| 4.3 | order_router | Etsy webhook payload | Printify fulfillment via API | `data/logs/order_router.log` |
| 4.4 | price_adjuster | `listings` where `status=live` | none (read-only) | `data/logs/price_check.log` |
| 4.5 | social_poster | `listings` where `status=live` limit 5 | `listings.social_posted` | `data/logs/social_post.log` |
| 5.1 | analytics_puller | Etsy stats API per `etsy_listing_id` | `listings.views` `listings.favorites` `listings.sales` `listings.revenue` | `data/logs/analytics_pull.log` |
| 5.2 | performance_flagger | `listings` where `uploaded_at` older than 7d | `listings.status=underperforming` | `data/logs/performance_flag.log` |
| 5.3 | weekly_report | `listings` + `niches` joined aggregates | none | `data/logs/report_YYYY-MM-DD.md` |

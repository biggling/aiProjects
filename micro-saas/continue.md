# Micro-SaaS — Continue

## Last Session
2026-03-22 — Project initialized.

## What This Is
Focused software solving one specific problem for a limited audience. BiG's microservices + API experience makes this natural. Goal: one boring problem solved deeply, recurring subscription revenue.

## Priority: GOOD (Tier 2) — start after mcp-apps and digital-products

## Product Ideas (ranked by Thai market fit + build speed)
1. **Shopee seller analytics dashboard** — sales trends, top SKUs, profit margin calc; Shopee has no good built-in analytics
2. **Thai-language invoice generator** — bilingual PDF invoices for Thai freelancers/small biz, PromptPay QR embedded
3. **Small team uptime/monitoring dashboard** — simpler than Datadog, $5/month, targeted at 1-5 person dev shops
4. **Crypto tax report generator (Thai)** — calculates capital gains for Thai tax filing, understands TH exchanges (Bitkub)

## Pricing Model
- $5–20/month subscription
- Free tier (limited reports/seats) → paid
- Annual plan discount to lock in cash flow

## Tech Stack
- Go backend (BiG's strength) + simple React or HTMX frontend
- Postgres on Railway/Supabase
- Stripe for billing
- Deploy: Railway or Fly.io

## Phase Plan
- [ ] Phase 1: Validate one idea (5 potential customers say they'd pay)
- [ ] Phase 2: Build MVP in one weekend
- [ ] Phase 3: Launch on IndieHackers + Thai dev Facebook groups
- [ ] Phase 4: Add billing, iterate on feedback

## Current Phase
**Phase 1** — Not started

## Next Step
Pick one idea. Shopee seller analytics is highest fit — post in Thai seller Facebook groups to gauge interest before building.

## Notes
- Rule: solve a problem you personally have first
- Keep it boring — boring niches have less competition
- Aim for 10 paying customers before adding features
- BiG's Thai market knowledge is a moat for Thai-specific tools

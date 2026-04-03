# Project Brief

> Static context — written once, updated only when fundamentals change.
> Claude reads this every session to understand the shape of the system.

---

## What This Project Is

[One paragraph: what the product does, who uses it, why it exists]

Example:
> A SaaS dashboard for Shopee sellers in Thailand. Users connect their Shopee store and see sales trends, top SKUs, and profit margins. Built for sellers who find Shopee's built-in analytics too basic to make restocking decisions.

---

## Stack

| Layer | Technology | Notes |
|---|---|---|
| Backend | [e.g. Go 1.22, chi router] | [e.g. REST API, no GraphQL] |
| Database | [e.g. Postgres 15, pgx/v5] | [e.g. migrations with golang-migrate] |
| Frontend | [e.g. React 18, TypeScript, Vite] | [e.g. TanStack Query for server state] |
| Infra | [e.g. Railway, Docker] | [e.g. single container, no K8s] |
| Auth | [e.g. JWT, no OAuth yet] | |

---

## Non-Negotiables

Rules that never change. If Claude suggests violating one, refuse.

- [e.g. No ORM — raw SQL with pgx only]
- [e.g. No JavaScript — TypeScript strict mode only]
- [e.g. No external auth services — handle in-house]
- [e.g. Free-tier infrastructure only until first revenue]

---

## Repository Structure

```
[paste your actual directory tree here]
```

---

## Key Design Decisions

Decisions already made. Don't re-open these without a strong reason.

- [e.g. Single-page app — not SSR. Reason: team knows React, no SEO needed]
- [e.g. Postgres over MySQL — already have expertise, no migration planned]
- [e.g. No message queue yet — direct DB polling until scale demands it]

---

## External Dependencies

Services and APIs this project depends on.

| Service | Purpose | Free Tier Limit |
|---|---|---|
| [e.g. Shopee API] | [product data] | [1000 req/day] |
| [e.g. Anthropic API] | [copy generation] | [pay per token] |

---

## Out of Scope (for now)

Things explicitly not being built yet.

- [e.g. Mobile app]
- [e.g. Multi-currency support]
- [e.g. Team accounts]

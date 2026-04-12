# Architecture Decisions Log

> This file records significant technical decisions — why you chose one approach over another.
> Claude reads this to avoid re-litigating past decisions and to understand constraints.
> Format: date, decision, alternatives considered, reason chosen.

---

## How to Use This File

Add an entry when:
- You choose a library/framework over alternatives
- You decide on a naming convention or code pattern
- You reject an approach (so Claude doesn't re-propose it)
- Something broke and you changed how you handle it

Claude reads this at session start and will not re-propose rejected approaches.

---

## Template

```
### [short decision title] — [YYYY-MM-DD]
**Decision:** [what was decided]
**Alternatives considered:** [what else was evaluated]
**Reason:** [why this choice]
**Constraints:** [any conditions that would change this decision]
```

---

## Decisions

<!-- Add your decisions below. Example: -->

<!--
### Use pgx instead of database/sql — 2026-01-15
**Decision:** Use pgx/v5 as the Postgres driver — not database/sql
**Alternatives considered:** database/sql (stdlib), gorm (ORM)
**Reason:** pgx is faster, supports named prepared statements, has better type mapping. gorm adds too much magic.
**Constraints:** If we ever need to support multiple databases, revisit.

### JWT in httponly cookies, not Authorization header — 2026-02-03
**Decision:** Store JWT in httponly cookies (not localStorage, not Authorization header)
**Alternatives considered:** localStorage (XSS risk), sessionStorage (lost on tab close), Authorization header (CORS issues with mobile)
**Reason:** httponly cookie is the safest for web apps — not accessible via JS, not sent via CORS preflight
**Constraints:** Mobile apps can't use cookies — they need Authorization header. If mobile client added, re-evaluate.
-->

# System Patterns

> Architecture decisions, conventions, and hard-learned lessons.
> When Claude makes a mistake and you correct it, add the rule here so it never happens again.
> This file grows over time and never shrinks.

---

## Architecture

[How the system is structured. High-level patterns that apply everywhere.]

Example:
> **Request flow:** HTTP handler → validates input with Zod → calls service function → service calls repository → repository queries DB. No business logic in handlers. No DB calls in services.

---

## Naming Conventions

| Thing | Convention | Example |
|---|---|---|
| [e.g. DB tables] | [e.g. snake_case, plural] | [e.g. user_sessions] |
| [e.g. Go functions] | [e.g. verb + noun] | [e.g. GetUserByID] |
| [e.g. React components] | [e.g. PascalCase] | [e.g. ProductCard] |
| [e.g. API endpoints] | [e.g. /api/v1/resources/:id] | [e.g. /api/v1/products/123] |

---

## Patterns That Work

[Things you've validated in this codebase. Use these, don't reinvent.]

### [Pattern Name]
```
[code or description]
```
Why: [one line explanation]

---

## Mistakes Claude Made (and corrections)

> Every entry here prevents the same mistake from happening again.

- **[date]** Claude used [wrong pattern]. Correct approach: [right pattern]. Rule: [never do X, always do Y].

Example:
- **2026-04-01** Claude used `session.query(User)` (SQLAlchemy 1.x style). Correct: `session.execute(select(User))`. Rule: always use SQLAlchemy 2.x execute() style.
- **2026-03-28** Claude added business logic to the HTTP handler. Rule: handlers only validate + call services. Zero logic.

---

## Performance Notes

[Things that affect performance in this specific codebase.]

- [finding + what to do about it]

---

## Security Rules

[Project-specific security constraints.]

- [rule]
- [rule]

---

## Testing Patterns

[How tests are structured in this project.]

- Test files live at: [location]
- Mock pattern: [how mocking is done]
- DB in tests: [real DB / in-memory / mocked]
- Run tests with: [command]

# CLAUDE.md — Next.js / React (App Router)

## Stack
Next.js 14+, App Router, TypeScript 5.x, React 18, Tailwind CSS, Prisma, NextAuth.js, Zod.

## Commands
```bash
npm run dev          # next dev
npm run build        # next build
npm run start        # next start (production)
npm run lint         # next lint
npm run typecheck    # tsc --noEmit
npx prisma studio    # DB GUI
npx prisma migrate dev --name <name>  # create + apply migration
npx prisma generate  # regenerate client after schema change
```

## App Router Conventions

### Folder Structure
```
app/
  layout.tsx              ← root layout (html, body, providers)
  page.tsx                ← home route
  (auth)/                 ← route group — no URL segment
    login/page.tsx
    register/page.tsx
  dashboard/
    layout.tsx            ← nested layout for dashboard
    page.tsx
    [id]/page.tsx         ← dynamic segment
  api/
    users/route.ts        ← API route handler
components/
  ui/                     ← generic, no business logic (Button, Input, Modal)
  features/               ← domain-specific (UserCard, OrderList)
lib/
  db.ts                   ← Prisma client singleton
  auth.ts                 ← NextAuth config
  validations.ts          ← Zod schemas
actions/
  user.ts                 ← Server Actions
types/
  index.ts                ← shared TypeScript types
```

### Server vs Client Components
- Default to Server Components — add `"use client"` only when you need:
  - `useState` / `useEffect` / event handlers
  - Browser APIs (`window`, `document`)
  - Client-side libraries (charts, drag-and-drop)
- Never import heavy client libraries into Server Components
- Pass data from Server to Client as props — don't fetch in Client Components

```tsx
// Server Component (default — no directive needed)
export default async function UsersPage() {
  const users = await db.user.findMany()   // ← direct DB call, no API needed
  return <UserList users={users} />        // ← pass data down as props
}

// Client Component — only where interactivity is needed
'use client'
export function UserList({ users }: { users: User[] }) {
  const [filter, setFilter] = useState('')
  return (...)
}
```

### Data Fetching
- Server Components: fetch directly from DB/ORM — skip the API layer for internal data
- Client Components: use SWR or React Query for client-side fetching
- Use `cache()` for deduplication across a request, `revalidate` for ISR
- Never `useEffect` + `fetch` in Client Components — use SWR

```tsx
// Correct — Server Component with caching
import { cache } from 'react'

const getUser = cache(async (id: string) => {
  return db.user.findUnique({ where: { id } })
})
```

### Server Actions
- Use Server Actions for form submissions and mutations — no need for API routes
- Define in `actions/` directory with `'use server'` directive
- Validate input with Zod before any DB operation
- Return `{ success: true, data }` or `{ success: false, error: string }` — consistent shape

```typescript
// actions/user.ts
'use server'
import { z } from 'zod'

const schema = z.object({ name: z.string().min(1), email: z.string().email() })

export async function createUser(formData: FormData) {
  const result = schema.safeParse(Object.fromEntries(formData))
  if (!result.success) return { success: false, error: result.error.message }

  const user = await db.user.create({ data: result.data })
  revalidatePath('/users')
  return { success: true, data: user }
}
```

### API Routes (Route Handlers)
- Use API routes only for: webhooks, OAuth callbacks, public APIs consumed by external clients
- Internal app data → Server Components + Server Actions (not API routes)
- Always validate request body with Zod before processing

```typescript
// app/api/webhooks/stripe/route.ts
export async function POST(request: Request) {
  const body = await request.text()
  const sig = request.headers.get('stripe-signature')!
  // verify webhook signature, process event...
}
```

### Prisma
- One client instance: `lib/db.ts` — import `db` everywhere, never `new PrismaClient()`
- Always use `select` to fetch only needed fields — never `findMany()` without limits
- Use transactions for multi-step writes: `db.$transaction([...])`
- Run `prisma generate` after every schema change

```typescript
// lib/db.ts — singleton pattern
import { PrismaClient } from '@prisma/client'
declare global { var prisma: PrismaClient | undefined }
export const db = global.prisma ?? new PrismaClient()
if (process.env.NODE_ENV !== 'production') global.prisma = db
```

### Auth (NextAuth.js v5 / Auth.js)
- Config in `lib/auth.ts` — one place for providers, callbacks, session strategy
- Use `auth()` server-side for session, `useSession()` client-side
- Protect routes in `middleware.ts` — never trust client-side auth checks alone
- JWT strategy for API routes, database sessions for web app sessions

### Environment Variables
- `NEXT_PUBLIC_` prefix = exposed to browser — never put secrets here
- Non-prefixed vars = server only — safe for DB URLs, API keys
- Validate all env vars at startup with Zod in `lib/env.ts`
- `.env.local` for local dev, actual env vars in production (never commit `.env.local`)

## Security
- Use `headers()` to set security headers in `next.config.ts`: CSP, X-Frame-Options, etc.
- Sanitize user content before rendering — never dangerouslySetInnerHTML with user data
- Validate all Server Action inputs — they're callable from the client
- Rate-limit auth endpoints and Server Actions with `upstash/ratelimit` or similar
- Never expose DB IDs in URLs for sensitive resources — use UUIDs or slugs

## Performance
- Use `next/image` for all images — automatic optimization, lazy loading, sizing
- Use `next/font` for fonts — avoids layout shift, self-hosted automatically
- Use `loading.tsx` files for Suspense boundaries — instant visual feedback
- Avoid client-side state that duplicates server data — let Server Components own it

## Common Mistakes Claude Makes Without This Config
- Adding `"use client"` to every component (makes the whole tree a client bundle)
- Fetching data in Client Components with `useEffect` instead of Server Components
- Creating API routes for internal data instead of using Server Components directly
- Forgetting `revalidatePath()` after mutations — UI shows stale data
- Using `new PrismaClient()` everywhere instead of the singleton
- Putting secrets in `NEXT_PUBLIC_` env vars
- Not validating Server Action inputs (they're public endpoints)

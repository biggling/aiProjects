# CLAUDE.md — TypeScript / Node.js

## Stack
TypeScript 5.x, Node.js 20+, ESM modules, Hono or Express, Zod, Vitest.

## Commands
```bash
npm run dev          # tsx watch src/index.ts
npm run build        # tsc --noEmit && tsc
npm test             # vitest run
npm run lint         # eslint src/
npm run typecheck    # tsc --noEmit
```

## Code Conventions

### TypeScript Rules
- Strict mode always: `"strict": true` in tsconfig — no exceptions
- No `any` — use `unknown` and narrow with type guards, or use generics
- No non-null assertions (`!`) unless you've proven the value exists with a comment why
- Explicit return types on exported functions; infer return types on internal functions
- Use `satisfies` operator for config objects to get both inference and type checking
- Prefer `type` over `interface` for object shapes; use `interface` only for extension/merging

### Imports / Modules
- ESM only: `"type": "module"` in package.json, `.js` extensions in imports
- No default exports — named exports only (easier to refactor, better tree-shaking)
- Group imports: 1) Node built-ins, 2) external packages, 3) internal modules
- Use `import type` for type-only imports: `import type { Foo } from './foo.js'`

### Runtime Validation
- Validate all external data (API requests, env vars, file reads) with Zod
- Define schemas next to the types that use them
- Use `z.infer<typeof Schema>` for type derivation — single source of truth
- Throw `ZodError` on invalid input at boundaries; catch and return 400 in handlers

### Error Handling
- Use `Result<T, E>` pattern for expected failures (no try/catch for control flow)
- Throw only for programmer errors (bugs), not user/input errors
- Always type caught errors: `catch (e) { if (e instanceof Error) ... }`
- Never swallow errors silently — at minimum log them

### Async
- `async/await` everywhere — no raw `.then()` chains
- Always `await` Promises; never fire-and-forget without error handling
- Use `Promise.all()` for parallel independent operations
- Add timeouts to all network calls with `AbortController`

### Project Structure
```
src/
  index.ts          ← entry point, server setup only
  routes/           ← route handlers, thin — call services only
  services/         ← business logic
  repositories/     ← data access (DB, external APIs)
  schemas/          ← Zod schemas + inferred types
  lib/              ← shared utilities, no business logic
  types/            ← global type declarations
```

### Hono Conventions (if using Hono)
- Define routes in `routes/` files, register in `index.ts`
- Use Hono's built-in validator middleware with Zod: `zValidator('json', schema)`
- Set proper content-type and status codes explicitly
- Use `c.env` for environment variables (typed with `Env` type parameter)

### MCP Server Conventions (if using @modelcontextprotocol/sdk)
- Streamable HTTP transport only — SSE transport is deprecated
- Tool responses must be under 25,000 tokens
- Annotate every tool with `readOnly: true/false` and `destructiveHint: true/false`
- Use `z.object()` schemas for all tool input validation
- Keep tool names snake_case: `get_portfolio_value`, not `getPortfolioValue`

### Environment Variables
- Load with `dotenv` in dev only — never in production (use actual env)
- Validate all env vars at startup with a Zod schema, crash fast if invalid
- Type env access: create `src/env.ts` that exports parsed, typed env object

### Testing (Vitest)
- Test files: `src/__tests__/foo.test.ts` or co-located `foo.test.ts`
- Use `vi.mock()` sparingly — prefer dependency injection for testability
- Test behavior, not implementation — don't assert on internal state
- Use `beforeEach` to reset state; avoid test interdependency

### What NOT to Do
- No `require()` — ESM imports only
- No `var` — use `const` by default, `let` only when reassignment is needed
- No `console.log` in production code — use a structured logger (pino)
- No `ts-ignore` or `eslint-disable` without a comment explaining why
- No synchronous file I/O (`readFileSync`) in request handlers

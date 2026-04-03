# Agent Instructions — TypeScript / Node.js

## allowed_tools
read, write, edit, bash, search

## context_files
- memory-bank/projectBrief.md
- memory-bank/activeContext.md
- memory-bank/progress.md
- memory-bank/systemPatterns.md
- continue.md

## conventions

### TypeScript
- Strict mode always — no exceptions
- No `any` — use `unknown` and narrow with type guards
- No non-null assertions (`!`) without a comment explaining why
- Named exports only — no default exports
- `import type` for type-only imports

### Modules
- ESM only: `"type": "module"` in package.json
- `.js` extensions in all imports
- Group: Node built-ins → external packages → internal modules

### Validation
- Zod for all external data (requests, env vars, file reads)
- `z.infer<typeof Schema>` for type derivation — single source of truth

### Async
- `async/await` everywhere — no raw `.then()` chains
- `Promise.all()` for parallel independent operations
- `AbortController` for timeouts on all network calls

### Errors
- Throw only for programmer errors — not user/input errors
- Always type caught errors: `catch (e) { if (e instanceof Error) ... }`

### What Not To Do
- No `require()` — ESM imports only
- No `var` — const by default, let only when reassignment needed
- No `console.log` in production — use pino
- No `ts-ignore` without comment

## workflow
1. Read context_files before starting any task
2. Run `npm run typecheck` after any TypeScript changes
3. Follow conventions above autonomously
4. Update continue.md when done
5. Ask only for: money decisions, genuine blockers, major architectural tradeoffs

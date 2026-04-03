# Agent Instructions — Go Microservices

## allowed_tools
read, write, edit, bash, search

## context_files
- memory-bank/projectBrief.md
- memory-bank/activeContext.md
- memory-bank/progress.md
- memory-bank/systemPatterns.md
- continue.md

## conventions

### Error Handling
- Wrap errors with context: `fmt.Errorf("doing X: %w", err)`
- No `panic()` in library or service code — only in main() for startup failures
- Return errors up the stack; handle once at the entry point
- Use `errors.Is()` / `errors.As()` for type checks — never string matching

### Naming
- Interfaces: single-method = `<Method>er` (Reader, Storer)
- No stutter: `user.UserService` → `user.Service`
- Acronyms uppercase: `userID`, `httpURL`

### Structure
- cmd/<name>/main.go — entry point only, wire dependencies
- internal/handler/ — HTTP/gRPC handlers, no business logic
- internal/service/ — business logic only
- internal/repository/ — DB queries, returns domain types

### Logging
- `slog` (stdlib Go 1.21+): `slog.Info("msg", "key", value)`
- Never log secrets or tokens
- Log at INFO for normal flow, ERROR for recoverable errors

### Testing
- Table-driven tests for all pure functions
- `testify/require` for setup, `testify/assert` for assertions

### What Not To Do
- No `init()` with side effects
- No global mutable state
- No ignoring errors: `_, err := f()` must handle err
- No `time.Sleep` in production logic

## workflow
1. Read context_files before starting any task
2. Follow conventions above — no need to ask about established patterns
3. Make implementation decisions autonomously
4. Update continue.md when done with: what was done, what's next
5. Ask only when: task involves money, two approaches have real tradeoffs, or you're genuinely blocked

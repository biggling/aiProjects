# CLAUDE.md — Go Microservices

## Stack
Go 1.22+, microservices architecture, REST/gRPC, Postgres, Redis, Docker/Kubernetes.

## Commands
```bash
go build ./...
go test ./... -v -race
go vet ./...
golangci-lint run
```

## Code Conventions

### Error Handling
- Always wrap errors with context: `fmt.Errorf("doing X: %w", err)`
- Never use `panic()` in library or service code — only in `main()` for unrecoverable startup failures
- Return errors up the call stack; handle them once at the entry point (handler/main)
- Use `errors.Is()` and `errors.As()` for error type checking, never string matching

### Naming
- Interfaces: single-method interfaces use `<Method>er` (e.g., `Reader`, `Storer`)
- Avoid stutter: `user.UserService` → `user.Service`
- Unexported fields in structs — export only what callers need
- Acronyms stay uppercase: `userID`, `httpURL`, `parseJSON`

### Interfaces
- Define interfaces in the consuming package, not the implementing package
- Keep interfaces small (1–3 methods); compose larger behavior from small interfaces
- Accept interfaces, return concrete types

### Project Structure
```
cmd/
  servicename/main.go   ← entry point only, wire dependencies here
internal/
  handler/              ← HTTP/gRPC handlers, no business logic
  service/              ← business logic, no DB/HTTP knowledge
  repository/           ← DB queries, returns domain types
  domain/               ← structs, no methods with side effects
pkg/                    ← shared, importable by other services
```

### Logging
- Use `slog` (stdlib, Go 1.21+): `slog.Info("message", "key", value)`
- Always include request ID in logs: `slog.With("request_id", id)`
- Never log secrets, tokens, or passwords
- Log at INFO for normal flow, ERROR for recoverable errors, no DEBUG in production

### HTTP Handlers
- Handlers only: decode request → call service → encode response
- No business logic in handlers
- Use `net/http` stdlib or `chi` router
- Always set timeouts: `http.Server{ReadTimeout: 5*time.Second, WriteTimeout: 10*time.Second}`
- Return proper HTTP status codes; never return 200 with an error body

### Testing
- Table-driven tests for all pure functions
- Use `testify/assert` and `testify/require`
- `require` for setup/preconditions (stops test on fail), `assert` for assertions
- Name test files `*_test.go`, test functions `TestFuncName_Scenario`
- Mock interfaces with `testify/mock` or hand-rolled fakes — never mock concrete types

### Concurrency
- Pass `context.Context` as first argument to every function that does I/O
- Cancel contexts on timeout/shutdown; check `ctx.Err()` in loops
- Use `sync.WaitGroup` for goroutine lifecycle; never fire-and-forget without tracking
- Prefer channels for communication, mutexes for state — never mix

### Database
- Use `pgx/v5` for Postgres; avoid `database/sql` raw interface
- Keep transactions short; never hold a transaction across HTTP request boundary
- Use parameterized queries — never string-format SQL
- Run migrations with `golang-migrate` or `goose`; migrations are versioned files, not code

### Configuration
- Load config from environment variables via `os.Getenv` or `envconfig`
- Validate all config at startup — fail fast if required vars are missing
- Never hardcode ports, hostnames, credentials, or timeouts

### What NOT to Do
- No `init()` functions with side effects
- No global mutable state
- No `interface{}` or `any` without a clear reason — use typed interfaces
- No `time.Sleep` in production logic — use tickers or context deadlines
- No ignoring errors: `_, err := f()` must handle `err`

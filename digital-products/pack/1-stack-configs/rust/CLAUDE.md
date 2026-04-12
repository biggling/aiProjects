# CLAUDE.md — Rust

## Stack
Rust (stable), Cargo, Tokio (async), Axum or Actix-web, SQLx, Serde, Anyhow/Thiserror, Clippy.

## Commands
```bash
cargo build                  # debug build
cargo build --release        # release build
cargo test                   # all tests
cargo test -- --nocapture    # show println! in tests
cargo clippy -- -D warnings  # lint (treat warnings as errors)
cargo fmt                    # format
cargo doc --open             # generate and open docs
cargo watch -x test          # auto-run tests on save (cargo-watch)
```

## Error Handling

### Library Code — thiserror
- Define your own error type with `#[derive(Error, Debug)]`
- Each variant maps to a specific failure mode — no catch-all
- Implement `From<OtherError>` via `#[from]` for automatic conversion

```rust
use thiserror::Error;

#[derive(Error, Debug)]
pub enum UserError {
    #[error("user {0} not found")]
    NotFound(i64),
    #[error("email already exists")]
    DuplicateEmail,
    #[error("database error: {0}")]
    Database(#[from] sqlx::Error),
}
```

### Application Code — anyhow
- Use `anyhow::Result<T>` in `main()`, `async fn main()`, and top-level handlers
- Use `context()` / `with_context()` to add meaning to errors as they propagate
- `?` everywhere — never `.unwrap()` in application code (only in tests/examples)

```rust
use anyhow::{Context, Result};

async fn load_config(path: &str) -> Result<Config> {
    let content = tokio::fs::read_to_string(path)
        .await
        .with_context(|| format!("reading config from {path}"))?;
    let config: Config = toml::from_str(&content)
        .context("parsing config TOML")?;
    Ok(config)
}
```

### Never Do
- Never `.unwrap()` or `.expect()` outside tests — use `?` or handle explicitly
- Never `panic!()` in library code
- Never use `unwrap_or_default()` to silently ignore errors

## Ownership and Borrowing
- Prefer `&str` over `String` for function parameters — callers choose allocation
- Return `String` when ownership is transferred, `&str` when borrowing internal data
- Use `Cow<'_, str>` when a function sometimes needs to allocate, sometimes can borrow
- Prefer `Arc<T>` for shared ownership across threads, `Rc<T>` for single-threaded

```rust
// Correct — accept &str, return owned when needed
fn greet(name: &str) -> String {
    format!("Hello, {name}!")
}

// Wrong — taking String when &str suffices
fn greet(name: String) -> String { ... }
```

## Async (Tokio)
- Use `tokio::spawn` for independent concurrent tasks — always `.await` the `JoinHandle` or handle the error
- Use `tokio::join!()` for parallel independent futures — not sequential `.await`
- Use `tokio::select!()` for racing futures or responding to cancellation
- Never use `std::thread::sleep` in async code — use `tokio::time::sleep`
- Mark functions `async` only when they do I/O — pure computation stays synchronous

```rust
// Parallel fetches
let (users, orders) = tokio::join!(
    fetch_users(db),
    fetch_orders(db)
);

// Wrong — sequential when parallel is possible
let users = fetch_users(db).await?;
let orders = fetch_orders(db).await?;
```

## Web (Axum)

### Structure
```
src/
  main.rs           ← server startup, router assembly
  routes/           ← handler modules (users.rs, orders.rs)
  models/           ← domain structs (User, Order)
  db/               ← SQLx queries
  errors.rs         ← AppError type implementing IntoResponse
  state.rs          ← AppState struct (DB pool, config)
```

### Handler Pattern
- Handlers extract state, path params, and body via Axum extractors — in that order
- Return `Result<impl IntoResponse, AppError>` from every handler
- Implement `IntoResponse` on `AppError` — map internal errors to HTTP status codes

```rust
// Correct Axum handler
async fn get_user(
    State(state): State<AppState>,
    Path(id): Path<i64>,
) -> Result<Json<User>, AppError> {
    let user = state.db.find_user(id).await?;
    match user {
        Some(u) => Ok(Json(u)),
        None => Err(AppError::NotFound),
    }
}
```

## SQLx
- Use compile-time checked queries: `sqlx::query_as!(Model, "SELECT ...", params)`
- Validate query against DB at compile time — run `cargo sqlx prepare` before committing
- Use connection pool (`PgPool`) — never single connections
- All DB functions are `async` — always `.await`

```rust
let user = sqlx::query_as!(
    User,
    "SELECT id, name, email FROM users WHERE id = $1",
    user_id
)
.fetch_optional(&pool)
.await
.context("fetching user from DB")?;
```

## Testing
- Unit tests in the same file as the code: `#[cfg(test)] mod tests { ... }`
- Integration tests in `tests/` directory — use `tokio::test` for async
- Use `sqlx::test` for DB tests — provides a temporary test database
- Never test against the production database

```rust
#[cfg(test)]
mod tests {
    use super::*;

    #[tokio::test]
    async fn test_create_user() {
        // ...
    }
}
```

## Clippy Rules
Run `cargo clippy -- -D warnings` in CI. Fix all warnings — they indicate real problems.
Common clippy fixes:
- `needless_return` → remove explicit `return`
- `clone_on_copy` → remove `.clone()` on `Copy` types
- `map_unwrap_or` → use `.map_or()` instead

## Security
- Never put secrets in source code — read from env vars at startup
- Use `secrecy::Secret<String>` for sensitive values in memory — prevents accidental logging
- Validate all user input before processing — use Serde's `#[serde(deny_unknown_fields)]`
- Use prepared statements via SQLx — never format SQL strings with user input

## Common Mistakes Claude Makes Without This Config
- Using `.unwrap()` in application code instead of `?`
- Accepting `String` instead of `&str` in function parameters
- Using `std::thread::sleep` inside async functions (blocks the runtime)
- Spawning Tokio tasks and ignoring the `JoinHandle` (silent failures)
- Sequential `.await` on independent async operations instead of `tokio::join!()`
- Missing `#[from]` on error variants (forces manual `From` implementations)
- Not using `cargo clippy` — missing obvious Rust idiom violations

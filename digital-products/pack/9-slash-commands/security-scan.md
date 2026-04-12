---
description: Scan staged or recently changed files for OWASP Top 10 security vulnerabilities
allowed-tools: Bash, Read, Glob, Grep
---

# /security-scan — OWASP Security Scan

Scan staged or recently changed files for security vulnerabilities.

## Step 1: Get the files to scan
Run `git diff --staged --name-only` for staged. If nothing staged, run `git diff HEAD~1 --name-only`.
Scan source files only. Skip tests, markdown, generated code.

## Step 2: Check each file for these vulnerability patterns

### Injection (A03)
- SQL: string concatenation or formatting in queries — `"SELECT * WHERE id = " + id`
- Command injection: user input in `exec()`, `os.system()`, `subprocess`, `Bash`, `eval()`
- Template injection: user-controlled template strings

### Broken Auth (A07)
- Hardcoded credentials: `password = "secret"`, `token = "eyJ..."`  
- Weak tokens: `Math.random()`, `rand.Intn()` for security-sensitive IDs
- Missing auth checks on routes/handlers
- JWT not validating `exp`, `iss`, `aud`

### Sensitive Data Exposure (A02)
- Secrets, API keys, tokens in code or comments
- PII logged to stdout/logfiles
- Passwords stored without hashing, or hashed with MD5/SHA1

### Insecure Design (A04)
- Missing rate limiting on auth endpoints
- No input size limits (`MaxBytesReader`, request body limits)
- CORS `allow_origins = ["*"]` in production paths

### Security Misconfiguration (A05)
- Debug mode enabled unconditionally
- Stack traces exposed to clients
- Missing security headers (X-Frame-Options, CSP, HSTS)

### Vulnerable Dependencies (A06)
- Note any packages imported with known vulnerability patterns
- (Full scan: suggest running `npm audit`, `pip-audit`, `cargo audit`, `govulncheck`)

## Step 3: Output format

```
## Security Scan — [date]

### 🔴 Critical (fix before merge)
- file.go:42 — SQL injection: user input concatenated into query
  Fix: use parameterized query `db.Query("... WHERE id = $1", id)`

### 🟡 High (fix before deploy)
- config.py:8 — Hardcoded API key: `STRIPE_KEY = "sk_live_..."`
  Fix: load from environment variable

### 🟢 Informational
- [non-blocking observations]

### ✅ Clean
[areas checked with no issues found]
```

If no issues found: output "✅ No security issues found in changed files."

$ARGUMENTS

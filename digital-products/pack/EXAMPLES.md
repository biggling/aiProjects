# Usage Examples — Claude Code Elite Pack

Real before/after examples showing exactly how each component solves the problems developers hit daily.

---

## Table of Contents

1. [Stack Configs — Claude that knows your conventions](#1-stack-configs)
2. [Memory OS — Never re-explain your project again](#2-memory-os)
3. [Auto Mode Profiles — Safe autonomous operation](#3-auto-mode-profiles)
4. [Hooks — Hard safety rails that can't be ignored](#4-hooks)
5. [Multi-Agent System — Claude works while you sleep](#5-multi-agent-system)
6. [1M Context Optimization — Stop burning tokens on what Claude already knows](#6-1m-context-optimization)
7. [Cross-Platform AGENTS.md — Same conventions in every AI tool](#7-cross-platform)

---

## 1. Stack Configs

### The Problem

You start a new Claude session. You ask it to add an endpoint to your Go service.
Claude writes this:

```go
// WITHOUT stack config — Claude guesses your conventions
func GetUser(db *sql.DB, id string) (*User, error) {
    var user User
    err := db.QueryRow("SELECT * FROM users WHERE id = " + id).Scan(&user.ID, &user.Name)
    if err != nil {
        panic(err)  // ← wrong
    }
    return &user, nil
}
```

Problems: SQL injection via string concat, `panic` in service code, using `database/sql` instead of `pgx`, no context propagation.

### With the Go CLAUDE.md

Claude produces this instead — without you saying a word:

```go
// WITH go-microservices/CLAUDE.md — Claude knows your conventions
func (r *UserRepository) GetUser(ctx context.Context, id string) (*domain.User, error) {
    row, err := r.db.QueryRow(ctx, "SELECT id, name FROM users WHERE id = $1", id)
    if err != nil {
        return nil, fmt.Errorf("getting user %s: %w", id, err)
    }
    var u domain.User
    if err := row.Scan(&u.ID, &u.Name); err != nil {
        if errors.Is(err, pgx.ErrNoRows) {
            return nil, nil
        }
        return nil, fmt.Errorf("scanning user: %w", err)
    }
    return &u, nil
}
```

No SQL injection. No panic. Context passed through. pgx used. Error wrapped correctly.

---

### TypeScript Example

**Prompt:** "Add a POST /users endpoint"

**Without config:**
```typescript
app.post('/users', async (req, res) => {
  const user = await db.query(`INSERT INTO users VALUES ('${req.body.name}')`)
  res.json(user)  // ← no validation, SQL injection, no error handling
})
```

**With typescript-node/CLAUDE.md:**
```typescript
const createUserSchema = z.object({ name: z.string().min(1).max(100) })

usersRouter.post('/', async (c) => {
  const result = createUserSchema.safeParse(await c.req.json())
  if (!result.success) return c.json({ error: 'Invalid input' }, 400)

  const user = await userService.create(result.data)
  return c.json(user, 201)
})
```

Zod validation, no injection, proper status code, typed response.

---

### Next.js Example

**Prompt:** "Add a page that shows all users from the database"

**Without config:**
```tsx
// Client Component fetching on mount — wasteful and slow
'use client'
export default function UsersPage() {
  const [users, setUsers] = useState([])
  useEffect(() => {
    fetch('/api/users').then(r => r.json()).then(setUsers)
  }, [])
  return <div>{users.map(u => <div key={u.id}>{u.name}</div>)}</div>
}
```

**With nextjs-react/CLAUDE.md:**
```tsx
// Server Component — direct DB access, zero client JS, full SEO
export default async function UsersPage() {
  const users = await db.user.findMany({
    select: { id: true, name: true, email: true },
    orderBy: { createdAt: 'desc' },
  })
  return <UserList users={users} />
}
```

No API route needed. No client bundle. Rendered on the server. Faster, simpler.

---

### Rust Example

**Prompt:** "Add an endpoint to get a user by ID"

**Without config:**
```rust
async fn get_user(id: web::Path<u64>) -> impl Responder {
    let user = DB.query_one("SELECT * FROM users WHERE id = " + &id.to_string(), ...).unwrap();
    HttpResponse::Ok().json(user)
}
```

**With rust/CLAUDE.md:**
```rust
async fn get_user(
    State(state): State<AppState>,
    Path(id): Path<i64>,
) -> Result<Json<User>, AppError> {
    let user = sqlx::query_as!(User, "SELECT id, name, email FROM users WHERE id = $1", id)
        .fetch_optional(&state.pool)
        .await
        .context("fetching user")?;
    match user {
        Some(u) => Ok(Json(u)),
        None => Err(AppError::NotFound),
    }
}
```

Compile-time checked SQL. No SQL injection. Proper error types. No `.unwrap()`.

---

### Java Spring Boot Example

**Prompt:** "Create a service to get orders for a user"

**Without config:**
```java
@RestController
public class OrderController {
    @Autowired
    OrderRepository repo;

    @GetMapping("/orders/{userId}")
    public List<Order> getOrders(@PathVariable Long userId) {
        return repo.findAll().stream()  // ← loads ENTIRE table
            .filter(o -> o.getUserId().equals(userId))
            .collect(Collectors.toList());
    }
}
```

**With java-spring-boot/CLAUDE.md:**
```java
// Repository
public interface OrderRepository extends JpaRepository<Order, Long> {
    List<Order> findByUserIdOrderByCreatedAtDesc(Long userId);
}

// Service
@Service @Transactional @RequiredArgsConstructor
public class OrderService {
    private final OrderRepository orderRepository;
    private final OrderMapper orderMapper;

    @Transactional(readOnly = true)
    public List<OrderResponse> getUserOrders(Long userId) {
        return orderRepository.findByUserIdOrderByCreatedAtDesc(userId)
            .stream().map(orderMapper::toResponse).toList();
    }
}

// Controller
@GetMapping("/{userId}/orders")
public ResponseEntity<List<OrderResponse>> getUserOrders(@PathVariable Long userId) {
    return ResponseEntity.ok(orderService.getUserOrders(userId));
}
```

Proper layering. No N+1. Constructor injection. DTO separation.

---

### Python FastAPI Example

**Prompt:** "Add an endpoint to get items from the database"

**Without config:**
```python
@app.get("/items/{id}")
async def get_item(id: int, db: Session = Depends(get_db)):
    item = db.execute(select(Item).where(Item.id == id))  # ← blocks event loop
    return item.scalar_one_or_none()
```

**With python-fastapi-react/CLAUDE.md:**
```python
@router.get("/items/{id}", response_model=ItemResponse)
async def get_item(id: int, db: Session = Depends(get_db)):
    item = await asyncio.to_thread(
        db.execute, select(Item).where(Item.id == id)
    )
    result = item.scalar_one_or_none()
    if not result:
        raise HTTPException(status_code=404, detail="Item not found")
    return result
```

Sync DB call properly wrapped, 404 handled, response model typed.

---

### Kotlin Android Example

**Prompt:** "Show a list of items from the database"

**Without config:**
```kotlin
// In a Composable — wrong on multiple levels
@Composable
fun ItemList() {
    val items = runBlocking { db.itemDao().getAll() }  // ← blocks main thread
    Column {
        items.forEach { item -> Text(item.name) }  // ← no lazy loading
    }
}
```

**With kotlin-android/CLAUDE.md:**
```kotlin
@HiltViewModel
class ItemListViewModel @Inject constructor(
    private val repository: ItemRepository
) : ViewModel() {
    val uiState: StateFlow<ItemListUiState> = repository.getAllItems()
        .map { ItemListUiState.Success(it) }
        .stateIn(viewModelScope, SharingStarted.WhileSubscribed(5000), ItemListUiState.Loading)
}

@Composable
fun ItemListScreen(viewModel: ItemListViewModel = hiltViewModel()) {
    val state by viewModel.uiState.collectAsState()
    when (state) {
        is ItemListUiState.Loading -> CircularProgressIndicator()
        is ItemListUiState.Success -> LazyColumn {
            items((state as ItemListUiState.Success).items) { item ->
                Text(item.name)
            }
        }
        is ItemListUiState.Error -> Text((state as ItemListUiState.Error).message)
    }
}
```

MVVM correctly layered, StateFlow, LazyColumn, proper loading states.

---

## 2. Memory OS

### The Problem

**Session 1:** You spend 15 minutes explaining to Claude what your project does, what stack you're using, what patterns you've established. Claude finally gets up to speed and writes good code.

**Session 2 (next day):** Claude has forgotten everything. You start over.

Over a week, you're wasting 1–2 hours just re-explaining context.

### The Solution

After Memory OS setup, your session starts like this:

**You:** "Continue working on the auth flow"

**Claude:** *(reads memory-bank/ in 30 seconds)*
> I can see from memory-bank/:
> - This is a FastAPI + React trading dashboard
> - Auth uses JWT with 15-min access tokens + 30-day refresh tokens stored in httponly cookies
> - Last session: completed the `/auth/refresh` endpoint, left off at the React `useAuth` hook
> - Known gotcha: never use `localStorage` for tokens (noted in systemPatterns.md)
>
> Picking up at the `useAuth` hook...

No re-explanation. Full context at turn 0.

### Setup Example

```bash
# One-time setup from your project root
cd /my-project
bash /path/to/pack/2-memory-os/setup-memory-os.sh

# Creates:
# memory-bank/projectBrief.md    ← fill this in once
# memory-bank/activeContext.md   ← Claude updates this each session
# memory-bank/progress.md        ← running task list
# memory-bank/systemPatterns.md  ← architecture decisions + gotchas
```

**Fill in projectBrief.md once:**
```markdown
## Project
Crypto trading dashboard. FastAPI backend, React frontend, Postgres DB.

## Stack
Python 3.11, FastAPI 0.111, SQLAlchemy 2.x, React 18, TypeScript, React Query v5, Vite.

## Rules
- Never store JWT in localStorage — httponly cookie only
- All money amounts stored as integers (cents) — never floats
- All DB access via Repository layer — never direct from routes
```

**After first real session, systemPatterns.md looks like:**
```markdown
## Architecture Decisions
- WebSocket manager is a singleton in api/ws.py — never instantiate a second one
- React Query keys: always arrays — ['orders', id], ['orders', 'list']
- Auth: verify_api_key dependency on all routes except /health and /ws

## Gotchas Discovered
- SQLAlchemy session must be wrapped in asyncio.to_thread() — blocks event loop otherwise
- Vite proxies /api to localhost:8000 in dev — don't add /api prefix to fetch calls
```

Now Claude never makes those mistakes again — and never needs to be told twice.

---

## 3. Auto Mode Profiles

### The Problem

You want to run Claude in Auto Mode (no approval prompts) so it can work through a task uninterrupted. But the default settings are too permissive — you've had Claude accidentally `git push` to main or delete files.

Conversely, the conservative mode is so locked down that Claude can't even install a dependency.

### The Solution

Four profiles, each calibrated for a specific workflow.

**Scenario 1: Auditing unfamiliar code**
```bash
cp 3-auto-mode-profiles/conservative/settings.json .claude/settings.json
claude "explain the authentication flow and identify any security issues"
# Claude can read everything, search the web, but cannot write, edit, or run bash
```

**Scenario 2: Normal feature development**
```bash
cp 3-auto-mode-profiles/standard/settings.json .claude/settings.json
claude "implement the password reset flow"
# Claude can read, write, edit files, run tests — cannot git push or call external URLs
```

**Scenario 3: Pairing session where you want Claude to commit**
```bash
cp 3-auto-mode-profiles/trusted-dev/settings.json .claude/settings.json
claude "implement and commit the rate limiting middleware"
# Claude can commit — cannot force push or deploy
```

**Scenario 4: Cron job running Claude overnight**
```bash
cp 3-auto-mode-profiles/ci-scripted/settings.json .claude/settings.json
./scripts/run-agent-continue.sh my-project
# Full access for the automation script — no interactive prompts
```

### Switching Profiles in 2 Seconds
```bash
# Add these aliases to ~/.zshrc
alias claude-readonly='cp ~/.claude/profiles/conservative.json .claude/settings.json'
alias claude-dev='cp ~/.claude/profiles/standard.json .claude/settings.json'
alias claude-commit='cp ~/.claude/profiles/trusted-dev.json .claude/settings.json'
```

---

## 4. Hooks

### The Problem

CLAUDE.md says "never run rm -rf". Claude follows this instruction... until it's deep in a multi-step task and decides the fastest way to clean up is `rm -rf ./dist`. The instruction is a suggestion. A hook is a hard block.

### Blocking Dangerous Commands (block-rm-rf.sh)

**Scenario:** Claude is cleaning up build artifacts in Auto Mode.

**Without hook:**
```
Claude: Let me clean up the old build files.
$ rm -rf ./dist ./node_modules  ← gone, no warning
```

**With hook installed:**
```
Claude: Let me clean up the old build files.
$ rm -rf ./dist
BLOCKED: rm -rf is not allowed outside /tmp (block-rm-rf.sh)
Claude: I can't run rm -rf here. Instead I'll delete specific files...
```

### Blocking Force Push (block-force-push.sh)

**Without hook:**
```
Claude: Rebasing and pushing...
$ git push --force origin main  ← bye bye main branch history
```

**With hook:**
```
$ git push --force origin main
BLOCKED: git push --force is not allowed (block-force-push.sh)
Claude: Force push is blocked. I'll push to a feature branch instead and open a PR.
```

### Session Context Loading (load-context.sh)

**Without hook:** You open Claude, type "continue", Claude reads nothing and asks what to work on.

**With hook:** Session opens and automatically prints:
```
=== Session Context ===
[continue.md contents]

=== Latest Research ===
[research/findings/latest.md — last 4000 chars]
======================
Claude is ready with full context.
```

### Telegram Notifications (notify-telegram.sh)

Claude is running a 45-minute cron job. You're not watching.

```
[Telegram message at 20:47]
✅ Claude task completed
Project: mcp-apps
Duration: 43 minutes
Last action: Committed "feat: add get_trending_tools endpoint"
```

You check results on your phone without ever opening the terminal.

### Hook Setup Quick Reference

```bash
# 1. Copy hooks
mkdir -p ~/.claude/hooks/pre-tool-call ~/.claude/hooks/session-start
cp pack/4-hooks/pre-tool-call/*.sh ~/.claude/hooks/pre-tool-call/
cp pack/4-hooks/session-start/*.sh ~/.claude/hooks/session-start/
chmod +x ~/.claude/hooks/**/*.sh

# 2. Add Telegram creds (optional)
echo 'export TELEGRAM_BOT_TOKEN="xxx"' >> ~/.zshrc
echo 'export TELEGRAM_CHAT_ID="xxx"' >> ~/.zshrc

# 3. Register in settings.json (see 4-hooks/README.md for the full JSON block)
```

---

## 5. Multi-Agent System

### The Problem

You have 5 side projects. You can only work on them on weekends. Progress is slow because you also spend most of your session re-reading the codebase to remember where you were.

### The Solution

Claude runs every day without you. Research in the morning. Work in the evening. You check the diffs on your phone.

### Daily Automation Example

**crontab.conf (installed once):**
```cron
# 8am: research agent checks competitors, prices, tech news for each project
0 8 * * * /workspace/scripts/run-research.sh mcp-apps
0 8 * * * /workspace/scripts/run-research.sh digital-products

# 8pm: work agent picks up from continue.md and does the next task
0 20 * * * /workspace/scripts/run-agent-continue.sh mcp-apps
0 20 * * * /workspace/scripts/run-agent-continue.sh digital-products

# Sunday 7am: weekly summary across all projects
0 7 * * 0 /workspace/scripts/weekly-summary.sh
```

**You don't touch any of this.** Every morning you check `research/findings/latest.md`. Every evening you check the git log.

### Research Agent (run-research.sh) Example

**research/AGENT.md** (you write this once):
```markdown
## Research Brief — MCP Apps

Search weekly for:
1. New MCP servers launched on GitHub (search: "mcp server site:github.com")
2. Reddit threads about MCP pain points (search: "MCP server problems reddit")
3. Pricing of top-selling Claude extensions on Gumroad

Save findings as:
- Competitor: name, price, review count, gaps
- Pain point: exact user quote + source URL
- Opportunity: specific niche not yet covered
```

**research/findings/2026-04-05.md** (Claude writes this automatically):
```markdown
## Findings — 2026-04-05

### New Competitors
- "mcp-github-stars" — 2.3k stars, no monetization yet
- "mcp-notion-sync" — $12/mo, complaints about auth flow

### Pain Points Found
- r/ClaudeAI: "I wish there was an MCP that automatically categorized my expenses"
  Source: reddit.com/r/ClaudeAI/...

### Opportunity
Expense categorization MCP — no existing solution, 47 upvotes on pain thread
```

### Work Agent (run-agent-continue.sh) Example

**continue.md** before the evening run:
```markdown
## Current Phase
Phase 2 — Building MCP server skeleton

## Next Actions
- [ ] Implement get_trending_tools endpoint
- [ ] Write tests for the tool schema validation
- [ ] Update README with endpoint documentation
```

**After the evening run (git log):**
```
8f3a2c1 feat: implement get_trending_tools endpoint with pagination
4d9b7e2 test: add schema validation tests for tool input
```

Two tasks done while you slept. `continue.md` updated with what's next.

### Manual Run Examples

```bash
# Run a specific task right now
./scripts/run-agent.sh mcp-apps "fix the failing test in tests/test_tools.py"

# Run all priority projects in sequence
./scripts/run-agent-continue.sh all

# Get a cross-project status report
./scripts/run-now.sh status

# Check what the weekly summary looks like
./scripts/weekly-summary.sh
```

---

## 6. 1M Context Optimization

### The Problem

You're 45 minutes into a session. Claude starts forgetting things from earlier. Or it re-reads the same file multiple times. You're burning context on overhead, not progress.

### What Burns Tokens (and how to stop it)

**Problem 1: Claude re-reads files it already loaded**

Add to CLAUDE.md:
```markdown
## Efficiency Rules
- Do not re-read a file you've already seen in this session unless it has likely changed
- Do not read files to answer questions about imports or structure — infer from what you already know
- When in doubt, ask instead of loading another file
```

**Problem 2: Claude explains every step at length**

Add to CLAUDE.md:
```markdown
## Response Style
- Lead with code, not explanation
- Skip "I'll now..." and "As you can see..." preamble
- One-sentence rationale max when I didn't ask why
- No summaries of what you just did — I can read the diff
```

**Problem 3: CLAUDE.md itself is too long**

Your CLAUDE.md is loaded every single turn. 300 lines × 20 turns = 6,000 tokens just on instructions.

Strip examples out of CLAUDE.md into a separate `docs/conventions.md`. Keep CLAUDE.md under 150 lines of pure rules.

### Token Budget Statusline

See `6-1m-context-optimization/token-budget-statusline.md` for how to add this to your terminal:

```
[claude] 47k/200k tokens (23%) ████░░░░░░░░░░░░░░░░
```

Visible feedback. You know when to start a fresh session before Claude starts forgetting context.

### context-trim.md Quick Wins

Copy these sections from `6-1m-context-optimization/context-trim.md` into your CLAUDE.md:

1. **Response Conciseness** — cuts 30-40% of Claude's verbose output
2. **Decision Autonomy** — stops Claude asking for confirmation on trivial choices
3. **File Reading Discipline** — prevents re-reading files Claude already has in context
4. **Session Completion** — ensures Claude saves state before token limit hits

---

## 7. Cross-Platform AGENTS.md

### The Problem

You use Claude Code in the terminal, your team uses Cursor, your CI uses OpenCode. Each tool has different behavior. You maintain three sets of instructions. They drift.

### The Solution

`AGENTS.md` is read by Claude Code, Cursor, OpenCode, and most modern AI coding tools.
One file, consistent conventions across all tools.

**7-cross-platform/go-microservices/AGENTS.md** contains the same conventions as the CLAUDE.md, formatted for maximum cross-tool compatibility:

```markdown
# Agent Instructions — Go Microservices

## Stack
Go 1.22+, pgx/v5, chi router, slog, testify

## Before Every Code Change
1. Read the file you're about to modify
2. Understand what it's doing before changing anything
3. Run existing tests after your change: `go test ./...`

## Code Rules
[same rules as CLAUDE.md, structured for tool-agnostic parsing]
```

**Usage:**
```bash
# Copy to project root — works in Claude Code, Cursor, OpenCode, Continue
cp 7-cross-platform/go-microservices/AGENTS.md /your/project/AGENTS.md
```

One install. Works everywhere your team codes.

---

### React Native Example

**Prompt:** "Show a paginated list of products"

**Without config:**
```tsx
function ProductList() {
  const [products, setProducts] = useState([])
  useEffect(() => { fetchProducts().then(setProducts) }, [])
  return (
    <ScrollView>
      {products.map(p => <ProductCard key={p.id} product={p} />)}
    </ScrollView>
  )
}
```

**With react-native/CLAUDE.md:**
```tsx
function ProductList() {
  const { data, fetchNextPage, hasNextPage, isFetching } = useInfiniteQuery({
    queryKey: ['products'],
    queryFn: ({ pageParam = 1 }) => api.getProducts(pageParam),
    getNextPageParam: (last) => last.nextPage,
  })
  const products = data?.pages.flatMap(p => p.items) ?? []

  return (
    <FlatList
      data={products}
      keyExtractor={(item) => item.id.toString()}
      renderItem={({ item }) => <ProductCard item={item} />}
      onEndReached={() => hasNextPage && fetchNextPage()}
      onEndReachedThreshold={0.5}
      ListFooterComponent={isFetching ? <ActivityIndicator /> : null}
    />
  )
}
```

FlatList (not ScrollView), React Query pagination, proper loading state.

---

### Flutter Example

**Prompt:** "Display a list of items from an API"

**Without config:**
```dart
class ItemListScreen extends StatefulWidget { ... }
class _ItemListState extends State<ItemListScreen> {
  List items = [];
  void initState() {
    super.initState();
    ApiService().getItems().then((data) => setState(() => items = data));
  }
  Widget build(BuildContext context) {
    return Column(children: items.map((i) => Text(i['name'])).toList()); // ← no lazy loading
  }
}
```

**With flutter-dart/CLAUDE.md:**
```dart
@riverpod
class ItemList extends _$ItemList {
  @override
  Future<List<Item>> build() => ref.watch(itemRepositoryProvider).getItems();
}

class ItemListScreen extends ConsumerWidget {
  @override
  Widget build(BuildContext context, WidgetRef ref) {
    final items = ref.watch(itemListProvider);
    return items.when(
      data: (list) => ListView.builder(
        itemCount: list.length,
        itemBuilder: (_, i) => ItemCard(key: ValueKey(list[i].id), item: list[i]),
      ),
      loading: () => const CircularProgressIndicator(),
      error: (e, _) => Text('Error: $e'),
    );
  }
}
```

Riverpod (not setState), ListView.builder (not Column), proper loading/error states.

---

## Buyer Problem → Pack Component Map

| Your Problem | Pack Component |
|---|---|
| "Claude forgets my conventions each session" | `1-stack-configs/` |
| "I write Go and Claude ignores my error handling style" | `1-stack-configs/go-microservices/` |
| "Claude writes TypeScript with any types and default exports" | `1-stack-configs/typescript-node/` |
| "Claude uses Pages Router patterns in my App Router project" | `1-stack-configs/nextjs-react/` |
| "Claude uses .unwrap() everywhere in my Rust code" | `1-stack-configs/rust/` |
| "Claude puts business logic in Spring Boot controllers" | `1-stack-configs/java-spring-boot/` |
| "Claude uses useState+useEffect instead of React Query in React Native" | `1-stack-configs/react-native/` |
| "Claude uses setState instead of Riverpod in Flutter" | `1-stack-configs/flutter-dart/` |
| "Claude blocks the event loop in my FastAPI async routes" | `1-stack-configs/python-fastapi-react/` |
| "Claude calls get_node() inside _process() in Godot" | `1-stack-configs/gdscript-godot4/` |
| "I spend 15 min re-explaining my project every session" | `2-memory-os/` |
| "Claude deleted files / pushed to main in Auto Mode" | `3-auto-mode-profiles/` + `4-hooks/` |
| "I need Claude to run unsupervised without destroying things" | `3-auto-mode-profiles/ci-scripted/` + `4-hooks/` |
| "I want Claude to work on my projects overnight" | `5-multi-agent-system/` |
| "I want market research done automatically each morning" | `5-multi-agent-system/run-research.sh` |
| "Claude is forgetting context mid-session" | `6-1m-context-optimization/` |
| "My team uses Cursor/OpenCode, not just Claude Code" | `7-cross-platform/` |
| "I want a dashboard to track all my projects" | `8-notion-dashboard/` |

---

## Common Questions

**Q: Do I need all 8 folders?**
Start with `1-stack-configs/` and `5-multi-agent-system/`. Those two together cover 80% of the value for most users. Add others as needed.

**Q: Can I use the CLAUDE.md files as-is?**
Yes. They're production-ready. Customize by adding your project-specific rules at the bottom.

**Q: How long does full setup take?**
Starter/Pro: 10 minutes. Elite (all 8 folders): 20 minutes. See `SETUP.md`.

**Q: What if my stack isn't in the configs?**
The 12 configs cover the most common stacks: Go, TypeScript/Node, Next.js, Rust, Java Spring Boot, Python (FastAPI + data pipeline), Kotlin Android, React Native, Flutter, Godot 4, and a workspace config. If yours isn't listed, use `1-stack-configs/side-project-workspace/CLAUDE.md` as the base and add your stack's conventions at the bottom. The structure and patterns transfer across stacks.

**Q: Can the cron agent accidentally break my codebase?**
Use `3-auto-mode-profiles/standard/settings.json` for cron runs — it allows edits and tests but blocks git push and destructive bash commands. Combine with `4-hooks/block-rm-rf.sh` for belt-and-suspenders safety.

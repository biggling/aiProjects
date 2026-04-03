# CLAUDE.md — Python FastAPI + React

## Stack
Python 3.11+, FastAPI, SQLAlchemy 2.x, loguru, React 18, TypeScript, React Query (TanStack Query v5), Vite, WebSocket.

## Commands
```bash
# Backend
uvicorn api.main:app --reload
pytest tests/ -v
mypy api/

# Frontend
cd dashboard && npm install
cd dashboard && npm run dev      # Vite dev server
cd dashboard && npm run build
cd dashboard && npm test         # Vitest

# Both (dev)
bash scripts/dev.sh
```

## Backend Conventions (FastAPI)

### Async Rules
- All route handlers must be `async def`
- Wrap all synchronous SQLAlchemy calls in `asyncio.to_thread()` — never call sync DB code directly from async handlers
- Use `httpx.AsyncClient` for outbound HTTP, never `requests` inside async routes

```python
# Correct
@router.get("/items/{id}")
async def get_item(id: int, db: Session = Depends(get_db)):
    item = await asyncio.to_thread(db.execute, select(Item).where(Item.id == id))
    return item.scalar_one_or_none()

# Wrong
@router.get("/items/{id}")
async def get_item(id: int, db: Session = Depends(get_db)):
    item = db.execute(select(Item).where(Item.id == id))  # blocks event loop
```

### Route Structure
- Routes in `api/routes/` — one file per domain area
- Register routers in `api/main.py` with prefix and tags
- Thin routes: validate input → call service → return response
- No business logic in route handlers
- Use Pydantic models for request/response schemas

### WebSocket
- `api/ws.py` holds a singleton `ConnectionManager`
- Import `manager` from `api/ws.py` — never create a second instance
- Broadcast events: `await manager.broadcast(json.dumps({"type": "...", "data": ...}))`
- React side subscribes via `hooks/useWebSocket.ts` — WebSocket events invalidate React Query keys

### Auth
- All routes require `verify_api_key` dependency except WebSocket and health check
- API key from `Authorization: Bearer <key>` header
- Never put API key in URL query params

### Config
- `VITE_` prefix for frontend env vars
- Backend reads from `os.getenv()` — loaded via `python-dotenv` in dev
- Validate required vars at startup — fail fast

## Frontend Conventions (React + TypeScript)

### State Management
- Server state: React Query only — no Redux/Zustand for server data
- Client UI state: `useState` / `useReducer` — keep local when possible
- No prop drilling beyond 2 levels — use context or co-locate state

### React Query
- All server state fetching in `api/hooks.ts` as custom hooks
- Query keys are arrays: `['items', id]`, `['items', 'list']`
- Invalidate on mutation: `queryClient.invalidateQueries({ queryKey: ['items'] })`
- Use `enabled: false` for queries that depend on user action

```typescript
// hooks.ts pattern
export function useItem(id: number) {
  return useQuery({
    queryKey: ['items', id],
    queryFn: () => apiClient.get<Item>(`/items/${id}`),
  })
}
```

### API Client
- Axios client in `api/client.ts` reads `VITE_API_KEY` from import.meta.env
- Bearer token set in axios default headers — never add manually per-request
- Handle 401 globally in response interceptor

### WebSocket Hook
- `hooks/useWebSocket.ts` manages connection lifecycle
- On message: parse JSON → check `type` field → dispatch to correct invalidation
- Reconnect on disconnect with exponential backoff
- Clean up on component unmount

### Component Conventions
- Functional components only — no class components
- Co-locate styles with components (CSS modules or Tailwind)
- Extract hooks for complex logic — components stay readable
- `interface Props` defined in the same file as the component

### What NOT to Do
- No `useEffect` for data fetching — use React Query
- No `any` in TypeScript — use `unknown` + narrowing
- No synchronous DB calls in async FastAPI routes
- No `console.log` in production — remove before commit
- No direct DOM manipulation — use React state

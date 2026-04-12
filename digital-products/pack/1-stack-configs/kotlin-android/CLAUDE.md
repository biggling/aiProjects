# CLAUDE.md — Kotlin / Android (Jetpack Compose)

## Stack
Kotlin, Jetpack Compose, Android SDK 26+, Room, ViewModel, StateFlow, Hilt, Coroutines, AdMob.

## Commands
```bash
# Build
./gradlew assembleDebug
./gradlew assembleRelease

# Tests
./gradlew test                  # unit tests
./gradlew connectedAndroidTest  # instrumented tests

# Lint
./gradlew lint
./gradlew ktlintCheck

# Install on device
./gradlew installDebug
```

## Code Conventions

### Architecture (MVVM)
```
ui/
  screens/          ← Composable screens, observe ViewModel state only
  components/       ← Reusable Composables, no ViewModel dependency
  theme/            ← MaterialTheme setup
viewmodel/
  FooViewModel.kt   ← StateFlow + UiState, no Android framework in logic
repository/
  FooRepository.kt  ← single source of truth, abstracts Room + network
data/
  local/            ← Room DAOs and entities
  remote/           ← Retrofit/API clients
di/
  AppModule.kt      ← Hilt modules
```

### ViewModel
- Expose state as `StateFlow<UiState>` — never expose `LiveData` in new code
- `UiState` is a sealed class: `Loading`, `Success(data)`, `Error(message)`
- One `collectAsState()` call per screen — subscribe to one state flow
- Use `viewModelScope.launch` for coroutines — auto-cancelled on ViewModel clear
- No Android context in ViewModel — inject Application via `@HiltViewModel` if needed

```kotlin
// Correct UiState pattern
sealed class HomeUiState {
    object Loading : HomeUiState()
    data class Success(val items: List<Item>) : HomeUiState()
    data class Error(val message: String) : HomeUiState()
}

class HomeViewModel @HiltViewModel constructor(
    private val repository: ItemRepository
) : ViewModel() {
    private val _uiState = MutableStateFlow<HomeUiState>(HomeUiState.Loading)
    val uiState: StateFlow<HomeUiState> = _uiState.asStateFlow()
}
```

### Compose
- Composables are stateless where possible — hoist state to ViewModel
- Use `remember` only for UI-local state (scroll position, expanded state)
- Never call `viewModel()` inside a nested Composable — pass state/callbacks down
- Use `LazyColumn` / `LazyRow` for lists — never `Column` with `forEach` for long lists
- `Modifier` param on every reusable Composable: `modifier: Modifier = Modifier`

### Room
- DAO methods return `Flow<T>` for reactive queries, `suspend` for one-shots
- Entities are plain data classes — no business logic in entities
- Use `@Transaction` for queries that read multiple tables
- Never access DAO directly from ViewModel — always go through Repository

```kotlin
// Correct DAO
@Dao
interface ItemDao {
    @Query("SELECT * FROM items ORDER BY created_at DESC")
    fun getAll(): Flow<List<Item>>   // reactive

    @Insert(onConflict = OnConflictStrategy.REPLACE)
    suspend fun insert(item: Item)
}
```

### Coroutines
- `viewModelScope` in ViewModels, `lifecycleScope` in Activities/Fragments
- `Dispatchers.IO` for all DB and network work — never on `Main`
- Use `withContext(Dispatchers.IO)` in Repository methods, not in ViewModel
- Handle exceptions with `try/catch` or `CoroutineExceptionHandler` — never ignore

### Hilt DI
- `@HiltViewModel` for ViewModels
- `@Singleton` for repository and network singletons
- `@ApplicationContext` for context injection — never store Activity context
- Provide Room DB and Retrofit in `AppModule` or `DatabaseModule`

### AdMob
- Initialize `MobileAds.initialize()` once in `Application.onCreate()`
- Load banner ads in `BannerAdView` Composable with `AndroidView`
- Interstitials: load in ViewModel, show from Activity only (never from Composable directly)
- Test ads in debug builds: use test ad unit IDs from Google's docs
- Never show ads on first launch — give user value first

### What NOT to Do
- No `runBlocking` except in tests
- No `GlobalScope` — always use scoped coroutines
- No `findViewById` — Compose only in new screens
- No business logic in Composables
- No hardcoded strings — use `stringResource(R.string.key)`
- No hardcoded dimensions — use `dimensionResource()` or `MaterialTheme.spacing`

## Navigation (Compose Navigation)
- Define all routes as constants in a `Screen` sealed class or object
- Pass only primitive arguments via nav args — load full objects from ViewModel/Repository
- Use `rememberNavController()` at the top-level composable only; pass `NavController` down as a lambda, not the controller itself
- Back stack: use `popUpTo` + `launchSingleTop = true` to avoid duplicate destinations

```kotlin
// Correct — typed route constants
sealed class Screen(val route: String) {
    object Home : Screen("home")
    object Detail : Screen("detail/{itemId}") {
        fun createRoute(itemId: Int) = "detail/$itemId"
    }
}
```

## Permissions
- Request permissions at the moment they're needed, not at app launch
- Use `rememberLauncherForActivityResult(ActivityResultContracts.RequestPermission())` in Compose
- Handle denial gracefully — show rationale, provide a path to settings
- Never assume a permission is granted — always check before use

```kotlin
val launcher = rememberLauncherForActivityResult(
    ActivityResultContracts.RequestPermission()
) { granted ->
    if (!granted) showPermissionRationale()
}
```

## Offline-First / Data Sync
- Room is the single source of truth — UI always reads from Room, never directly from network
- Repository fetches from network, saves to Room, Room emits updated `Flow<T>` to UI
- Use `WorkManager` for background sync that must survive process death
- Mark sync work as `Constraints.Builder().setRequiredNetworkType(NetworkType.CONNECTED)`

## Common Mistakes Claude Makes Without This Config
- Calling `viewModel()` inside nested Composables (creates a new ViewModel per recomposition)
- Using `LiveData` in new code instead of `StateFlow`
- Calling DAO directly from ViewModel instead of via Repository
- Using `runBlocking` in production coroutine code
- Using `GlobalScope.launch` instead of `viewModelScope`
- `Column { items.forEach { ... } }` instead of `LazyColumn` for lists
- Accessing DB on the main thread (missing `withContext(Dispatchers.IO)`)

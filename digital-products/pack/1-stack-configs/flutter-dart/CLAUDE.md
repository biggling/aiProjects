# CLAUDE.md — Flutter / Dart

## Stack
Flutter 3.x, Dart 3.x, Riverpod 2.x (state management), GoRouter (navigation), Dio (HTTP), Freezed (immutable models), Hive or Isar (local DB), flutter_secure_storage.

## Commands
```bash
flutter run                         # run on connected device/emulator
flutter run --flavor dev            # run with dev flavor
flutter test                        # unit + widget tests
flutter test integration_test/      # integration tests
flutter build apk --release         # Android APK
flutter build appbundle --release   # Android AAB (Play Store)
flutter build ipa                   # iOS (requires Mac + Xcode)
flutter analyze                     # static analysis
dart format .                       # format all Dart files
flutter pub get                     # install packages
flutter pub upgrade                 # upgrade packages
```

## Project Structure
```
lib/
  main.dart                 ← entry point, ProviderScope, app setup
  app.dart                  ← MaterialApp + GoRouter setup
  core/
    theme/                  ← ThemeData, colors, text styles
    constants/              ← app-wide constants
    utils/                  ← pure utility functions
    network/                ← Dio client setup, interceptors
  features/
    auth/
      data/                 ← AuthRepository, AuthApiService
      domain/               ← User model (Freezed), auth state
      presentation/         ← LoginScreen, AuthNotifier (Riverpod)
    home/
      data/
      domain/
      presentation/
  shared/
    widgets/                ← reusable widgets (AppButton, AppTextField)
test/
  unit/
  widget/
integration_test/
```

## State Management (Riverpod)

### Provider Types
- `Provider` — synchronous, read-only derived state
- `StateNotifierProvider` — mutable state with a `StateNotifier` class
- `AsyncNotifierProvider` — async state (preferred for data fetching in Riverpod 2)
- `FutureProvider` — simple one-shot async data
- `StreamProvider` — reactive streams (WebSocket, Firestore)

```dart
// Correct — AsyncNotifierProvider for data fetching
@riverpod
class UserList extends _$UserList {
  @override
  Future<List<User>> build() async {
    return ref.watch(userRepositoryProvider).getUsers();
  }

  Future<void> refresh() async {
    state = const AsyncLoading();
    state = await AsyncValue.guard(() => ref.read(userRepositoryProvider).getUsers());
  }
}
```

### Consuming Providers
- `ConsumerWidget` replaces `StatelessWidget` when you need to watch providers
- `ConsumerStatefulWidget` replaces `StatefulWidget`
- Use `ref.watch()` for reactive data, `ref.read()` for one-time reads in callbacks
- Never call `ref.watch()` inside a callback or conditional

```dart
class UserListScreen extends ConsumerWidget {
  @override
  Widget build(BuildContext context, WidgetRef ref) {
    final usersAsync = ref.watch(userListProvider);
    return usersAsync.when(
      data: (users) => ListView.builder(...),
      loading: () => const CircularProgressIndicator(),
      error: (error, stack) => ErrorWidget(error.toString()),
    );
  }
}
```

## Navigation (GoRouter)

```dart
// app.dart
final router = GoRouter(
  initialLocation: '/home',
  redirect: (context, state) {
    final isLoggedIn = ref.read(authProvider).isLoggedIn;
    if (!isLoggedIn && !state.matchedLocation.startsWith('/auth')) {
      return '/auth/login';
    }
    return null;
  },
  routes: [
    GoRoute(path: '/home', builder: (_, __) => const HomeScreen()),
    GoRoute(
      path: '/product/:id',
      builder: (_, state) => ProductScreen(id: state.pathParameters['id']!),
    ),
    ShellRoute(routes: [...]),  // nested navigation / bottom tabs
  ],
);
```

- Use `context.go('/path')` for replacing the stack, `context.push('/path')` for pushing
- Pass only IDs in route params — load full objects from Repository in the destination screen
- Never use `Navigator.push()` directly — route through GoRouter

## Models (Freezed)

Use `Freezed` for all domain models — immutable, with `copyWith`, `==`, `hashCode` for free.

```dart
// user.dart
import 'package:freezed_annotation/freezed_annotation.dart';
part 'user.freezed.dart';
part 'user.g.dart';

@freezed
class User with _$User {
  const factory User({
    required String id,
    required String name,
    required String email,
    @Default(false) bool isPremium,
  }) = _User;

  factory User.fromJson(Map<String, dynamic> json) => _$UserFromJson(json);
}
```

Run `flutter pub run build_runner build --delete-conflicting-outputs` after adding Freezed models.

## HTTP (Dio)

```dart
// core/network/dio_client.dart
final dioProvider = Provider<Dio>((ref) {
  final dio = Dio(BaseOptions(
    baseUrl: AppConstants.baseUrl,
    connectTimeout: const Duration(seconds: 10),
    receiveTimeout: const Duration(seconds: 30),
  ));
  dio.interceptors.add(AuthInterceptor(ref));  // inject Bearer token
  return dio;
});
```

- Always set `connectTimeout` and `receiveTimeout` — never leave them default (no timeout)
- Handle `DioException` in Repository layer, convert to domain errors
- Use interceptors for auth token injection and global error handling
- Never catch `DioException` in UI layer — map to domain errors in Repository

## Local Storage
- `flutter_secure_storage` for sensitive data: tokens, passwords, API keys
- `Hive` or `Isar` for structured local data (cache, offline-first)
- `SharedPreferences` for simple key-value non-sensitive settings only
- Never store tokens in SharedPreferences — use SecureStorage

## Widget Conventions
- Prefer `const` constructors everywhere — improves rebuild performance
- Extract widgets to methods only for very small pieces; extract to classes for anything reusable
- Use `ListView.builder` / `GridView.builder` for lists — never `Column` with `.map().toList()`
- Add `key` to stateful list items to prevent rebuild/animation bugs

```dart
// Correct
ListView.builder(
  itemCount: items.length,
  itemBuilder: (context, index) => ItemCard(key: ValueKey(items[index].id), item: items[index]),
)

// Wrong
Column(children: items.map((item) => ItemCard(item: item)).toList())
```

## Testing
- Widget tests: `testWidgets` + `WidgetTester` — wrap with `ProviderScope` for Riverpod
- Unit tests: standard `test()` — mock Repositories with `Mockito` or `Mocktail`
- Use `ProviderContainer` for testing Riverpod providers in isolation

## Common Mistakes Claude Makes Without This Config
- Using `setState` in new code instead of Riverpod providers
- Calling `ref.watch()` inside an `onPressed` callback (should be `ref.read()`)
- Using `Navigator.push()` instead of `context.go()` / `context.push()`
- `Column` with `.map()` for lists instead of `ListView.builder`
- Missing `const` on widget constructors (performance regression)
- Storing auth tokens in SharedPreferences instead of SecureStorage
- Not generating Freezed code after model changes (`build_runner`)

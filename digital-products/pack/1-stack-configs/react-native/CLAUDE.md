# CLAUDE.md — React Native (Expo + TypeScript)

## Stack
React Native, Expo SDK 51+, TypeScript, Expo Router (file-based routing), React Query (TanStack v5), Zustand, NativeWind (Tailwind for RN), AsyncStorage, React Native Reanimated.

## Commands
```bash
npx expo start               # start dev server (Expo Go or dev build)
npx expo start --ios         # iOS simulator
npx expo start --android     # Android emulator
npx expo run:ios             # build and run native iOS (requires Xcode)
npx expo run:android         # build and run native Android (requires Android Studio)
eas build --platform all     # cloud build via EAS
npx expo lint                # lint
```

## Project Structure (Expo Router)
```
app/
  _layout.tsx             ← root layout (providers, navigation theme)
  (tabs)/
    _layout.tsx           ← tab bar layout
    index.tsx             ← home tab
    profile.tsx           ← profile tab
  (auth)/
    login.tsx
    register.tsx
  [id].tsx                ← dynamic route
components/
  ui/                     ← generic (Button, Input, Card)
  features/               ← domain-specific (ProductCard, OrderItem)
hooks/
  useAuth.ts
  useTheme.ts
lib/
  api.ts                  ← axios/fetch client
  queryClient.ts          ← React Query setup
store/
  auth.ts                 ← Zustand auth store
  ui.ts                   ← Zustand UI state
constants/
  colors.ts
  fonts.ts
assets/
  images/
  fonts/
```

## Navigation (Expo Router)
- File-based routing — folder structure defines the navigation structure
- Use `Link` from `expo-router` for navigation, not `useNavigation().navigate`
- Use `useLocalSearchParams()` for route params — never pass complex objects
- Use `Stack.Screen` options for per-screen header config
- Use `(groups)` for layout sharing without URL segments

```tsx
// Correct navigation
import { Link } from 'expo-router'

<Link href="/profile/123">View Profile</Link>

// Programmatic navigation
import { router } from 'expo-router'
router.push('/checkout')
router.replace('/(auth)/login')  // replace — no back
```

## Components

### Styling (NativeWind)
- Use `className` with Tailwind classes via NativeWind — no inline `style` objects
- For dynamic styles, use `clsx` or `cn` utility
- Platform-specific styles: `Platform.select({ ios: ..., android: ... })`
- Safe area: wrap screen content in `SafeAreaView` or use `useSafeAreaInsets()`

```tsx
// Correct
<View className="flex-1 bg-white px-4 py-6">
  <Text className="text-lg font-bold text-gray-900">{title}</Text>
</View>

// Wrong — inline styles everywhere
<View style={{ flex: 1, backgroundColor: 'white', paddingHorizontal: 16 }}>
```

### FlatList vs ScrollView
- `FlatList` for any list of items — never `ScrollView` with `.map()` for long lists
- Always provide `keyExtractor` returning a stable unique string
- Use `getItemLayout` for fixed-height lists (improves scroll performance)
- Use `ListEmptyComponent` and `ListFooterComponent` for loading/empty states

```tsx
<FlatList
  data={items}
  keyExtractor={(item) => item.id.toString()}
  renderItem={({ item }) => <ItemCard item={item} />}
  ListEmptyComponent={<EmptyState />}
  onEndReached={fetchNextPage}
  onEndReachedThreshold={0.5}
/>
```

## State Management

### Server State — React Query
- All API calls go through React Query hooks in `hooks/`
- Consistent query keys: `['users', userId]`, `['products', 'list', filters]`
- Invalidate on mutation: `queryClient.invalidateQueries({ queryKey: ['users'] })`
- Use `enabled: !!userId` to prevent queries until data is ready

### Client State — Zustand
- Zustand for global UI state (auth, theme, cart) — not for server data
- Keep stores small and focused — one store per domain
- Use `immer` middleware for complex state updates

```typescript
// store/auth.ts
import { create } from 'zustand'
import { persist, createJSONStorage } from 'zustand/middleware'
import AsyncStorage from '@react-native-async-storage/async-storage'

export const useAuthStore = create(
  persist(
    (set) => ({
      token: null as string | null,
      setToken: (token: string) => set({ token }),
      logout: () => set({ token: null }),
    }),
    { name: 'auth', storage: createJSONStorage(() => AsyncStorage) }
  )
)
```

## Permissions
- Request permissions at the moment of use, not at app launch
- Use `expo-permissions` or module-specific permission APIs (`expo-camera`, `expo-location`)
- Show rationale before requesting — explain why the app needs it
- Handle denial gracefully — provide a fallback or link to Settings

```typescript
import * as ImagePicker from 'expo-image-picker'

async function pickImage() {
  const { status } = await ImagePicker.requestMediaLibraryPermissionsAsync()
  if (status !== 'granted') {
    Alert.alert('Permission needed', 'Enable photo access in Settings to upload images.')
    return
  }
  const result = await ImagePicker.launchImageLibraryAsync({ ... })
}
```

## Performance
- Use `React.memo()` for list item components to prevent unnecessary re-renders
- Use `useCallback` for callbacks passed to memoized children
- Use `Reanimated` for smooth animations — never `Animated` from React Native core
- Avoid rendering off-screen content — use `windowSize` prop on FlatList
- Use `InteractionManager.runAfterInteractions()` for non-critical work after navigation

## Offline / Async Storage
- Persist user session and critical data with `AsyncStorage` (via Zustand persist or MMKV)
- Use MMKV (`react-native-mmkv`) for high-frequency reads — 10x faster than AsyncStorage
- Cache API responses in React Query with `staleTime` + `gcTime` for offline resilience
- Show stale data with an indicator when offline — never show an empty screen

## Security
- Never store sensitive data (API keys, secrets) in AsyncStorage — use `expo-secure-store`
- Never put API keys in client-side code — use a backend proxy
- Validate all data received from external sources before using it
- Use HTTPS for all API calls — never HTTP in production

## Common Mistakes Claude Makes Without This Config
- Using `ScrollView` + `.map()` for lists instead of `FlatList`
- Navigating with `useNavigation().navigate` instead of Expo Router's `router.push`
- Requesting all permissions on app launch instead of at point of use
- Using `useState` + `useEffect` for server data instead of React Query
- Putting sensitive data in AsyncStorage instead of SecureStore
- Creating new components with inline style objects instead of NativeWind classes
- Missing `keyExtractor` on FlatList (causes React key warnings and bugs)

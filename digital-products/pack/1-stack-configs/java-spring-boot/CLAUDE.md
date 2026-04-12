# CLAUDE.md — Java / Spring Boot

## Stack
Java 21+, Spring Boot 3.x, Spring Data JPA, Spring Security, Hibernate, PostgreSQL, Maven or Gradle, Lombok, MapStruct, JUnit 5, Mockito.

## Commands
```bash
# Maven
./mvnw spring-boot:run          # run dev server
./mvnw test                     # run all tests
./mvnw verify                   # tests + integration tests
./mvnw clean package            # build jar

# Gradle
./gradlew bootRun               # run dev server
./gradlew test                  # run tests
./gradlew build                 # build jar

# Docker
docker build -t app .
docker run -p 8080:8080 app
```

## Project Structure
```
src/main/java/com/company/app/
  controller/       ← REST controllers (thin — delegate to services)
  service/          ← business logic
  repository/       ← Spring Data JPA interfaces
  domain/           ← JPA entities
  dto/              ← request/response DTOs (Lombok @Data or Java records)
  mapper/           ← MapStruct mappers (entity ↔ DTO)
  config/           ← Spring config classes (@Configuration)
  exception/        ← custom exceptions + @ControllerAdvice handler
src/main/resources/
  application.yml             ← base config
  application-dev.yml         ← dev overrides
  application-prod.yml        ← prod overrides
src/test/java/
  (mirror of main/)           ← tests alongside source
```

## Controller Layer
- Controllers are thin: validate request → call service → return response DTO
- No business logic in controllers — ever
- Use `@RestController` + `@RequestMapping` at class level, specific methods at method level
- Always specify `produces = MediaType.APPLICATION_JSON_VALUE`
- Return `ResponseEntity<T>` to control status codes explicitly

```java
@RestController
@RequestMapping("/api/v1/users")
@RequiredArgsConstructor
public class UserController {

    private final UserService userService;

    @GetMapping("/{id}")
    public ResponseEntity<UserResponse> getUser(@PathVariable Long id) {
        return ResponseEntity.ok(userService.getUser(id));
    }

    @PostMapping
    public ResponseEntity<UserResponse> createUser(@Valid @RequestBody CreateUserRequest request) {
        UserResponse created = userService.createUser(request);
        return ResponseEntity.status(HttpStatus.CREATED).body(created);
    }
}
```

## Service Layer
- Annotate with `@Service` and `@Transactional` at the class level (or specific methods)
- `@Transactional(readOnly = true)` on read-only methods — better performance
- Throw domain-specific exceptions (e.g., `UserNotFoundException`) — never generic `RuntimeException`
- Use constructor injection — never `@Autowired` on fields

```java
@Service
@Transactional
@RequiredArgsConstructor
public class UserService {

    private final UserRepository userRepository;
    private final UserMapper userMapper;

    @Transactional(readOnly = true)
    public UserResponse getUser(Long id) {
        User user = userRepository.findById(id)
            .orElseThrow(() -> new UserNotFoundException(id));
        return userMapper.toResponse(user);
    }
}
```

## Repository Layer
- Extend `JpaRepository<Entity, ID>` — gives CRUD for free
- Use `@Query` with JPQL for complex queries — never native SQL unless necessary
- Use `findBy...` derived method names for simple queries
- Never call `entityManager` directly — use the repository abstraction
- Projection interfaces for read-only partial data — avoid loading full entities for lists

```java
public interface UserRepository extends JpaRepository<User, Long> {
    Optional<User> findByEmail(String email);

    @Query("SELECT u FROM User u WHERE u.createdAt > :since")
    List<User> findRecentUsers(@Param("since") LocalDateTime since);
}
```

## DTOs and Mapping
- Use Java records for immutable request/response DTOs (Java 16+)
- Use Lombok `@Data` for mutable DTOs only
- Map between entity ↔ DTO using MapStruct — never manual mapping in service code
- Validate request DTOs with `@Valid` + Bean Validation annotations (`@NotNull`, `@Email`, etc.)

```java
// Request DTO
public record CreateUserRequest(
    @NotBlank @Size(max = 100) String name,
    @NotNull @Email String email
) {}

// Response DTO
public record UserResponse(Long id, String name, String email, LocalDateTime createdAt) {}
```

## Exception Handling
- Create domain exceptions extending `RuntimeException`
- Handle all exceptions in a single `@RestControllerAdvice` class
- Never expose stack traces to clients — log them, return safe messages
- Return consistent error response structure: `{ "error": "...", "status": 404 }`

```java
@RestControllerAdvice
public class GlobalExceptionHandler {

    @ExceptionHandler(UserNotFoundException.class)
    public ResponseEntity<ErrorResponse> handleNotFound(UserNotFoundException ex) {
        return ResponseEntity.status(HttpStatus.NOT_FOUND)
            .body(new ErrorResponse(ex.getMessage(), 404));
    }

    @ExceptionHandler(Exception.class)
    public ResponseEntity<ErrorResponse> handleGeneric(Exception ex) {
        log.error("Unexpected error", ex);  // full error to logs
        return ResponseEntity.status(HttpStatus.INTERNAL_SERVER_ERROR)
            .body(new ErrorResponse("Internal server error", 500));  // safe to client
    }
}
```

## JPA / Hibernate
- Fetch strategy: `LAZY` by default, `EAGER` only for mandatory associations
- Always use `@Column(nullable = false)` to enforce DB constraints in schema
- Use `@CreatedDate` / `@LastModifiedDate` with `@EntityListeners(AuditingEntityListener.class)`
- Avoid N+1 queries — use `JOIN FETCH` in JPQL or `@EntityGraph` for specific queries
- Use `@Version` for optimistic locking on frequently updated entities

```java
@Entity
@Table(name = "users")
@EntityListeners(AuditingEntityListener.class)
public class User {
    @Id @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    @Column(nullable = false, length = 100)
    private String name;

    @Column(nullable = false, unique = true)
    private String email;

    @CreatedDate
    @Column(updatable = false)
    private LocalDateTime createdAt;
}
```

## Testing
- Use `@SpringBootTest` for integration tests — loads full context
- Use `@WebMvcTest(Controller.class)` for controller unit tests — fast, no DB
- Use `@DataJpaTest` for repository tests — uses in-memory H2
- Mock services with `@MockBean` in controller tests
- Use `@Sql` to seed test data for repository tests

```java
@WebMvcTest(UserController.class)
class UserControllerTest {

    @Autowired private MockMvc mockMvc;
    @MockBean private UserService userService;

    @Test
    void getUser_returnsUser() throws Exception {
        given(userService.getUser(1L)).willReturn(new UserResponse(1L, "Alice", "alice@example.com", now()));

        mockMvc.perform(get("/api/v1/users/1"))
            .andExpect(status().isOk())
            .andExpect(jsonPath("$.name").value("Alice"));
    }
}
```

## Security
- Use Spring Security — never roll your own auth
- Store passwords with `BCryptPasswordEncoder` — never MD5, SHA1, or plaintext
- Use `@PreAuthorize("hasRole('ADMIN')")` for method-level security
- JWT validation in a `OncePerRequestFilter` — validate signature, expiry, and claims
- CORS: configure explicitly in `SecurityFilterChain` — never `*` in production

## Configuration
- Use `application.yml` over `application.properties` — more readable for nested config
- Use `@ConfigurationProperties` for typed config binding — not `@Value` for groups of related props
- `spring.jpa.open-in-view=false` — always disable (prevents lazy loading in views, N+1 issues)
- Activate profiles with `spring.profiles.active=dev` env var — never hardcode

## Common Mistakes Claude Makes Without This Config
- Putting business logic in controllers instead of service layer
- Using `@Autowired` on fields instead of constructor injection
- Missing `@Transactional` on service methods that write to the DB
- N+1 queries from lazy loading in loops — always use `JOIN FETCH`
- Not using `@Valid` on request body parameters — skips bean validation
- Using `findAll()` without pagination — loads entire table into memory
- Exposing JPA entities directly as API responses (leaks internal structure, triggers lazy loads)

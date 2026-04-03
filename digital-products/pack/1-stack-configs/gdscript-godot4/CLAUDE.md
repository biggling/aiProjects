# CLAUDE.md — GDScript / Godot 4

## Stack
Godot 4.x, GDScript, 2D game, exported to Windows/Mac/Linux/Web.

## Commands
```bash
# From project root (Godot CLI)
godot --headless --export-debug "Linux/X11" builds/game.x86_64
godot --headless --export-release "Web" builds/web/index.html

# Run tests (GUT framework if used)
godot --headless -s addons/gut/gut_cmdln.gd
```

## Project Structure
```
scenes/
  main/             ← main scene, game controller
  ui/               ← HUD, menus, overlays
  entities/         ← player, enemies, projectiles
  levels/           ← level scenes
scripts/
  entities/         ← attached scripts for entity scenes
  ui/               ← UI logic scripts
  autoloads/        ← singletons (GameManager, AudioManager, SaveManager)
data/
  items.json        ← game data, loaded at startup
  enemies.json
assets/
  sprites/
  audio/
  fonts/
```

## Code Conventions

### Scene + Script Structure
- One script per scene — scripts attach to the root node of their scene
- Scene files (`.tscn`) are source-controlled — never regenerate a scene from script alone
- Keep scenes focused: one scene = one entity/concept
- Instantiate scenes with `load("res://scenes/foo/Foo.tscn").instantiate()` — not `preload` in loops

### Signals Over Direct References
- Communicate upward via signals — never call parent methods directly
- Children emit signals; parents/autoloads connect and respond
- Define all signals at top of script: `signal health_changed(new_health: int)`
- Use typed signals (Godot 4): `signal enemy_died(enemy: Enemy)`

```gdscript
# Wrong — tight coupling
func take_damage(amount):
    health -= amount
    get_parent().get_node("HUD").update_health(health)  # BAD

# Correct — signal-based
func take_damage(amount):
    health -= amount
    health_changed.emit(health)  # HUD connects to this signal
```

### Node References
- Never use `get_node()` or `$NodePath` inside `_process()` or `_physics_process()` — cache in `_ready()`
- Use `@onready var` for node references: `@onready var sprite: Sprite2D = $Sprite2D`
- Use `@export var` for designer-editable properties
- Check for null before using nodes that may not exist: `if is_instance_valid(node):`

```gdscript
# Correct
@onready var sprite: Sprite2D = $Sprite2D
@onready var collision: CollisionShape2D = $CollisionShape2D

func _process(delta):
    sprite.position += velocity * delta  # cached reference — OK
```

### _ready() vs _process()
- `_ready()`: cache node refs, connect signals, load data, initialize state
- `_process(delta)`: per-frame logic only — keep it fast, no allocations
- `_physics_process(delta)`: physics and movement only
- Never yield/await inside `_process()` — use state machines or timers

### Resource Preloading
- Use `preload()` for resources known at edit time (scripts, small textures)
- Use `load()` inside `_ready()` or background loading for large assets
- Never `load()` inside `_process()` — causes frame hitches
- Store loaded resources in `const` or `@export` — don't reload each frame

### Autoloads (Singletons)
- Register in Project Settings → Autoload
- Use for: game state, audio management, save system, event bus
- Keep autoloads thin — business logic belongs in scene scripts
- Event bus pattern: `EventBus.emit_signal("player_died")` — decouples scenes

### Data (JSON)
- Game data (items, enemies, levels) lives in `data/*.json`
- Load once at startup in an autoload: `GameData.load_all()`
- Access via typed dictionary or a Resource class — not raw JSON dicts throughout code
- Never hardcode game values (damage, speed, prices) in scripts

### Performance
- Pool frequently spawned objects (bullets, particles) — don't `queue_free` + `instantiate` every frame
- Use `Callable` for deferred calls: `call_deferred("method_name")`
- Profile with Godot's built-in profiler before optimizing — don't guess

### What NOT to Do
- No `get_node()` calls in `_process()` — cache in `_ready()`
- No circular scene references — use signals or autoloads to break cycles
- No `print()` in shipped builds — use `push_warning()` / `push_error()` or `#DEBUG` guards
- No business logic in UI scenes — UI emits signals, game logic responds
- No hardcoded screen positions — use anchors and containers

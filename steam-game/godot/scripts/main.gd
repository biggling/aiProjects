extends Node2D
## Main game controller — manages game state and transitions.

enum GameState { MENU, SPINNING, RESOLVING, SHOPPING, GAME_OVER }

var state: GameState = GameState.MENU
var wave: int = 1
var gold: int = 0
var player_hp: int = 100
var max_hp: int = 100

@onready var reel_manager = $ReelManager
@onready var enemy_spawner = $EnemySpawner
@onready var ui = $UI

func _ready():
	state = GameState.MENU
	_update_ui()

func _input(event):
	if event.is_action_pressed("spin") and state == GameState.MENU:
		_start_spin()

func _start_spin():
	state = GameState.SPINNING
	reel_manager.spin()

func _on_reels_stopped(results: Array):
	state = GameState.RESOLVING
	var combos = _detect_combos(results)
	_resolve_combos(combos)

func _detect_combos(results: Array) -> Array:
	"""Detect matching sigils across reels."""
	var combos = []
	# Check each row for matches
	for row in range(results[0].size()):
		var sigils = []
		for reel in results:
			sigils.append(reel[row])

		# Count matches
		var counts = {}
		for s in sigils:
			counts[s] = counts.get(s, 0) + 1

		for sigil_type in counts:
			if counts[sigil_type] >= 2:
				combos.append({
					"sigil": sigil_type,
					"count": counts[sigil_type],
					"row": row,
				})

	return combos

func _resolve_combos(combos: Array):
	"""Apply spell effects from sigil combos."""
	for combo in combos:
		var power = combo.count  # 2=weak, 3=normal, 4=strong, 5=ultimate
		match combo.sigil:
			"fire":
				_deal_damage(10 * power)
			"ice":
				_slow_enemies(2.0 * power)
			"lightning":
				_chain_damage(8 * power, min(power, 3))
			"nature":
				_heal(5 * power)
			"shield":
				_add_shield(power)

	state = GameState.MENU
	_update_ui()

func _deal_damage(amount: int):
	if enemy_spawner:
		enemy_spawner.damage_front(amount)

func _slow_enemies(duration: float):
	if enemy_spawner:
		enemy_spawner.slow_all(duration)

func _chain_damage(amount: int, targets: int):
	if enemy_spawner:
		enemy_spawner.chain_damage(amount, targets)

func _heal(amount: int):
	player_hp = min(player_hp + amount, max_hp)

func _add_shield(stacks: int):
	# Shield absorbs next N hits
	pass

func _on_enemy_reached_player(damage: int):
	player_hp -= damage
	if player_hp <= 0:
		state = GameState.GAME_OVER
	_update_ui()

func _on_enemy_killed(reward: int):
	gold += reward
	_update_ui()

func _update_ui():
	if ui:
		ui.update_display(wave, gold, player_hp, max_hp, state)

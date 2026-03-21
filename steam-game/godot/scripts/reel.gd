extends Node2D
## Single reel — spins and stops on random sigils.

signal stopped(results: Array)

const SIGIL_TYPES = ["fire", "ice", "lightning", "nature", "shield"]
const VISIBLE_SLOTS = 3
const SPIN_SPEED = 800.0  # pixels per second
const DECELERATION = 400.0

var spinning := false
var spin_velocity := 0.0
var target_stop := false
var current_sigils: Array = []

func _ready():
	_randomize_sigils()

func _randomize_sigils():
	current_sigils.clear()
	for i in range(VISIBLE_SLOTS):
		current_sigils.append(SIGIL_TYPES[randi() % SIGIL_TYPES.size()])

func spin():
	spinning = true
	spin_velocity = SPIN_SPEED
	# Stop after random delay
	var delay = randf_range(0.8, 2.0)
	get_tree().create_timer(delay).timeout.connect(_begin_stop)

func _begin_stop():
	target_stop = true

func _process(delta):
	if not spinning:
		return

	if target_stop:
		spin_velocity -= DECELERATION * delta
		if spin_velocity <= 0:
			spin_velocity = 0
			spinning = false
			target_stop = false
			_randomize_sigils()
			stopped.emit(current_sigils.duplicate())
			return

	# Visual: move sigil sprites (to be connected to actual sprites)
	# For now, just the logic backbone

func get_results() -> Array:
	return current_sigils.duplicate()

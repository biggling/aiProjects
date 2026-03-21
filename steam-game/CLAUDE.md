# CLAUDE.md

## Project Purpose
Indie game for Steam — roguelike slot machine ("Sigil Spin"). Combine magical sigils on spinning reels to cast spells against waves of enemies.

## Commands
```bash
# Open in Godot 4
godot --path godot/

# Run from command line
godot --path godot/ --scene scenes/Main.tscn
```

## Architecture

### Game Design
- **Genre:** Roguelike + slot machine hybrid
- **Core loop:** Spin reels → sigils form spell combos → spells hit enemies → earn gold → upgrade sigils → repeat
- **Fun in 30 seconds:** Pull the lever, watch sigils align, enemies explode
- **Target:** $4.99, 30-60 min runs, infinite replayability via sigil synergies

### Godot Project Structure
```
godot/
├── project.godot
├── scenes/          # .tscn scene files
├── scripts/         # .gd GDScript files
├── assets/          # sprites, audio, fonts
└── data/            # JSON balance configs
```

### Key Conventions
- Godot 4 + GDScript
- Pixel art or minimalist vector style
- Game data/balance in JSON files (easy to tweak)
- Core mechanic first, polish later

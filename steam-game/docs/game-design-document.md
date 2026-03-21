# Sigil Spin — Game Design Document

## Elevator Pitch
A roguelike slot machine where you spin magical sigils to cast spells against waves of enemies. Think "Luck Be a Landlord" meets "Vampire Survivors" — simple input, deep strategy, explosive results.

## Core Loop
```
SPIN REELS → MATCH SIGILS → CAST SPELLS → DAMAGE ENEMIES → EARN GOLD → UPGRADE/BUY SIGILS → REPEAT
```

## Mechanics

### Reels
- 3 reels with 5 visible slots each
- Player pulls lever (spacebar or click)
- Reels spin and stop sequentially (left → right)
- Matching sigils on paylines trigger spell effects

### Sigils (5 base types)
| Sigil | Element | Effect | Color |
|-------|---------|--------|-------|
| 🔥 Flame | Fire | Damage single enemy | Red |
| ❄️ Frost | Ice | Slow all enemies | Blue |
| ⚡ Bolt | Lightning | Chain damage 3 enemies | Yellow |
| 💚 Leaf | Nature | Heal player | Green |
| 🛡️ Ward | Shield | Block next hit | White |

### Combos
- **3 matching:** Standard spell cast
- **4 matching:** Enhanced spell (2x effect)
- **5 matching (jackpot):** Ultimate spell (screen-wide effect)
- **Mixed pairs:** Fusion spells (fire + ice = steam cloud AoE)

### Enemies
- Approach from right side of screen
- Each has HP bar, speed, damage
- Wave-based with increasing difficulty
- Boss every 5 waves

### Progression (per run)
- Gold earned from kills
- Between waves: shop appears
  - Buy new sigils (add to reel pool)
  - Upgrade existing sigils (better effects)
  - Remove unwanted sigils (curate your pool)
  - Buy relics (passive bonuses)

### Meta-progression
- Unlock new sigil types across runs
- Achievement-based unlocks
- No permanent power upgrades (pure skill + strategy)

## Art Direction
- **Style:** Clean pixel art, 16-bit inspired
- **Resolution:** 1920x1080
- **Palette:** Dark fantasy with vibrant spell effects
- **UI:** Large, readable, slot machine aesthetic with magical theme

## Technical
- **Engine:** Godot 4
- **Language:** GDScript
- **Target:** Windows/Mac/Linux via Steam
- **Min spec:** Any PC from the last 10 years

## Scope
- **MVP:** 5 sigils, 10 enemies, 1 boss, 10 waves, basic shop
- **Full:** 20+ sigils, 10+ enemies, 5 bosses, 50 waves, full meta
- **Solo dev estimate:** MVP in 2-3 months, full in 6 months

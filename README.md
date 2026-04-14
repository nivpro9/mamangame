# 🕹️ Retro Arcade Machine

A retro arcade machine built in Python + Pygame, featuring 4 classic games with neon LED styling.

## Games
| Game | Controls |
|------|----------|
| **Pac-Man** | Arrow Keys to move, eat dots, avoid ghosts |
| **Galaga** | ←/→ Move, SPACE Shoot |
| **Donkey Kong** | ←/→/↑/↓ Move, SPACE/UP Jump |
| **Street Fighter II** | A/D Move, W Jump, J Punch, K Kick, L Block |

## Features
- Name entry screen
- Neon LED arcade machine UI with particle effects
- High score leaderboard (saved to JSON)
- Scanline CRT effect
- Animated starfield background

## Requirements
```
pip install pygame
```

## Run
```
python main.py
```

## Files
```
main.py          - Arcade machine UI, name entry, menu, scoreboard
scores.py        - JSON-based high score management
pacman.py        - Pac-Man with maze, ghosts, power pellets
galaga.py        - Space shooter with dive-bombing enemies
donkey_kong.py   - Platformer with barrels and ladders
street_fighter.py - 1v1 fighting game vs CPU
```

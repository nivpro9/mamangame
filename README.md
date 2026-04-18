# Paper Airplane ✈️

A mobile-first browser game — fly your paper airplane through 70 levels across 7 biomes. Dodge pillars, collect coins, unlock vehicles, and land on the runway!

## Play

Open `web/index.html` in any modern browser, or serve the `web/` folder:

```
python server.py
```

Then open `http://localhost:8000` on your phone or desktop.

## How to Play

| Action | Mobile | Desktop |
|--------|--------|---------|
| Fly up | Hold screen | Hold mouse |
| Fall | Release | Release |
| Shoot cannon | Double-tap | Double-click |

## Features

- **70 levels** across 7 biomes: Sky, Sunset, Night, Storm, Arctic, Canyon, Space
- **10 vehicles** — Paper Plane, Drone, Rocket, B-2 Spirit, and more
- **Upgrades** — Engine, Control, Magnet, Shield, Cannon
- **Enemies** with homing missiles (level 25+)
- **Mystery boxes** with random prizes
- **Coin combos** and biome-colored coins
- **Prestige system** — restart after level 70 with a star
- **8 languages** — EN, IT, FR, RU, JA, ZH, HE, AR
- **PWA** — installable on iOS/Android home screen
- **Triple-layer save** — localStorage + sessionStorage + cookie

## Project Structure

```
web/
  index.html          — Game UI and screens
  css/style.css       — Mobile-first styling
  js/game.js          — Full game engine (single file)
  manifest.json       — PWA manifest
  icons/              — App icons (SVG, 192px, 512px, apple-touch-icon)
server.py             — Simple local HTTP server
make-icons.ps1        — PowerShell script to generate PNG icons
```

## Vehicles

| Vehicle | Cost | Perk |
|---------|------|------|
| Paper Plane | Free | Standard all-rounder |
| Upgraded Paper | 135 | Coin magnet +40% |
| Drone | 360 | Gravity halved |
| Light Plane | 810 | Tighter turns |
| Propeller Plane | 1620 | Fan gusts -60% |
| Rocket | 2880 | Speed burst |
| Small Airliner | 4500 | Coins worth +2 |
| Large Airliner | 7200 | Free shield per level |
| Stealth Plane | 10800 | Missiles miss 50% |
| B-2 Spirit | 16200 | Auto-fires cannon |

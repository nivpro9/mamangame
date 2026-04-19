# Paper Airplane ✈️

A mobile-first browser game — fly your paper airplane through 70 levels across 7 biomes. Dodge pillars, collect coins, unlock vehicles, and land on the runway!

## Play

```
python server.py
```

Then open `http://localhost:8080` on your phone or desktop.

**Live:** [nivpro9.github.io/Paper-airplane](https://nivpro9.github.io/Paper-airplane/)

## How to Play

| Action | Mobile | Desktop |
|--------|--------|---------|
| Fly up | Hold screen | Hold mouse |
| Fall | Release | Release |
| Shoot cannon | Tap 🔫 button | Double-click |

## Features

- **70 levels** across 7 biomes: Sky, Sunset, Night, Storm, Arctic, Canyon, Space
- **10 vehicles** — Paper Plane, Drone, Rocket, Stealth, Super Airflight, and more
- **Upgrades** — Engine, Control, Magnet, Shield, Cannon
- **Revive system** — continue after crashing with coins (100→200→300) or watch an ad (up to 3×)
- **Balloon targets** — shoot colorful balloons for bonus coins (level 3+)
- **Enemies** with homing missiles (level 25+) and Boss battles every 10 levels
- **Mystery boxes** — random prizes including coins, ammo, shield, speed, vehicles, and 💎 diamonds
- **Diamonds** 💎 — premium currency earned from mystery boxes
- **Daily Spin** — spin the wheel for prizes every 24 hours
- **Coin combos** and biome-colored coins
- **Prestige system** — restart after level 70 with a star
- **8 languages** — EN, IT, FR, RU, JA, ZH, HE, AR
- **PWA** — installable on iOS/Android, ready for Google Play via PWABuilder
- **Triple-layer save** — localStorage + sessionStorage + cookie

## Monetization (ready for stores)

- **Interstitial ads** — shown every 7 games (AdMob placeholder, ready to connect)
- **Rewarded ads** — watch ad to revive (up to 3× per session)
- Connect AdMob by replacing placeholder calls in `AdManager` inside `game.js`

## Project Structure

```
index.html          — Game UI and screens
css/style.css       — Mobile-first styling
js/game.js          — Full game engine (single file)
manifest.json       — PWA manifest (ready for PWABuilder → Google Play)
sw.js               — Service worker (offline support)
icons/              — App icons (SVG, 192px, 512px, apple-touch-icon)
server.py           — Simple local HTTP server
Procfile            — Deployment config (Render/Railway)
```

## Vehicles

| Vehicle | Cost | Perk |
|---------|------|------|
| Paper Plane | Free | Standard all-rounder |
| Upgraded Paper | 135 🪙 | Coin magnet +40% |
| Drone | 360 🪙 | Gravity halved |
| Light Plane | 810 🪙 | Tighter turns |
| Propeller Plane | 1,620 🪙 | Fan gusts -60% |
| Rocket | 2,880 🪙 | Speed burst |
| Small Airliner | 4,500 🪙 | Coins worth +2 |
| Large Airliner | 7,200 🪙 | Free shield per level |
| Stealth Plane | 10,800 🪙 | Missiles miss 50% |
| Super Airflight | 16,200 🪙 | Auto-fires cannon |

## Publishing to Google Play

1. Go to [pwabuilder.com](https://www.pwabuilder.com)
2. Enter `https://nivpro9.github.io/Paper-airplane/`
3. Click **Package for Stores → Google Play**
4. Upload the generated AAB to [Google Play Console](https://play.google.com/console)

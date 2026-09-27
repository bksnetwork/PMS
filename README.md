# PMS — Pokémon Management System

Public-safe Pokémon GO collection manager.

## Goals
- Living Dex / collector-first inventory tracking
- National Pokédex and region/generation completion
- Individual Pokémon stats, forms, visually distinct gender variants, shiny, costume/event, Shadow/Purified, Lucky, legacy/@special moves, tags, research reservations, and PvE/PvP roles
- Resource ledger for Stardust, Candy/XL Candy, balls, berries, TMs, evolution items, incubators, etc.
- Cleanup recommendations that only mark true surplus duplicates
- GitHub Pages dashboard with Pokémon artwork

## Privacy boundary
This repository is public. It must contain Pokémon/game data only. Do **not** commit trainer identity, email, phone, workplace, addresses, precise catch locations, raw screenshots, tokens, or unrelated POD data.

## Public site
GitHub Pages deploys the `public/` folder through `.github/workflows/pages.yml`.

## Local database
```bash
python3 server.py
```
Then open http://127.0.0.1:8765

The local SQLite database is ignored by Git and is not published.

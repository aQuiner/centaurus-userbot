# Centaurus Telegram UserBot

A lightweight Telegram userbot built on Python (Telethon-based), designed as a modular runtime system.

This ain't a “feature bot” — it's a core that boots a Telegram client and lets modules do literally everything else.

![Centaurus Banner](banner.png)

---

## What this is

Centaurus is basically a small userbot framework.

It:

- spins up a Telegram client via Telethon
- handles auth (phone / code / 2FA if needed)
- loads modular plugins ("cogs")
- lets you extend everything without touching core

Think of it like a plugin runtime for Telegram automation.

---

## How it works

### Boot process

Entry point starts in `main.py`.

It kicks off async runtime from `bot.py`, and the whole system comes alive.

---

### Telegram client

Handled in `bot.py` using Telethon.

Flow:

- connect to Telegram
- login via phone/code/password
- restore session if exists
- keep persistent connection alive

Once auth is done → modules get loaded.

---

### Config system

`config.py` pulls settings from `cfg.json`:

- API ID
- API Hash
- session name

Simple flat config, no overengineering.

---

### Module loader

`loader.py` scans `/cogs` folder and auto-loads every `.py` file as a module.

Each module must expose a `setup()` function.

That’s it — drop file in folder, it gets picked up.

---

### Logging

`log.py` is a lightweight colored logger.

Nothing fancy, just clean runtime visibility for startup + errors.

---

## Remote module (the spicy part)

`remote.py` turns the bot into a dynamic module manager.

It allows controlling modules directly from Telegram.

### Commands

- `.load` → load module from URL
- `.list` → show loaded modules
- `.unload` → remove module

---

### How `.load` works internally

When triggered, it:

- downloads Python source from a URL
- strips comments / cleanup
- saves it into modules folder
- installs dependencies via pip (if needed)
- imports module dynamically
- runs `setup()` if exists

So yeah — it’s basically runtime plugin injection.

---

## Architecture overview

The project is split clean:

- `main.py` → entry point
- `bot.py` → Telegram client + runtime
- `config.py` → config loader
- `loader.py` → module system
- `log.py` → logger
- `remote.py` → dynamic module manager
- `/cogs` → extensions

Nothing bloated. Each file has one job.

---

## What’s good

- clean separation of logic
- lightweight core
- modular design
- easy to extend
- no framework dependency hell
- dynamic plugin loading (hot reload style)

---

## Tradeoffs

Not everything is perfect:

- dynamic loading can get unpredictable
- broad exception handling in some places
- no automated tests
- config is external (cfg.json required)

---

## TL;DR

It’s a Telegram userbot core.

- Telethon client
- modular plugin system
- hot-loadable modules via Telegram
- lightweight and extendable runtime

Drop modules in → bot runs them → done.

---

## Closing

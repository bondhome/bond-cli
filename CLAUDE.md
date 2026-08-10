# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Bond CLI is a Python command-line tool for interacting with Bond Home automation devices. It provides commands for device discovery, management, firmware upgrades, and diagnostics.

## Development Commands

### Setup
```bash
pip install -e "."                    # Install in editable mode
pip install -r requirements-test.txt  # Install test dependencies
```

### Testing
```bash
pytest                                # Run all tests with coverage
pytest bond/database/test_database.py # Run specific test file
pytest -k "test_name"                 # Run tests matching pattern
```

### Linting
```bash
flake8 . --count --max-line-length=127 --statistics
```

### Running the CLI
```bash
bond discover                         # Find Bonds on network
bond select <bond-id>                 # Select active Bond
bond -h                               # Show all commands
```

## Architecture

### Command System
Commands are registered in `bond/app.py` and live in `bond/commands/`. Each command module exposes:
- `help` / `description` - Help text
- `run(args)` - Execution function
- `setup(parser)` - Optional argparse setup
- `arguments` - Dict of argument definitions
- `subcommands` - List of nested subcommands (for commands like `devices`, `groups`, `wifi`)

### Protocol Layer (`bond/proto/`)
- `http.py` - HTTP transport to Bond REST API (`/v2/` endpoints)
- `mdns.py` - mDNS discovery using zeroconf (`_bond._tcp.local.`)
- `wye.py` - High-level facade exposing `get()`, `post()`, `put()`, `patch()`, `delete()`
- `base_transport.py` - Async support via `request_async()` with callbacks

### State Management (`bond/database/`)
Singleton JSON database at `~/.bond/db.json` stores:
- Selected Bond ID
- Discovered Bond metadata (IP, port, token)
- Per-Bond settings

Uses `MutableMapping` interface with thread-safe RLock.

### CLI Framework (`bond/cli/`)
- `main.py` - argparse-based command dispatcher
- `console.py` - Thread-safe queue-based output with ANSI color support
- `table.py` - Fixed-width table formatting

## Key Patterns

**Adding a new command**: Create module in `bond/commands/`, register in `bond/app.py` via `load_command()`.

**Async requests**: Use `request_async(method, bondid, on_success=callback, on_error=callback)` from protocol layer.

**Token authentication**: Token passed in `BOND-Token` header. Can be retrieved via PIN unlock or set manually.

## CI/CD

- Tests run on Python 3.7, 3.8, 3.9
- Releases: bump version in `setup.py`, create annotated git tag (`git tag -a "vX.Y.Z"`), push to trigger PyPI deployment

## Claude Code Plugin

This repository is also a Claude Code plugin for natural language control of Bond Home devices.

### Installation

```
/plugin add bondhome/bond-cli
```

### Usage

After installation, use natural language to control devices:

- "Turn on the bedroom fan"
- "Set living room fan to speed 3"
- "Open the office shades"
- "Turn off all lights"
- "What's the status of my devices?"

### Skill Structure

- `skills/assistant/SKILL.md` - Core skill with common operations
- `skills/assistant/references/` - Detailed reference documents for specific domains:
  - `discovery-auth.md` - mDNS discovery, token retrieval
  - `actions-fan.md` - Ceiling fan actions
  - `actions-shades.md` - Motorized shade actions
  - `actions-light.md` - Light actions
  - `actions-fireplace.md` - Fireplace/heater actions
  - `device-types.md` - Device type reference
  - `groups-scenes.md` - Multi-device control
  - `schedules.md` - Time-based automation
  - `system.md` - System operations
  - `troubleshooting.md` - Error diagnosis

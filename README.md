# Claude Setup

My personal Claude Code configuration — custom skills, settings, and dotfiles, packaged with a cross-platform installer.

## What's Included

### Skills

| Skill | Description |
|---|---|
| **caveman** | Ultra-compressed communication mode. Cuts token usage ~75%. |
| **find-skills** | Helps discover and install agent skills from the ecosystem. |
| **grill-me** | Stress-tests plans and designs by interviewing you relentlessly. |
| **arch-coach** | Architectural Review Coach. Tests you on code review skills across 6 exercise types and 5 languages. |

### Config

- `settings.json` — Global Claude Code settings (theme, model)
- `CLAUDE.md` — Global instructions applied to every project

## Installation

```bash
# Clone the repo
git clone https://github.com/Castiaan/claude-setup.git
cd claude-setup

# Run the installer
python install.py
```

Existing files in `~/.claude/` are automatically backed up before being overwritten.

### Options

```bash
python install.py --dry-run    # Preview without making changes
python install.py --help       # Show full help
```

## Cross-Platform

Works on **Windows**, **macOS**, and **Linux**. The installer uses only the Python standard library — no dependencies required.

## Restoring Backups

Each install creates a timestamped backup in `~/.claude/backup/`. To restore:

```bash
cp -r ~/.claude/backup/20250706_123456/* ~/.claude/
```

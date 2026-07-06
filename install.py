#!/usr/bin/env python3
"""
Claude Setup Installer — cross-platform (Windows, macOS, Linux).

Copies custom skills and config files from this repo into ~/.claude/,
with automatic backup of any existing files.

Usage:
    python install.py          # Install everything
    python install.py --dry-run  # Preview without making changes
    python install.py --help     # Show this help
"""

import argparse
import shutil
import sys
from datetime import datetime
from pathlib import Path

# ── Paths ──────────────────────────────────────────────────────────────────

REPO_ROOT = Path(__file__).resolve().parent
CLAUDE_DIR = Path.home() / ".claude"
SKILLS_SRC = REPO_ROOT / "skills"
CONFIG_SRC = REPO_ROOT / "config"
BACKUP_DIR = CLAUDE_DIR / "backup" / datetime.now().strftime("%Y%m%d_%H%M%S")

# ── What to install ────────────────────────────────────────────────────────

SKILLS = ["caveman", "find-skills", "grill-me"]
CONFIG_FILES = ["settings.json", "CLAUDE.md"]


# ── Helpers ────────────────────────────────────────────────────────────────

def green(text: str) -> str:
    return f"\033[92m{text}\033[0m"


def yellow(text: str) -> str:
    return f"\033[93m{text}\033[0m"


def red(text: str) -> str:
    return f"\033[91m{text}\033[0m"


def dim(text: str) -> str:
    return f"\033[90m{text}\033[0m"


def backup_file(path: Path, dry_run: bool) -> None:
    """Copy an existing file to the backup directory."""
    if not path.exists():
        return
    rel = path.relative_to(CLAUDE_DIR)
    dest = BACKUP_DIR / rel
    if not dry_run:
        dest.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(path, dest)
    print(f"  {yellow('backup')}  {path} -> {dest}")


def install_skill(name: str, dry_run: bool) -> bool:
    """Install a single skill. Returns True if successful."""
    src = SKILLS_SRC / name / "SKILL.md"
    dst = CLAUDE_DIR / "skills" / name / "SKILL.md"

    if not src.exists():
        print(f"  {red('skipped')}  {name} (source not found: {src})")
        return False

    # Backup existing
    if dst.exists():
        backup_file(dst, dry_run)

    # Install
    dst.parent.mkdir(parents=True, exist_ok=True)
    if not dry_run:
        shutil.copy2(src, dst)
    print(f"  {green('install')}  {name} -> {dst}")
    return True


def install_config(filename: str, dry_run: bool) -> bool:
    """Install a single config file. Returns True if successful."""
    src = CONFIG_SRC / filename
    dst = CLAUDE_DIR / filename

    if not src.exists():
        print(f"  {red('skipped')}  {filename} (source not found: {src})")
        return False

    # Backup existing
    if dst.exists():
        backup_file(dst, dry_run)

    # Install
    if not dry_run:
        shutil.copy2(src, dst)
    print(f"  {green('install')}  {filename} -> {dst}")
    return True


# ── Main ───────────────────────────────────────────────────────────────────

def main() -> None:
    parser = argparse.ArgumentParser(
        description="Install Claude Code skills and config from this repo.",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Preview what would be installed without making changes.",
    )
    args = parser.parse_args()

    dry_run = args.dry_run

    print(f"Claude Setup Installer")
    print(f"  Repo:  {REPO_ROOT}")
    print(f"  Dest:  {CLAUDE_DIR}")
    if dry_run:
        print(f"  Mode:  {yellow('dry run')} (no changes will be made)")
    print()

    # ── Install skills ────────────────────────────────────────────────
    print(dim("-- Skills --"))
    skills_ok = 0
    skills_total = 0
    for name in SKILLS:
        if install_skill(name, dry_run):
            skills_ok += 1
        skills_total += 1
    print()

    # ── Install config ─────────────────────────────────────────────────
    print(dim("-- Config --"))
    config_ok = 0
    config_total = 0
    for filename in CONFIG_FILES:
        if install_config(filename, dry_run):
            config_ok += 1
        config_total += 1
    print()

    # ── Summary ────────────────────────────────────────────────────────
    all_ok = skills_ok == skills_total and config_ok == config_total

    if dry_run:
        print(green("Dry run complete. No changes were made."))
        print("Run without --dry-run to apply.")
    elif all_ok:
        print(green("All done! Everything installed successfully."))
        if any((CLAUDE_DIR / f).exists() for f in ["settings.json", "CLAUDE.md"]):
            print()
            print(dim("Tip: Restart Claude Code to pick up new settings."))
    else:
        print(
            yellow(
                f"Installed {skills_ok}/{skills_total} skills and "
                f"{config_ok}/{config_total} config files."
            )
        )
        print(yellow("Some items were skipped (see above)."))

    # Show backup info if any backups were made
    if BACKUP_DIR.exists() and any(BACKUP_DIR.iterdir()):
        print()
        print(dim(f"Backups saved to: {BACKUP_DIR}"))
        print(dim("To restore: cp -r {BACKUP_DIR}/* {CLAUDE_DIR}/"))

    sys.exit(0 if all_ok else 1)


if __name__ == "__main__":
    main()

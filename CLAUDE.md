# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Overview

This is a personal collection of Linux CLI utility tools (Python + Bash). There is no
build system, test suite, or linter — each top-level directory is an independent tool
with its own install script. Tools are installed by copying/rsyncing their `src/`
contents into `~/.local/opt/utils/<tool>/` and adding that directory to `PATH` via
`~/.bashrc`.

## Global setup

- `global_vars.py` (repo root) defines the install locations:
  - `INSTALL_DIR` = `~/.local/opt/utils` (where tools get installed)
  - `DATA_DIR` = `~/Code/data` (backup/data target used by `scripts/src/backup.py`)
  - `CACHE_DIR` = `INSTALL_DIR/.cache`
- `init.py` (repo root) must be run first. It:
  - writes `INSTALL_DIR`/`CACHE_DIR` to `config.yaml` in the repo root
  - copies `global_vars.py` and `config.yaml` into `INSTALL_DIR`
  - creates `INSTALL_DIR` and `CACHE_DIR`
- After `init.py`, each tool directory is installed independently via its own
  `install.py`/`install.sh`.

Each tool's `install.py` adds the repo root to `sys.path` (`sys.path.append(FILE_DIR/..)`)
to import `global_vars`, then rsyncs its `src/` into `INSTALL_DIR/<tool>/src` and appends
an `export PATH=$PATH:<target_dir>` line to `~/.bashrc` (idempotently — checks if the
line already exists first).

## Tools

### `open/` — directory alias navigation (`o` command)

- `open/src/o.sh` is the bash entrypoint, installed as `o` (renamed from `o.sh` during
  install). It dispatches on flags and wraps `open/src/open.py`.
- `open/src/open.py` manages aliases stored in `open/data/dirs.csv` (TSV format
  despite the `.csv` extension: `alias\tpath`).
- Key behaviors:
  - `o <alias>` — open alias's directory in the file explorer (`xdg-open`)
  - `o -t <alias>` (sourced) — `cd` into the alias's directory
  - `o -a [-d<sep>] <alias>,<path>` — add a new alias (append + sort `dirs.csv`)
  - `o -r <alias>` / `o -br <file>` — remove one alias / bulk-remove aliases listed in a file
  - `o -n <old> <new>` — rename an alias
  - `o -l` — list all aliases; `o -h` — show `open/data/help.txt`
  - `.pdf`/`.txt`/`.md` arguments are opened directly via `xdg-open` instead of being
    treated as aliases.
- `o.sh` reads `CACHE_DIR` from `config.yaml` (written by the root `init.py` into
  `INSTALL_DIR`), so the root `init.py` must run before installing `open`.
- Install: `open/install.py` (preferred) or `open/install.sh`. `open/install.sh`
  resets the locally stored `dirs.csv` to the repo's copy — be careful re-running it.
- `open/uninstall.sh` is currently empty.

### `scripts/` — misc standalone scripts

Installed via `scripts/install.py`, which rsyncs `scripts/src/` to
`INSTALL_DIR/scripts/src` (chmod 755) and adds it to `PATH`.

- `backup.py` — backs up VS Code settings/keybindings/snippets and `open`'s
  `dirs.csv` into `DATA_DIR`.
- `maketex.sh` — runs `latexmk -pdf` on a `.tex` file (or the sole `.tex` file in the
  current directory if only one exists), then cleans aux files.
- `texclean.sh` — removes common LaTeX auxiliary files
  (`.aux`, `.bbl`, `.blg`, `.log`, `.out`, `.synctex.gz`, `.snm`, `.toc`, `.nav`).
- `init_cheatsheet.sh` — rsyncs a hardcoded LaTeX cheatsheet template directory into
  the current directory (path is machine-specific, under
  `/home/kramasamy/Documents/Templates/...`).

**Directory alias navigation for Windows PowerShell** — the Windows port of the `open/` tool.

Unlike `open/` (a bash/python mixture), all logic here is in Python
(`src/open.py`). The only PowerShell is `src/o.ps1`, a thin wrapper that
cannot be avoided: a child process cannot change the shell's current
directory, so for `o -t <alias>` Python prints the target path and the
wrapper runs `Set-Location`. A bonus of `.ps1` scripts running in the
calling session: `o -t` works directly — no `source` / dot-sourcing as in
the bash version.

### Requirements
- Python 3 on PATH (`python` or `py`).
- Script execution enabled for local scripts. If PowerShell refuses to run
  `o`, run once:
  `Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser`

### Install
From PowerShell, in this directory:
```powershell
python install.py
```
This copies `src/` and `data/` to `%USERPROFILE%\.local\opt\utils\open_win\`
and adds the `src` directory to your user PATH. Open a new PowerShell
window afterwards.

### Update
Re-run `python install.py`. It refreshes the scripts and `help.txt` but
never overwrites your installed `dirs.csv` alias database.

### Usage
    o <alias1> <alias2> ...   - Open the aliases' directories in Windows Explorer.
    o .                       - Open the current folder in Explorer.
    o ..                      - Open the parent folder in Explorer.
    o <file>.pdf|.txt|.md     - Open the file with its default application.
    o .\<path>\               - Open a relative path in Explorer.
    o -t <alias>              - cd into the alias's directory.
    o -a <alias> [<path>]     - Add an alias. <path> defaults to the current
                                directory; relative paths are resolved.
    o -af <alias> [<path>]    - Force-add: replace an existing alias entry.
    o -r <alias>              - Remove an alias.
    o -br <file>              - Remove all aliases listed in <file> (one per line).
    o -n <old> <new>          - Rename an alias.
    o -s <keyword>            - Search aliases and paths for a keyword.
    o -l                      - List all aliases.
    o -h                      - Show help.

### Differences from the Linux `open/` tool
- `o -t <alias>` needs no sourcing (`. o -t x` → just `o -t x`).
- The primary add syntax is space-separated: `o -a <alias> [<path>]`.
  PowerShell parses a bare `alias,path` as an array, so the comma form of
  the Linux tool only works quoted: `o -a 'docs,C:\Docs'` (the `-d<sep>`
  flag is still supported for a custom separator).
- Files/folders open via `os.startfile` (Explorer / default app) instead
  of `xdg-open`.
- The alias database format is unchanged (`data\dirs.csv`, tab-separated,
  sorted by path), so a `dirs.csv` from the Linux tool can be reused —
  though the stored paths must of course be valid Windows paths.

### Files
| File | Role |
|---|---|
| `src/open.py` | All tool logic (Python) |
| `src/o.ps1` | Thin wrapper; only handles `Set-Location` for `-t` |
| `data/dirs.csv` | Alias database (TSV: `alias<TAB>path`) |
| `data/help.txt` | Help text for `o -h` |
| `install.py` | Installer (also serves as updater) |

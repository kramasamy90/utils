#!/usr/bin/env python3
"""open.py — backend for the `o` directory-alias tool on Windows.

All logic lives here. src/o.ps1 is a thin PowerShell wrapper that exists
only because a child process cannot change the shell's current directory:
for `o -t <alias>` this script prints the path and the wrapper runs
Set-Location on it. Every other command is handled entirely in Python.

Alias database: ../data/dirs.csv (TSV: alias<TAB>path), kept sorted by path.
"""

import os
import sys

FILE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.normpath(os.path.join(FILE_DIR, '..', 'data'))
DIRS_FILE = os.path.join(DATA_DIR, 'dirs.csv')
HELP_FILE = os.path.join(DATA_DIR, 'help.txt')

# Files with these extensions are opened directly with their default app
# instead of being treated as aliases.
OPENABLE_EXTENSIONS = ('.pdf', '.txt', '.md')


def error(message):
    print(message, file=sys.stderr)


def load_aliases():
    """Read dirs.csv into {alias: path}."""
    aliases = {}
    if not os.path.exists(DIRS_FILE):
        return aliases
    with open(DIRS_FILE, encoding='utf-8') as file:
        for line in file:
            line = line.rstrip('\n')
            if not line.strip():
                continue
            parts = line.split('\t')
            if len(parts) >= 2:
                aliases[parts[0]] = parts[1]
    return aliases


def save_aliases(aliases):
    """Write {alias: path} back to dirs.csv, sorted by path."""
    rows = sorted(aliases.items(), key=lambda item: item[1].lower())
    with open(DIRS_FILE, 'w', encoding='utf-8') as file:
        for alias, path in rows:
            file.write(f'{alias}\t{path}\n')


def open_path(path):
    """Open a file or directory with its default application / Explorer."""
    path = os.path.normpath(path)
    if hasattr(os, 'startfile'):
        os.startfile(path)
    else:
        # Fallback so the script also works outside Windows (e.g. testing).
        import subprocess
        subprocess.Popen(['xdg-open', path])


def resolve_path(path):
    """Expand ~ and resolve a possibly relative path against the CWD."""
    if not path or path == '.':
        return os.getcwd()
    return os.path.abspath(os.path.expanduser(path))


def looks_like_path(arg):
    return (arg.startswith('./') or arg.startswith('.\\')
            or arg.endswith('/') or arg.endswith('\\'))


# ---------------------------------------------------------------- commands

def cmd_open(args):
    """o <alias|path|file> ... — open each argument in Explorer/default app."""
    aliases = load_aliases()
    missing = []
    for arg in args:
        if arg in ('.', '..'):
            open_path(arg)
        elif arg.lower().endswith(OPENABLE_EXTENSIONS) and os.path.isfile(arg):
            open_path(arg)
        elif looks_like_path(arg) and os.path.isdir(arg):
            open_path(arg)
        elif arg in aliases:
            path = aliases[arg]
            if os.path.isdir(path):
                open_path(path)
            else:
                error(f"ERROR: directory for alias '{arg}' does not exist:")
                error(f'  {path}')
        else:
            missing.append(arg)
    if missing:
        error('WARNING: The following aliases do not exist:')
        for alias in missing:
            error(f'  {alias}')
        return 1
    return 0


def cmd_terminal(args):
    """o -t <alias> — print the alias's path for o.ps1 to Set-Location."""
    if not args:
        error('Usage: o -t <alias>')
        return 1
    alias = args[0]
    aliases = load_aliases()
    if alias not in aliases:
        error(f"ERROR: alias '{alias}' does not exist.")
        return 1
    path = aliases[alias]
    if not os.path.isdir(path):
        error(f"ERROR: directory for alias '{alias}' does not exist:")
        error(f'  {path}')
        return 1
    print(path)
    return 0


def cmd_add(args, force=False):
    """o -a [-d<sep>] <alias> [<path>] — add an alias.

    Path defaults to the CWD; relative paths are resolved against it.
    With a single argument containing <sep> (default ','), the argument is
    split into alias and path — kept for parity with the Linux tool.
    """
    sep = ','
    operands = []
    for arg in args:
        if arg.startswith('-d') and len(arg) > 2:
            sep = arg[2:]
        else:
            operands.append(arg)

    if not operands:
        error('Usage: o -a <alias> [<path>]')
        return 1

    if len(operands) == 1 and sep in operands[0]:
        alias, _, path = operands[0].partition(sep)
    else:
        alias = operands[0]
        # A path given unquoted with spaces arrives as several arguments.
        path = ' '.join(operands[1:])

    if not alias or '\t' in alias or any(ch.isspace() for ch in alias):
        error(f"ERROR: invalid alias: '{alias}'")
        return 1

    path = resolve_path(path)
    if not os.path.isdir(path):
        error(f'ERROR: not a directory: {path}')
        return 1

    aliases = load_aliases()
    if force:
        aliases.pop(alias, None)
    if alias in aliases:
        error(f"ERROR: alias '{alias}' is already taken:")
        error(f'  {alias}\t{aliases[alias]}')
        return 1

    if path in aliases.values():
        existing = next(a for a, p in aliases.items() if p == path)
        print(f"This path is already associated with alias '{existing}'.")
        answer = input(f"Rename '{existing}' to '{alias}'? [yes/no] ")
        if answer.strip().lower() in ('y', 'yes'):
            aliases.pop(existing)
            print(f"Renamed '{existing}' to '{alias}'")
        else:
            print('Nothing added.')
            return 1

    aliases[alias] = path
    save_aliases(aliases)
    print(f'Added: {alias} -> {path}')
    return 0


def cmd_remove(args):
    """o -r <alias> — remove one alias."""
    if not args:
        error('Usage: o -r <alias>')
        return 1
    alias = args[0]
    aliases = load_aliases()
    if alias not in aliases:
        error(f"ERROR: alias '{alias}' does not exist.")
        return 1
    aliases.pop(alias)
    save_aliases(aliases)
    print(f'Removed: {alias}')
    return 0


def cmd_bulk_remove(args):
    """o -br <file> — remove every alias listed in <file> (one per line)."""
    if not args:
        error('Usage: o -br <file>')
        return 1
    list_file = args[0]
    if not os.path.isfile(list_file):
        error(f'ERROR: file not found: {list_file}')
        return 1

    aliases = load_aliases()
    missing = []
    with open(list_file, encoding='utf-8') as file:
        for line in file:
            alias = line.strip()
            if not alias:
                continue
            if alias in aliases:
                aliases.pop(alias)
                print(f'Removed: {alias}')
            else:
                missing.append(alias)
    save_aliases(aliases)
    if missing:
        error('WARNING: The following aliases do not exist:')
        for alias in missing:
            error(f'  {alias}')
    return 0


def cmd_rename(args):
    """o -n <old> <new> — rename an alias."""
    if len(args) < 2:
        error('Usage: o -n <old_alias> <new_alias>')
        return 1
    old, new = args[0], args[1]
    aliases = load_aliases()
    if old not in aliases:
        error(f"ERROR: alias '{old}' does not exist.")
        return 1
    if new in aliases:
        error(f"ERROR: alias '{new}' is already taken:")
        error(f'  {new}\t{aliases[new]}')
        return 1
    aliases[new] = aliases.pop(old)
    save_aliases(aliases)
    print(f"Renamed '{old}' to '{new}'")
    return 0


def cmd_list():
    """o -l — print the alias database."""
    for alias, path in load_aliases().items():
        print(f'{alias}\t{path}')
    return 0


def cmd_search(args):
    """o -s <keyword> — case-insensitive search over aliases and paths."""
    if not args:
        error('Usage: o -s <keyword>')
        return 1
    keyword = args[0].lower()
    for alias, path in load_aliases().items():
        if keyword in alias.lower() or keyword in path.lower():
            print(f'{alias}\t{path}')
    return 0


def cmd_help():
    with open(HELP_FILE, encoding='utf-8') as file:
        print(file.read(), end='')
    return 0


def main(argv):
    if not argv:
        return cmd_help()

    command = argv[0]
    rest = argv[1:]

    if command == '-h':
        return cmd_help()
    if command == '-l':
        return cmd_list()
    if command == '-s':
        return cmd_search(rest)
    if command == '-t':
        return cmd_terminal(rest)
    if command == '-a':
        return cmd_add(rest)
    if command == '-af':
        return cmd_add(rest, force=True)
    if command == '-r':
        return cmd_remove(rest)
    if command == '-br':
        return cmd_bulk_remove(rest)
    if command == '-n':
        return cmd_rename(rest)
    if command.startswith('-'):
        error(f'Invalid option: {command}')
        error('Use -h for help')
        return 1
    return cmd_open(argv)


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))

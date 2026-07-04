#!/usr/bin/env python3
"""Installer for open_win. Run on Windows from PowerShell:

    python install.py

Reads INSTALL_DIR from the repo root's config.yaml (written by init.py,
which must be run first), copies src/ and data/ to INSTALL_DIR\\open_win
and adds the src directory to the user PATH (registry, HKCU\\Environment).
Safe to re-run to update: an existing dirs.csv alias database is never
overwritten.
"""

import os
import shutil
import sys

FILE_DIR = os.path.realpath(os.path.dirname(__file__))
CONFIG_FILE = os.path.join(FILE_DIR, '..', 'config.yaml')


def read_install_dir():
    if not os.path.isfile(CONFIG_FILE):
        sys.exit(f'config.yaml not found at {os.path.normpath(CONFIG_FILE)}. '
                 'Run init.py at the repo root first.')
    with open(CONFIG_FILE, encoding='utf-8') as file:
        for line in file:
            # Split on the first colon only: Windows paths contain ':'.
            key, _, value = line.partition(':')
            if key.strip() == 'INSTALL_DIR' and value.strip():
                return value.strip()
    sys.exit('INSTALL_DIR not found in config.yaml. '
             'Run init.py at the repo root first.')


INSTALL_DIR = read_install_dir()
SRC_TARGET = os.path.join(INSTALL_DIR, 'open_win', 'src')
DATA_TARGET = os.path.join(INSTALL_DIR, 'open_win', 'data')


def add_to_user_path(directory):
    """Append directory to the user's PATH in the registry, idempotently."""
    import ctypes
    import winreg

    with winreg.OpenKey(winreg.HKEY_CURRENT_USER, 'Environment', 0,
                        winreg.KEY_READ | winreg.KEY_SET_VALUE) as key:
        try:
            current, value_type = winreg.QueryValueEx(key, 'Path')
        except FileNotFoundError:
            current, value_type = '', winreg.REG_EXPAND_SZ
        entries = [entry for entry in current.split(';') if entry]
        if directory.lower() in (entry.lower() for entry in entries):
            print(f'Already in PATH: {directory}')
            return
        entries.append(directory)
        winreg.SetValueEx(key, 'Path', 0, value_type, ';'.join(entries))

    # Notify running processes that the environment changed so new
    # terminals pick up the PATH without a logout.
    HWND_BROADCAST, WM_SETTINGCHANGE = 0xFFFF, 0x001A
    ctypes.windll.user32.SendMessageTimeoutW(
        HWND_BROADCAST, WM_SETTINGCHANGE, 0, 'Environment', 0, 5000, None)
    print(f'Added to user PATH: {directory}')


def main():
    if os.name != 'nt':
        sys.exit('This installer is for Windows. '
                 'On Linux use the open/ tool instead.')

    os.makedirs(SRC_TARGET, exist_ok=True)
    os.makedirs(DATA_TARGET, exist_ok=True)

    shutil.copytree(os.path.join(FILE_DIR, 'src'), SRC_TARGET,
                    dirs_exist_ok=True)

    shutil.copy2(os.path.join(FILE_DIR, 'data', 'help.txt'), DATA_TARGET)
    dirs_csv = os.path.join(DATA_TARGET, 'dirs.csv')
    if not os.path.exists(dirs_csv):
        shutil.copy2(os.path.join(FILE_DIR, 'data', 'dirs.csv'), dirs_csv)

    add_to_user_path(SRC_TARGET)
    print('Done. Open a new PowerShell window and run:  o -h')


if __name__ == '__main__':
    main()

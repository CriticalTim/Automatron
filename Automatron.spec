# -*- mode: python ; coding: utf-8 -*-

import sys
import os
from PyInstaller.utils.hooks import collect_data_files, collect_submodules

# Collect all CustomTkinter files
customtkinter_datas = collect_data_files('customtkinter')

# Collect webdriver manager data
webdriver_datas = collect_data_files('webdriver_manager')

# Add additional data files
datas = []
datas += customtkinter_datas
datas += webdriver_datas

# Collect hidden imports
hiddenimports = []
hiddenimports += collect_submodules('customtkinter')
hiddenimports += collect_submodules('webdriver_manager')
hiddenimports += collect_submodules('selenium')
hiddenimports += [
    'tkinter',
    'tkinter.ttk',
    'tkinter.filedialog',
    'tkinter.messagebox',
    'sqlite3',
    'smtplib',
    'email.mime.text',
    'email.mime.multipart',
    'ssl',
    'PyPDF2',
    'requests',
    'beautifulsoup4',
    'schedule',
    'threading',
    'json',
    'os',
    're',
    'time',
    'random',
    'difflib',
    'datetime'
]

block_cipher = None

a = Analysis(
    ['run.py'],
    pathex=[],
    binaries=[],
    datas=datas,
    hiddenimports=hiddenimports,
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[
        'matplotlib',
        'numpy',
        'pandas',
        'scipy',
        'PIL.ImageQt',
        'PyQt5',
        'PyQt6',
        'PySide2',
        'PySide6',
        'wx'
    ],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='Automatron',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,  # Set to False for GUI app
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon='app_icon.ico',
    version=None,
)
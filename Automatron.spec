# -*- mode: python ; coding: utf-8 -*-

import sys
import os
from PyInstaller.utils.hooks import collect_data_files, collect_submodules

# Safe collection of data files with error handling
def safe_collect_data_files(module_name):
    try:
        return collect_data_files(module_name)
    except Exception as e:
        print(f"Warning: Could not collect data files for {module_name}: {e}")
        return []

def safe_collect_submodules(module_name):
    try:
        return collect_submodules(module_name)
    except Exception as e:
        print(f"Warning: Could not collect submodules for {module_name}: {e}")
        return []

# Collect all CustomTkinter files
customtkinter_datas = safe_collect_data_files('customtkinter')

# Collect webdriver manager data
webdriver_datas = safe_collect_data_files('webdriver_manager')

# Collect Pillow/PIL data
pillow_datas = safe_collect_data_files('PIL')

# Add additional data files
datas = []
datas += customtkinter_datas
datas += webdriver_datas
datas += pillow_datas

# Collect hidden imports with error handling
hiddenimports = []
hiddenimports += safe_collect_submodules('customtkinter')
hiddenimports += safe_collect_submodules('webdriver_manager')
hiddenimports += safe_collect_submodules('selenium')
hiddenimports += safe_collect_submodules('PIL')
hiddenimports += [
    'tkinter',
    'tkinter.ttk',
    'tkinter.filedialog',
    'tkinter.messagebox',
    'sqlite3',
    'smtplib',
    'email.mime.text',
    'email.mime.multipart',
    'email.mime.base',
    'email.encoders',
    'ssl',
    'PyPDF2',
    'requests',
    'bs4',
    'beautifulsoup4',
    'schedule',
    'threading',
    'json',
    'os',
    're',
    'time',
    'random',
    'difflib',
    'datetime',
    'logging',
    'urllib.parse',
    'urllib.request',
    'http.client',
    'base64',
    'hashlib',
    'uuid',
    'pathlib',
    'platform',
    'subprocess',
    'dotenv',
    'python_dotenv'
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
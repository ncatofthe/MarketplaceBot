# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

a = Analysis(
    ['main.py'],
    pathex=[],
    binaries=[],
    datas=[
        ('config.py', '.'),
    ],
    hiddenimports=[
        'api',
        'api.ozon_api',
        'api.wb_api',
        'bots',
        'bots.base_bot',
        'bots.ozon_bot',
        'bots.wildberries_bot',
        'gui',
        'gui.main_window',
        'utils',
        'utils.logger',
        'utils.answers',
        'config',
        'tkinter',
        'tkinter.ttk',
        'tkinter.scrolledtext',
        'json',
        'logging',
        'threading',
        'requests',
        'urllib3',
        'cryptography',
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[
        'tkinter.ttk',
    ],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
    optimize=0,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='MarketplaceBot',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,  # Без консоли для GUI приложения
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=None,
    version='version_info.txt',  # Файл с информацией о версии
)


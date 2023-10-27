# -*- mode: python ; coding: utf-8 -*-


a = Analysis(
    ['main.py'],
    pathex=['app', 'resources', '.github'],
    binaries=[('C:\\Users\\adrie\\AppData\\Local\\Programs\\Python\\Python312\\python312.dll', '.')],
    binaries=[],
    datas=[('version.json', '.'), ('generate_appcast.py', '.'), ('config.ini', '.'), ('theme.qss', '.'), ('winsparkle_wrapper.py', '.'), ('LICENSE.md', '.'), ('README.md', '.'), ('requirements.txt', '.'), ('WinSparkle.dll', '.')],
    hiddenimports=[],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='main',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)
coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='main',
)

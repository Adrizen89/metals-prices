# -*- mode: python ; coding: utf-8 -*-

def get_requirements():
    with open('requirements.txt', 'r') as file:
        lines = file.readlines()
    # Extraire uniquement les noms des bibliothèques, en ignorant les versions ou autres spécifications
    return [line.split('==')[0] for line in lines]

block_cipher = None



a = Analysis(
    ['main.py'],
    pathex=['app', 'resources'],
    binaries=[],
    datas=[('config.ini', '.'), ('theme.qss', '.')],
    hiddenimports=get_requirements(),
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
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
    name='main',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=True,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)

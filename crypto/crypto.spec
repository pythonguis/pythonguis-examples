# -*- mode: python ; coding: utf-8 -*-

block_cipher = None


a = Analysis(['crypto.py'],
             binaries=[],
             datas=[],
             hiddenimports=[],
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher,
             noarchive=False)
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)
exe = EXE(pyz,
          a.scripts,
          [],
          exclude_binaries=True,
          name='Goodforbitcoin',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          console=False,
          icon='resources/icon.ico'
          )
coll = COLLECT(exe,
               a.binaries,
               a.zipfiles,
               a.datas,
               strip=False,
               upx=True,
               upx_exclude=[],
               name='Goodforbitcoin'
               )
app = BUNDLE(coll,
             name='Goodforbitcoin.app',
             icon='resources/icon.icns',
             bundle_identifier='com.learnpyqt.Goodforbitcoin',
             info_plist={
                 'NSHighResolutionCapable': 'True'
             },
            )

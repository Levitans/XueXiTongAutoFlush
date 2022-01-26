# -*- mode: python ; coding: utf-8 -*-


block_cipher = None


a = Analysis(['main.py',
r'F:\python项目\学习通刷课2\package\disPlay.py',
r'F:\python项目\学习通刷课2\package\manageDate.py',
r'F:\python项目\学习通刷课2\package\user.py',
r'F:\python项目\学习通刷课2\package\ControlWeb\course.py',
r'F:\python项目\学习通刷课2\package\ControlWeb\xueXiTong.py',
r'F:\python项目\学习通刷课2\package\ControlWeb\task\getAnswer.py',
r'F:\python项目\学习通刷课2\package\ControlWeb\task\homework.py',
r'F:\python项目\学习通刷课2\package\ControlWeb\task\PPT.py',
r'F:\python项目\学习通刷课2\package\ControlWeb\task\video.py'],
             pathex=['F:\\python项目\\学习通刷课2'],
             binaries=[],
             datas=[],
             hiddenimports=['selenium'],
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
          console=True )

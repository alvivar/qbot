""" Create an .exe with cx_Freeze, just call 'python setup.py build'. """

from cx_Freeze import Executable, setup

OPTIONS = {'build_exe': {'includes': ['sqlalchemy.sql.default_comparator']}}

EXECUTABLES = [Executable('qbot.py', targetName='qbot.exe')]

setup(
    name='QBot',
    version='0.1',
    description=
    "Bot that tweets on schedules, using json files as configuration",
    executables=EXECUTABLES,
    options=OPTIONS)

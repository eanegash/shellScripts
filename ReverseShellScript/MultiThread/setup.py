import sys
from cx_Freeze import setup, Executable

include_files = ['autorun.inf']
base = None

if sys.platform == "win32":
    base = "Win32GUI"

setup(name="diagnostics",version='0.1',
    description="Diagnostic tool", 
    options=('build_exe': {'include_files': include_files}),
    executables=[Executable("client_multithread.py", base=base)])
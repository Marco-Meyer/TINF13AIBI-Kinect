import sys
from cx_Freeze import setup, Executable

# Dependencies are automatically detected, but it might need fine tuning.
build_exe_options = {"excludes": ["tkinter"]}

base = None
if sys.platform == "win32":
    base = "Win32GUI"
setup(  name = "2048",
        version = "1.0",
        description = "2048",
        options = {"build_exe": build_exe_options},
        executables = [Executable("2048.py", base=base)])
import os
import zipfile

with zipfile.ZipFile(os.path.join("build","exe.win32-3.4", "library.zip"), "a") as f:
    f.write("freesansbold.ttf", "pygame/freesansbold.ttf")

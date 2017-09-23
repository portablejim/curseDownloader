#!python3

import sys
from cx_Freeze import setup, Executable
import os.path

PYTHON_INSTALL_DIR = os.path.dirname(os.path.dirname(os.__file__))
os.environ['TCL_LIBRARY'] = os.path.join(PYTHON_INSTALL_DIR, 'tcl', 'tcl8.6')
os.environ['TK_LIBRARY'] = os.path.join(PYTHON_INSTALL_DIR, 'tcl', 'tk8.6')

file_includes = []

base = None
targetName = "cursePackDownloader"
if sys.platform == "win32":
    base = "Win32GUI"
    targetName = "cursePackDownloader.exe"
    file_includes = [
        os.path.join(PYTHON_INSTALL_DIR, 'DLLs', 'tk86t.dll'),
        os.path.join(PYTHON_INSTALL_DIR, 'DLLs', 'tcl86t.dll')
    ]


setup_options = {
    "build_exe": {
        'include_files': file_includes,
        "packages": ["appdirs","idna","chardet","urllib3","certifi","requests"],
    }
}

setup(
    name="cursePackDownloader",
    version="0.3",
    description="Download extra mods from Curse-hosted Minecraft modpacks",
    options = setup_options,
    executables=[Executable("downloader.py", targetName=targetName, base=base)]
)

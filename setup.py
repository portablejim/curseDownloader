#!python3

import sys
from cx_Freeze import setup, Executable

base = None
if sys.platform == "win32":
    base = "Win32GUI"

setup(
    name = "cursePackDownloader",
    version = "0.1",
    description = "Download extra mods from Curse-hosted Minecraft modpacks",
    executables = [Executable("downloader.py")])

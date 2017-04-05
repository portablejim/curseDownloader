# Curseforge Minecraft Modpack Downloader


A simple script to download mods from a CurseForge Minecraft modpack.

## Requirements

- Python 3.4+
- appdirs
- requests
- python-tk

### Setup

#### Ubuntu

- `sudo apt install python3 python3-tk python3-pip`
- `pip3 install -r requirements.txt`

## How to use

  1. Find the modpack you want from the [CurseForge modpack list](http://www.curse.com/modpacks/minecraft)
  2. Unzip the download. There should be a manifest.json file.
  3. Run! `python3.4 /path/to/downloader.py --manifest /path/to/manifest.json`


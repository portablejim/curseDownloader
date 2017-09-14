# Curseforge Minecraft Modpack Downloader


A simple script to download mods from a CurseForge Minecraft modpack.

## Requirements

- Python 3.4+
- appdirs
- requests
- python-tk

### Installation

#### Fedora

- `sudo dnf copr enable srakitnican/minecraft`
- `sudo dnf install cursedownloader`

### Setup
#### Fedora

- `sudo dnf install python3-appdirs python3-requests python3-tkinter`

#### Ubuntu

- `sudo apt install python3 python3-tk python3-pip`
- `pip3 install -r requirements.txt`

## How to use

  1. Find the modpack you want from the [CurseForge modpack list](http://www.curse.com/modpacks/minecraft)
  2. Unzip the download. There should be a manifest.json file.
  3. Run! `python3.4 /path/to/downloader.py --manifest /path/to/manifest.json`


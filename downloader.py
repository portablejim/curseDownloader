#!python3

import argparse
import json
from pathlib import Path
import requests
import shutil
import urllib

parser = argparse.ArgumentParser(description="Download Curse modpack mods")
parser.add_argument("manifest", help="manifest.json file from unzipped pack")
#parser.add_argument("--gui", action="store_true", help="Use gui to to select manifest")
args = parser.parse_args()

manifestPath = Path(args.manifest)
targetDirPath = manifestPath.parent

manifestText = ""
manifestText = manifestPath.open().read()

manifestJson = json.loads(manifestText)

overridePath = Path(targetDirPath, manifestJson['overrides'])
minecraftPath = Path(targetDirPath, "minecraft")
if overridePath.exists():
    shutil.move(str(overridePath), str(minecraftPath))


sess = requests.session()

i = 1
iLen = len(manifestJson['files'])

print("%d files to download" % (iLen))

for dependency in manifestJson['files']:
    projectResponse = sess.get("http://minecraft.curseforge.com/mc-mods/%s" % (dependency['projectID']), stream=True)
    fileResponse = sess.get("%s/files/%s/download" % (projectResponse.url, dependency['fileID']), stream=True)
    while fileResponse.is_redirect:
        source = fileResponse
        fileResponse = sess.get(source, stream=True)
    filePath = Path(fileResponse.url)
    fileName = filePath.name.replace("%20", " ")
    print("[%d/%d] %s" % (i, iLen, fileName))
    with open(str(minecraftPath / "mods" / fileName), "wb") as mod:
        mod.write(fileResponse.content)

    i += 1


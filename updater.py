import argparse
import json
from pathlib import Path
import re
import requests

__author__ = 'james'

parser = argparse.ArgumentParser(description="Update Curse modpack manifest")
parser.add_argument("--manifest", help="manifest.json file from unzipped pack")
#parser.add_argument("--noIgui", dest="gui", action="store_false", help="Do not use gui to to select manifest")
args, unknown = parser.parse_known_args()

def parseManifest(manifest):
    manifestPath = Path(manifest)
    targetDirPath = manifestPath.parent

    manifestText = manifestPath.open().read()
    manifestText = manifestText.replace('\r', '').replace('\n', '')

    manifestJson = json.loads(manifestText)
    return manifestJson


def getNameForNumericalId(session, numericalid):
    project_response = session.get("http://minecraft.curseforge.com/mc-mods/%s" % (numericalid), stream=True)
    name_id_parts = re.split("\d+-([^/]*)", project_response.url, 1)
    return name_id_parts[-2]


def getFilesForVersion(session, mcversion, modid, modname):
    files_json_response = session.get("http://widget.mcf.li/mc-mods/minecraft/%s.json" % modname)
    if files_json_response.status_code != 200:
        files_json_response = session.get("http://widget.mcf.li/mc-mods/minecraft/%d-%s.json" % (modid, modname))
    files_json = files_json_response.json()
    versions = files_json["versions"]
    if mcversion in versions:
        return versions[mcversion]
    else:
        return []
    pass


sess = requests.session()
#v = getNameForNumericalId(sess, 67133)
fs = getFilesForVersion(sess, "1.7.10", 67133, "veinminer")
for f in fs:
    print("%s | %s: %s" % (f["name"], f["type"], f["id"]))

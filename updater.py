import argparse
import json
from pathlib import Path
import re
from tkinter import Tk
import tkinter

import requests


__author__ = 'james'

parser = argparse.ArgumentParser(description="Update Curse modpack manifest")
parser.add_argument("--manifest", help="manifest.json file from unzipped pack")
parser.add_argument("--nogui", dest="gui", action="store_false", help="Do not use gui to to select manifest")
args, unknown = parser.parse_known_args()


class UpdateChooseGui():
    optionChosen = -1
    optionValues = {}

    def __init__(self):
        self.choose_gui = None
        self.choose_listbox = None

    def get_option(self, choices):
        self.choose_gui = Tk()
        self.choose_gui.title("Choose file to use")
        self.choose_gui.minsize(500, 200)
        self.center(self.choose_gui)
        choose_gui_frame = tkinter.Frame(self.choose_gui)
        choose_gui_frame.pack(fill=tkinter.BOTH, expand=True)
        self.choose_listbox = tkinter.Listbox(choose_gui_frame)
        i = 0
        for choice in choices:
            self.choose_listbox.insert(i, choice["text"])
            self.optionValues[i] = choice["value"]
            i += 1
        self.choose_listbox.pack(side=tkinter.TOP, fill=tkinter.BOTH, expand=True)

        choose_button = tkinter.Button(choose_gui_frame, text="Use version", command=self.set_option)
        choose_button.pack(side=tkinter.BOTTOM, fill=tkinter.X)

        self.choose_gui.mainloop()

        if self.optionChosen > -1:
            return self.optionValues[self.optionChosen]
        else:
            return -1

    def set_option(self):
        self.optionChosen = self.choose_listbox.curselection()[0]
        self.choose_gui.quit()

    def center(self, toplevel):
        toplevel.update_idletasks()
        w = toplevel.winfo_screenwidth()
        h = toplevel.winfo_screenheight()
        size = tuple(int(_) for _ in toplevel.geometry().split('+')[0].split('x'))
        x = w/2 - size[0]/2
        y = h/2 - size[1]/2
        # noinspection PyStringFormat
        toplevel.geometry("%dx%d+%d+%d" % (size + (x, y)))


class UpdateChooseCli():
    optionChosen = -1
    optionValues = {}
    def get_option(self, choices):

        i = 0
        for choice in choices:
            print("%d) %s" % (i+1, choice["text"]))
            self.optionValues[i] = choice["value"]
            i += 1

        while self.optionChosen is -1:
            try:
                test_val = int(input("Choose file to use: "))
                if test_val in self.optionValues:
                    self.optionChosen = test_val
            except ValueError:
                pass

        if self.optionChosen > -1:
            return self.optionValues[self.optionChosen]
        else:
            return -1


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


def get_newer_files(file_list, target_file):
    newer_files = []
    for test_file in file_list:
        if test_file["id"] is not target_file:
            newer_files += [test_file]
        else:
            break

    return newer_files


def get_filtered_files(file_list):
    remaining_alpha = 3
    remaining_beta = 2
    remaining_release = 2

    filtered_list = []
    for test_file in file_list:
        if test_file["type"] == "release" and remaining_release > 0:
            remaining_release -= 1
        elif test_file["type"] == "beta" and remaining_beta > 0:
            remaining_beta -= 1
        elif test_file["type"] == "alpha" and remaining_alpha > 0:
            remaining_alpha -= 1
        else:
            continue

        filtered_list += [test_file]

    return filtered_list


def get_selectable_options(options):
    release_type_lookup = {"release": "Release", "beta": "Beta", "alpha": "Alpha"}

    selectable_options = []
    for option in options:
        new_val = dict()
        new_val["text"] = "[%s] %s (id %s)" % (release_type_lookup[option["type"]], option["name"], option["id"])
        new_val["value"] = option["id"]
        selectable_options.append(new_val)

    return selectable_options


def is_up_to_date(file_id, file_type, file_list, ignore_less_stable=True):
    types = ['alpha', 'beta', 'release']
    # Get more stable/better files release > beta > alpha
    target_types = None
    if ignore_less_stable and file_type in types:
        target_types = types[types.index(file_type):]
    else:
        target_types = types
    for file_item in file_list:
        if file_item['type'] in target_types:
            return file_item['id'] == file_id

    return False


sess = requests.session()
#v = getNameForNumericalId(sess, 67133)
fs = getFilesForVersion(sess, "1.7.10", 67133, "veinminer")
ffs = get_filtered_files(fs)
gui = None
print(args)
if args.gui:
    gui = UpdateChooseGui()
else:
    gui = UpdateChooseCli()
x = gui.get_option(get_selectable_options(ffs))
print(x)

#!python3

import argparse
import json
from pathlib import Path
import os
import requests
import shutil
from threading import Thread
from tkinter import *
from tkinter import ttk, filedialog
import urllib

parser = argparse.ArgumentParser(description="Download Curse modpack mods")
parser.add_argument("--manifest", help="manifest.json file from unzipped pack")
parser.add_argument("--nogui", dest="gui", action="store_false", help="Do not use gui to to select manifest")
args, unknown = parser.parse_known_args()

class downloadUI(ttk.Frame):
    def __init__(self):
        self.root = Tk()
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        self.parent = ttk.Frame(self.root)
        self.parent.grid(column=0, row=0, sticky=(N, S, E, W))
        self.parent.columnconfigure(0, weight=1)
        self.parent.rowconfigure(0, weight=1)
        ttk.Frame.__init__(self, self.parent, padding=(6,6,14,14))
        self.grid(column=0, row=0, sticky=(N, S, E, W))
        self.columnconfigure(0, weight=1)
        self.rowconfigure(2, weight=1)

        self.root.title("Curse Pack Downloader")

        self.manifestPath = StringVar()

        chooserContainer = ttk.Frame(self)
        self.chooserText = ttk.Label(chooserContainer, text="Locate 'manifest.json': ")
        chooserEntry = ttk.Entry(chooserContainer, textvariable=self.manifestPath)
        self.chooserButton = ttk.Button(chooserContainer, text="Browse", command=self.chooseFile)
        self.chooserText.grid(column=0, row=0, sticky=W)
        chooserEntry.grid(column=1, row=0, sticky=(E,W), padx=5)
        self.chooserButton.grid(column=2, row=0, sticky=E)
        chooserContainer.grid(column=0, row=0, sticky=(E,W))
        chooserContainer.columnconfigure(1, weight=1)
        downloadButton = ttk.Button(self, text="Download mods", command=self.goDownload)
        downloadButton.grid(column=0, row=1, sticky=(E,W))

        self.logText = Text(self, state="disabled", wrap="none")
        self.logText.grid(column=0, row=2, sticky=(N,E,S,W))

    def chooseFile(self):
        filePath = filedialog.askopenfilename(
                filetypes=(("Json files", "*.json"),), 
                initialdir=os.path.expanduser("~"), 
                parent=self)
        self.manifestPath.set(filePath)

    def goDownload(self):
        t = Thread(target=self.goDownloadBackground)
        t.start()

    def goDownloadBackground(self):
        self.chooserButton.configure(state="disabled")
        doDownload(self.manifestPath.get())
        self.chooserButton.configure(state="enabled")

    def setOutput(self, message):
        self.logText["state"] = "normal"
        self.logText.insert("end", message + "\n")
        self.logText["state"] = "disabled"

    def setManifest(self, fileName):
        self.manifestPath.set(fileName)

class headlessUI():
    def setOutput(self, message):
        pass

programGui = None

def doDownload(manifest):
    manifestPath = Path(manifest)
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
    programGui.setOutput("%d files to download" % (iLen))

    for dependency in manifestJson['files']:
        projectResponse = sess.get("http://minecraft.curseforge.com/mc-mods/%s" % (dependency['projectID']), stream=True)
        fileResponse = sess.get("%s/files/%s/download" % (projectResponse.url, dependency['fileID']), stream=True)
        while fileResponse.is_redirect:
            source = fileResponse
            fileResponse = sess.get(source, stream=True)
        filePath = Path(fileResponse.url)
        fileName = filePath.name.replace("%20", " ")
        print("[%d/%d] %s" % (i, iLen, fileName))
        programGui.setOutput("[%d/%d] %s" % (i, iLen, fileName))
        with open(str(minecraftPath / "mods" / fileName), "wb") as mod:
            mod.write(fileResponse.content)

        i += 1

if args.gui:
    programGui = downloadUI()
    if args.manifest is not None:
        programGui.setManifest(args.manifest)
    programGui.root.mainloop()
else:
    programGui = headlessUI()
    doDownload(args.manifest)



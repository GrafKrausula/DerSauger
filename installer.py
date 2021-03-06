import traceback
import subprocess
from subprocess import Popen, PIPE
from subprocess import Popen, CREATE_NEW_CONSOLE
from os import remove
from sys import argv
import pathlib
from pathlib import Path
import zipfile
from zipfile import ZipFile
from os import walk
import os, shutil, glob
import sys
import threading
import _thread
import urllib.request
import shutil
import queue
import time

def get_scriptpath():

    scriptpath = str(pathlib.Path(__file__).parent.absolute())
    return scriptpath
def open_readme(installpath):

    os.chdir('/')
    os.startfile(f'"{installpath}\Der Sauger\README.txt"')
    os.chdir('/')

class Downloader:
    def __init__(self):
        self.isdownloaded = False
        self.isunzipped = False
        self.installpath = None
        self.unzippath = None
        self.extensionpath = None

    def download_and_unzip(self,installpath):

        self.installpath = installpath
        zipfilepath = installpath + "/UPDATE_DerSauger.zip"
        print('{"Info": zipfilepath: %s}' % zipfilepath)

        self.download("https://github.com/GrafKrausula/DerSauger/archive/main.zip", zipfilepath)

        unzippedfile = self.unzip(zipfilepath,installpath)
        print('{"Info": download: %s}' % unzippedfile)

        self.unzippath = installpath + "\DerSauger-main"
        ##nach dem unzippen die zip datei löschen
        os.remove(zipfilepath)
        ##oder auch: extensionpath = self.unzippath + "\Der Sauger"
        self.extensionpath = installpath + "\DerSauger-main\Der Sauger"
        #Verschiebt den subordner "Der Sauger" aus "DerSauger-main" in das parentdirectory sprich installationsverzeichnis
        shutil.move(self.extensionpath, installpath)
        #Update den extensionpath auf die neue location nach der veschriebung
        self.extensionpath = installpath + "\Der Sauger"
        #entfernt die entpackte, nun leere parent datei der extension
        shutil.rmtree(self.unzippath)

        return True

    def download(self,url,file_name):

        print('{"Info": Downloading. Please wait and do not close this window...}')

        try:
            with urllib.request.urlopen(url) as response, open(file_name, 'wb') as out_file:
                shutil.copyfileobj(response, out_file)
            self.isdownloaded = True
            return True

        except Exception as err:
            traceback.print_exc()
            #print(err)
            return False

    def unzip(self,download_zip,installpath):

        print('{"Info": Unzipping download...}')

        if zipfile.is_zipfile(download_zip):

            with ZipFile(download_zip, 'r') as zipObj:
                # Extract all the contents of zip file in different directory
                zipObj.extractall(installpath)
                print('{"Info": File is unzipped in temp folder: %s}' % zipObj)

            self.isunzipped = True
            return True

        else:
            return False

    def get_extensionpath(self):

        return self.extensionpath


class DeployedPathvariables:
    def __init__(self, extensionpath):
        self.ffmpeg = False
        self.youtube = False
        self.extensionpath = extensionpath

    def check_pathvariables(self):

        print('{"Info": Checking for missing pathvariables...}')

        if self.are_pathvariables_complete() == False:
            self.add_missing_pathvariable()
            self.check_pathvariables()
        else:
            return True

    def are_pathvariables_complete(self):

        #installcmd = f'cmd /c "cd /d {get_installpath()}'
        cmd = 'cmd /c for /f "usebackq tokens=2,*" %A in (`reg query HKCU\Environment /v PATH`) do set my_user_path=%B'
        proc1 = subprocess.Popen(cmd,stderr=subprocess.STDOUT,stdout=subprocess.PIPE)

        while True:
            cmdState = proc1.poll()
            #print(cmdState)
            if cmdState != None:
                print("### Search for pathvariables completed! ###")
                break;
            line = proc1.stdout.readline()

            #print(type(line))
            if "ffmpeg" in str(line):
                print("ffmpeg pathvariable found")
                self.ffmpeg = True

            if "youtube-dl" in str(line):
                print("youtube-dl pathvariable found")
                self.youtube = True


            print(f"{line}")


        if (self.youtube and self.ffmpeg) == True:
        #if self.ffmpeg == True:
            print("### Pathvariables are complete! ###")
            return True
        else:
            print("### Pathvariables are incomplete! ###")
            return False

    def add_missing_pathvariable(self):

        print('{"Info": Adding missing pathvariables...}')

        if self.ffmpeg == False:
            self.add_ffmpeg_path()
        if self.youtube == False:
            self.add_youtube_path()

        return True

    def add_ffmpeg_path(self):
        proc1 = subprocess.Popen(f'{self.extensionpath}\AddFfmpegVariable.bat',stderr=subprocess.STDOUT)
        while True:
            cmdState = proc1.poll()
            #print(cmdState)
            if cmdState != None:
                print("ffmpeg PATHVARIABLE added")
                return True;

        return False

    def add_youtube_path(self):
        print(f'{self.extensionpath}')
        proc1 = subprocess.Popen(f'{self.extensionpath}\AddYoutubeVariable.bat',stderr=subprocess.STDOUT)
        while True:
            cmdState = proc1.poll()
            #print(cmdState)
            if cmdState != None:
                print("youtube PATHVARIABLE added")
                return True;

        return False


    def add_registry(self):

        proc1 = subprocess.Popen(f'{self.extensionpath}/nativeMessaging\host\host\install_host.bat',stderr=subprocess.STDOUT)
        while True:
            cmdState = proc1.poll()
            #print(cmdState)
            if cmdState != None:
                print("registry key added")
                return True;

        return False

    def restart_explorer(self):

        proc1 = subprocess.Popen(f'{self.extensionpath}\Reloadpath.bat',stderr=subprocess.STDOUT)
        while True:
            cmdState = proc1.poll()
            #print(cmdState)
            if cmdState != None:
                print("registry key added")
                return True;

        return False


def Main():

    installpath = get_scriptpath()

    downloader = Downloader()
    downloader.download_and_unzip(installpath)

    dpv = DeployedPathvariables(downloader.get_extensionpath())
    dpv.check_pathvariables()
    dpv.add_registry()
    #dpv.restart_explorer()

    x = input("Finished. Press ENTER to exit...")

    open_readme(installpath)

    remove(argv[0]) #removes the .py file


if __name__ == '__main__':


    try:

        Main()

    except Exception as err:

        traceback.print_exc()
        #print(err)
        x = input("An error occured! Press ENTER to exit...")

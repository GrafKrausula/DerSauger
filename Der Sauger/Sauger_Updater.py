import traceback
import subprocess
from subprocess import Popen, PIPE
from subprocess import Popen, CREATE_NEW_CONSOLE
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

def getScriptPath():

    scriptpath = str(pathlib.Path(__file__).parent.absolute())
    return scriptpath

def makedir(convertpath,new_fldr_name):

    new_fldr_name = new_fldr_name.upper()

    new_fldr = f'{convertpath}\{new_fldr_name}'
    #print(new_fldr)

    try:
      os.makedirs(new_fldr) ## it creates the destination folder in capslock
    except:
      print('{"Info": current_thread: %s}' % new_fldr_name)

    return new_fldr

class Updater:

    def __init__(self):
        self.isupdated = False

    def startUpdate(self):

        extensionparentdir_path = getScriptPath()
        tempdownload_folder = makedir(extensionparentdir_path,"temp-sauger")
        zipfile_path = tempdownload_folder + "/UPDATE_DerSauger.zip"
        print('{"Info": extensionparentdir_path: %s}' % extensionparentdir_path)
        print('{"Info": tempdownload_folder: %s}' % tempdownload_folder)
        print('{"Info": downloadfile_path: %s}' % zipfile_path)

        self.downloadUpdate("https://github.com/GrafKrausula/DerSauger/archive/main.zip", zipfile_path)
        print('{"Info": zipfile_path: %s}' % zipfile_path)
        download = self.unzipUpdate(zipfile_path,tempdownload_folder)
        print('{"Info": download: %s}' % download)

        self.installUpdate(tempdownload_folder,extensionparentdir_path) #(Von Argument 1, zu Argument 2)

        return True

    def downloadUpdate(self,url,file_name):

        file = None
        with urllib.request.urlopen(url) as response, open(file_name, 'wb') as out_file:
            shutil.copyfileobj(response, out_file)
            file = out_file
        return file


    def unzipUpdate(self,download_zip,folder):

        if zipfile.is_zipfile(download_zip):

            with ZipFile(download_zip, 'r') as zipObj:
                # Extract all the contents of zip file in different directory
                zipObj.extractall(folder)
                print('{"Info": File is unzipped in temp folder: %s}' % zipObj)

            return True

        else:
            return False

    def installUpdate(self,tempdownload_folder,destination_path):

        current_version_path = f'{destination_path}\Der Sauger'
        update_path = self.searchUpdate(tempdownload_folder)
        print('{"Info": installUpdate(): update_path: %s}' % update_path)

        print('{"Info": installUpdate(): current_version_path: %s}' % current_version_path)
        print('{"Info": installUpdate(): destination_path: %s}' % destination_path)

        shutil.rmtree(current_version_path)
        shutil.move(update_path, destination_path)
        shutil.rmtree(tempdownload_folder)

        return True

    def searchUpdate(self,update_folder):

        allfiles = os.listdir(update_folder)
        update_folder_path = None

        print('{"Info": searchUpdate(): allfiles: %s}' % allfiles)
        for file in allfiles:
            if ("DerSauger" in file) and not ("UPDATE_DerSauger.zip" in file):
                print('{"Info": UPDATE FOLDER FOUND: %s}' % file)
                update_folder_path = f'{update_folder}\{file}'
                update_path = f'{update_folder_path}\Der Sauger'

                return update_path

        return None



def Main():

    updater = Updater()
    updater.startUpdate()

    #readme öffnen

    x = input("Finished. Press Any key to exit...")


if __name__ == '__main__':


    try:

        Main()

    except Exception as err:

        traceback.print_exc()
        #print(err)
        x = input("An error occured! Press Any key to exit...")

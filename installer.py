# Imports various libraries for handling file paths, subprocesses, threading, network requests, and more
import traceback  # For detailed error traceback
import subprocess  # For managing subprocesses
from subprocess import Popen, PIPE, CREATE_NEW_CONSOLE  # Import subprocess utilities
from os import remove  # For deleting files
from sys import argv  # For accessing script arguments
import pathlib  # For working with file paths in a platform-independent way
from pathlib import Path  # Simplifies working with file system paths
import zipfile  # For working with zip files
from zipfile import ZipFile  # Provides utilities for zip file operations
from os import walk  # For directory traversal
import os, shutil, glob  # Utilities for file operations
import sys  # System-specific parameters and functions
import threading  # For thread-based concurrency
import _thread  # Lower-level thread module
import urllib.request  # For downloading files from URLs
import queue  # Thread-safe queue for multithreading
import time  # For adding delays during retries

# Retrieves the absolute path of the current script
def get_scriptpath():
    try:
        # Returns the directory where the script resides
        scriptpath = str(pathlib.Path(__file__).parent.absolute())
        return scriptpath
    except Exception as err:
        # Logs any exception that occurs
        print(f"Error getting script path: {err}")
        return None  # Ensures a None return on failure

# Attempts to open a README file located in a specific directory
def open_readme(installpath):
    try:
        os.chdir('/')  # Changes the working directory temporarily
        # Opens the README file in the specified install directory
        os.startfile(os.path.join(installpath, "Der Sauger", "README.txt"))
        os.chdir('/')  # Reverts back to the root directory
    except Exception as err:
        # Logs an error if the file cannot be opened
        print(f"Error opening README file: {err}")

# Downloader class encapsulates file download and extraction logic
class Downloader:
    def __init__(self):
        # Initialize state flags and path variables
        self.isdownloaded = False  # Indicates if download was successful
        self.isunzipped = False  # Indicates if unzip was successful
        self.installpath = None  # Installation directory path
        self.unzippath = None  # Path to extracted files
        self.extensionpath = None  # Final path after reorganization

    # Handles downloading, extracting, and reorganizing files
    def download_and_unzip(self, installpath):
        # Verifies that the installation path exists
        if not os.path.exists(installpath):
            print(f"Install path does not exist: {installpath}")
            return False

        # Defines the path to save the downloaded zip file
        self.installpath = installpath
        zipfilepath = os.path.join(installpath, "UPDATE_DerSauger.zip")
        print(f'{{"Info": zipfilepath: {zipfilepath}}}')

        # Handle missing `UPDATE_DerSauger.zip`
        if not os.path.isfile(zipfilepath):
            print("File 'UPDATE_DerSauger.zip' is missing. Attempting to resolve...")
            if not self.handle_missing_zip(zipfilepath):
                print("Failed to resolve missing zip file.")
                return False

        # Extracts the zip file contents
        if not self.unzip(zipfilepath, installpath):
            print("Unzip failed.")
            return False

        # Updates paths for further operations
        self.unzippath = os.path.join(installpath, "DerSauger-main")

        # Removes the zip file after extraction
        try:
            os.remove(zipfilepath)
        except Exception as err:
            print(f"Error removing zip file: {err}")
            if not self.handle_remove_failure(zipfilepath):
                print("Failed to resolve file removal issue.")
                return False

        # Moves specific files from extracted folder to install path
        self.extensionpath = os.path.join(installpath, "DerSauger-main", "Der Sauger")
        try:
            shutil.move(self.extensionpath, installpath)
        except Exception as err:
            print(f"Error moving files: {err}")
            return False

        # Updates extension path to reflect its new location
        self.extensionpath = os.path.join(installpath, "Der Sauger")

        # Cleans up the now-empty extracted directory
        try:
            shutil.rmtree(self.unzippath)
        except Exception as err:
            print(f"Error removing directory: {err}")

        return True  # Signals success

    # Handles missing UPDATE_DerSauger.zip file by attempting three sequential approaches
     def handle_missing_zip(self, zipfilepath):
        # Attempts to resolve missing zip file using three sequential approaches
        attempts = [
            lambda: self.download("https://github.com/GrafKrausula/DerSauger/archive/main.zip", zipfilepath),
            lambda: self.try_alternative_source(zipfilepath),
            lambda: self.use_bitsadmin(zipfilepath),
            lambda: self.prompt_user_for_file(zipfilepath)
        ]
        for attempt in attempts:
            if attempt():
                return True
        return False

    def try_alternative_source(self, zipfilepath):
        print("Attempting to download from an alternative source...")
        alternative_url = "https://backupserver.com/DerSauger/main.zip"
        return self.download(alternative_url, zipfilepath)

    def use_bitsadmin(self, zipfilepath):
        print("Attempting to download using 'bitsadmin.exe'...")
        url = "https://github.com/GrafKrausula/DerSauger/archive/main.zip"
        try:
            # Constructs the bitsadmin command
            command = f'bitsadmin.exe /transfer "DownloadZip" {url} "{zipfilepath}"'
            # Executes the command in the Windows shell
            result = subprocess.run(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            print(result.stdout)
            print(result.stderr)
            # Check for success
            if result.returncode == 0:
                print("Download via bitsadmin.exe succeeded.")
                return True
            else:
                print("Download via bitsadmin.exe failed.")
                return False
        except Exception as err:
            print(f"Error using bitsadmin.exe: {err}")
            return False

    def prompt_user_for_file(self, zipfilepath):
        print("Prompting user to manually place the zip file...")
        input(f"Please place the 'UPDATE_DerSauger.zip' file in the folder: {zipfilepath}. Press ENTER when done.")
        return os.path.isfile(zipfilepath)


    # Handles failure to remove the zip file by trying alternative methods
    def handle_remove_failure(self, filepath):
        attempts = [
            lambda: self.try_chmod_and_remove(filepath),
            lambda: self.try_del_command(filepath),
            lambda: self.ask_user_to_delete(filepath)
        ]
        for attempt in attempts:
            if attempt():
                return True
        return False

    def try_chmod_and_remove(self, filepath):
        print("Attempting to modify permissions and retry delete...")
        try:
            os.chmod(filepath, 0o777)
            os.remove(filepath)
            return True
        except Exception as err:
            print(f"Failed chmod/remove attempt: {err}")
            return False

    def try_del_command(self, filepath):
        print("Attempting to delete file using 'del' command...")
        try:
            subprocess.run(["del", "/f", filepath], shell=True, check=True)
            return True
        except Exception as err:
            print(f"Failed del command attempt: {err}")
            return False

    def ask_user_to_delete(self, filepath):
        print("Prompting user to manually delete the file...")
        input(f"Please delete the file manually: {filepath}. Press ENTER when done.")
        return not os.path.isfile(filepath)

    # Downloads a file from a URL, with retries for resiliency
    def download(self, url, file_name):
        print('{"Info": Downloading. Please wait and do not close this window...}')
        retries = 3  # Number of retry attempts
        while retries > 0:
            try:
                # Downloads and writes file content
                with urllib.request.urlopen(url) as response, open(file_name, 'wb') as out_file:
                    shutil.copyfileobj(response, out_file)
                self.isdownloaded = True  # Marks successful download
                return True
            except Exception as err:
                print(f"Error downloading file: {err}")
                retries -= 1  # Decrement retries on failure
                if retries > 0:
                    print(f"Retrying download ({retries} attempts left)...")
                    time.sleep(2)  # Adds a delay before retrying
                else:
                    print("Failed to download after multiple attempts.")
                    return False  # Fails if all retries are exhausted

    # Extracts the contents of a zip file, with retries for resiliency
    def unzip(self, download_zip, installpath):
        print('{"Info": Unzipping download...}')
        retries = 3  # Number of retry attempts
        while retries > 0:
            try:
                # Verifies the file is a valid zip file
                if zipfile.is_zipfile(download_zip):
                    # Extracts contents to the installation path
                    with ZipFile(download_zip, 'r') as zipObj:
                        zipObj.extractall(installpath)
                    self.isunzipped = True  # Marks successful extraction
                    return True
                else:
                    print("Downloaded file is not a valid zip file.")
                    return False
            except Exception as err:
                print(f"Error unzipping file: {err}")
                retries -= 1  # Decrement retries on failure
                if retries > 0:
                    print(f"Retrying unzip ({retries} attempts left)...")
                    time.sleep(2)  # Adds a delay before retrying
                else:
                    print("Failed to unzip after multiple attempts.")
                    return False  # Fails if all retries are exhausted

    # Returns the path to the extension
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
    try:
        installpath = get_scriptpath()
        if not installpath:
            raise ValueError("Could not determine script path.")

        downloader = Downloader()
        if not downloader.download_and_unzip(installpath):
            raise RuntimeError("Download and unzip process failed.")

        # Assuming DeployedPathvariables is defined elsewhere
        dpv = DeployedPathvariables(downloader.get_extensionpath())
        dpv.check_pathvariables()
        dpv.add_registry()
        # dpv.restart_explorer()

        x = input("Finished. Press ENTER to exit...")

        open_readme(installpath)

        try:
            remove(argv[0])  # Removes the script file
            print("Script file removed successfully.")
        except Exception as err:
            print(f"Failed to remove script file: {err}")

    except Exception as err:
        traceback.print_exc()
        x = input("An error occurred! Press ENTER to exit...")

if __name__ == '__main__':
    Main()

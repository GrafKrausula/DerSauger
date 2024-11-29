import os
import sys
import subprocess
import traceback
import pathlib
import zipfile
import shutil
import time
import urllib.request


# Retrieves the absolute path of the current script
def get_scriptpath():
    try:
        scriptpath = str(pathlib.Path(__file__).parent.absolute())
        return scriptpath
    except Exception as err:
        print(f"Error getting script path: {err}")
        return None


# Detects if the script is running with admin privileges
def is_admin():
    try:
        return os.getuid() == 0  # Works on Unix
    except AttributeError:
        # For Windows, check admin access by creating a privileged file in a system-protected directory
        try:
            temp_file = os.path.join(os.environ.get("SYSTEMROOT", "C:\\Windows"), "temp", "test_admin_privileges.tmp")
            with open(temp_file, "w") as file:
                file.write("test")
            os.remove(temp_file)
            return True
        except Exception:
            return False


# Re-launches the script with admin privileges
def relaunch_as_admin():
    try:
        script = sys.executable
        params = " ".join([f'"{arg}"' for arg in sys.argv])
        cmd = f"{script} {params}"
        subprocess.run(["runas", "/user:Administrator", cmd], shell=True)
        return True
    except Exception as err:
        print(f"Failed to relaunch as admin: {err}")
        return False


# Downloader class encapsulates file download and extraction logic
class Downloader:
    def __init__(self):
        self.isdownloaded = False
        self.isunzipped = False
        self.installpath = None
        self.unzippath = None
        self.extensionpath = None

    # Handles downloading, extracting, and reorganizing files
    def download_and_unzip(self, installpath):
        if not os.path.exists(installpath):
            print(f"Install path does not exist: {installpath}")
            return False

        self.installpath = installpath
        zipfilepath = os.path.join(installpath, "UPDATE_DerSauger.zip")
        print(f'{{"Info": zipfilepath: {zipfilepath}}}')

        if not os.path.isfile(zipfilepath):
            print("File 'UPDATE_DerSauger.zip' is missing. Attempting to resolve...")
            if not self.handle_missing_zip(zipfilepath):
                print("Failed to resolve missing zip file.")
                return False

        if not self.unzip(zipfilepath, installpath):
            print("Unzip failed.")
            return False

        self.unzippath = os.path.join(installpath, "DerSauger-main")

        try:
            os.remove(zipfilepath)
        except Exception as err:
            print(f"Error removing zip file: {err}")
            if not self.handle_remove_failure(zipfilepath):
                print("Failed to resolve file removal issue.")
                return False

        self.extensionpath = os.path.join(installpath, "DerSauger-main", "Der Sauger")
        try:
            shutil.move(self.extensionpath, installpath)
        except Exception as err:
            print(f"Error moving files: {err}")
            return False

        self.extensionpath = os.path.join(installpath, "Der Sauger")

        try:
            shutil.rmtree(self.unzippath)
        except Exception as err:
            print(f"Error removing directory: {err}")

        return True

    # Handles missing UPDATE_DerSauger.zip file by attempting three sequential approaches
    def handle_missing_zip(self, zipfilepath):
        attempts = [
            lambda: self.download("https://github.com/GrafKrausula/DerSauger/archive/main.zip", zipfilepath),
            lambda: self.try_alternative_source(zipfilepath),
            lambda: self.use_bitsadmin(zipfilepath),
            lambda: self.relaunch_for_privileges(zipfilepath),  # Admin privilege escalation
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
            command = f'bitsadmin.exe /transfer "DownloadZip" {url} "{zipfilepath}"'
            result = subprocess.run(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            print(result.stdout)
            print(result.stderr)
            return result.returncode == 0
        except Exception as err:
            print(f"Error using bitsadmin.exe: {err}")
            return False

    def relaunch_for_privileges(self, zipfilepath):
        print("Attempting to relaunch with admin privileges...")
        if not is_admin():
            if relaunch_as_admin():
                print("Admin relaunch succeeded.")
                return os.path.isfile(zipfilepath)
            else:
                print("Admin relaunch failed.")
                return False
        else:
            print("Already running as admin.")
            return False

    def prompt_user_for_file(self, zipfilepath):
        print("Prompting user to manually place the zip file...")
        input(f"Please place the 'UPDATE_DerSauger.zip' file in the folder: {zipfilepath}. Press ENTER when done.")
        return os.path.isfile(zipfilepath)

    def download(self, url, file_name):
        print('{"Info": Downloading. Please wait and do not close this window...}')
        retries = 3
        while retries > 0:
            try:
                with urllib.request.urlopen(url) as response, open(file_name, 'wb') as out_file:
                    shutil.copyfileobj(response, out_file)
                self.isdownloaded = True
                return True
            except Exception as err:
                print(f"Error downloading file: {err}")
                retries -= 1
                if retries > 0:
                    print(f"Retrying download ({retries} attempts left)...")
                    time.sleep(2)
                else:
                    print("Failed to download after multiple attempts.")
                    return False

    def unzip(self, download_zip, installpath):
        print('{"Info": Unzipping download...}')
        retries = 3
        while retries > 0:
            try:
                if zipfile.is_zipfile(download_zip):
                    with ZipFile(download_zip, 'r') as zipObj:
                        zipObj.extractall(installpath)
                    self.isunzipped = True
                    return True
                else:
                    print("Downloaded file is not a valid zip file.")
                    return False
            except Exception as err:
                print(f"Error unzipping file: {err}")
                retries -= 1
                if retries > 0:
                    print(f"Retrying unzip ({retries} attempts left)...")
                    time.sleep(2)
                else:
                    print("Failed to unzip after multiple attempts.")
                    return False

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

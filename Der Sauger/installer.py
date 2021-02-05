import traceback
import subprocess
from subprocess import Popen, PIPE

def get_installpath():

    scriptpath = str(pathlib.Path(__file__).parent.absolute())
    return scriptpath

class DeployedPathvar:
    def __init__(self):
        self.ffmpeg = False
        self.youtube = False

    def check_pathvariables(self):

        if self.are_pathvariables_complete() == False:
            self.add_missing_pathvariable()
            self.check_pathvariables()
        else:
            return True

    def are_pathvariables_complete(self):

        #installcmd = f'cmd /c "cd /d {get_installpath()}'

        proc1 = subprocess.Popen("cmd /c SET PATH",stderr=subprocess.STDOUT,stdout=subprocess.PIPE)

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
        if self.ffmpeg == False:
            self.add_ffmpeg_path()
        if self.youtube == False:
            self.add_youtube_path()

        return True

    def add_ffmpeg_path(self):
        print("ffmpeg PATHVARIABLE added")
        return True

    def add_youtube_path(self):
        print("youtubeDL PATHVARIABLE added")
        return True

def Main():

    dpv = DeployedPathvar()
    dpv.check_pathvariables()


    x = input("Finished. Press Any key to exit...")


if __name__ == '__main__':


    try:

        Main()

    except Exception as err:

        traceback.print_exc()
        #print(err)
        x = input("An error occured! Press Any key to exit...")

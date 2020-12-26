import threading
import traceback
import os
import pathlib
from pathlib import Path
import subprocess
from subprocess import Popen, PIPE
from subprocess import Popen, CREATE_NEW_CONSOLE
from os import walk
import os, shutil, glob
import time

def createconvertcmd(url):

    convertcmd = f'cmd /c "cd /d {downloadpath}'
    convertcmd+= f" && youtube-dl -f bestvideo+bestaudio/best {url}"
    convertcmd+= ' " '
    #print(convertcmd)
    #send_message('{"cmd": %s}' % convertcmd)
    return convertcmd


def convertfiles(url):
    #proc1 = subprocess.Popen(createconvertcmd(url),stderr=subprocess.STDOUT,stdout=subprocess.PIPE)
    #proc1 = subprocess.Popen(createconvertcmd(url),stderr=subprocess.STDOUT,stdout=subprocess.PIPE)
    #subprocess.run(["cmd.exe", "/c", "start", createconvertcmd(url)], timeout=15)
    #convertcmd = f'cd /d {downloadpath}'
    #convertcmd+= f' && youtube-dl -f bestvideo+bestaudio/best {url}'

    #subprocess.run(["cmd.exe", "/c", "start", convertcmd], timeout=15)
    #proc1 = subprocess.run(["cmd.exe", "/c","start", "youtube-dl -f bestvideo+bestaudio/best"])

    #proc1 = subprocess.Popen(createconvertcmd(url), creationflags=CREATE_NEW_CONSOLE) #wörks
    proc1 = subprocess.Popen(f'youtube-dl -f bestvideo+bestaudio/best {url}', creationflags=CREATE_NEW_CONSOLE)
    stdoutdata, stderrdata = proc1.communicate()
    print(proc1.returncode)
    #os.system(f"start %s" %createconvertcmd(url))

    #subprocess.run(["cmd.exe", "/c", "start", "dir"], timeout=15)

    #while True:
    #    line = proc1.stdout.readline()
    #    print(f"{line}")

    #    comparision = str(line) == "b\'\\r\\n\'"
    #    if comparision:
    #        print("DOWNLOAD FINISHED!")
    #        break;


def worker(num):
    """thread worker function"""

    try:
        convertfiles(url)
    except Exception as err:

        traceback.print_exc()
        #print(err)
        x = input("An error occured! Press Any key to exit...")

    print('Worker: %s' % num)
    return

threads = []
url = "https://www.youtube.com/watch?v=dO7gB5ATJr8"
downloadpath = "E:\Runterladungen!"
for i in range(5):
    t = threading.Thread(target=worker, args=(i,))
    threads.append(t)
    t.start()
    print(threads)

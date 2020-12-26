import pathlib
from pathlib import Path
import traceback

try:
    scriptpath = str(pathlib.Path(__file__).parent.absolute())
    print(scriptpath)
    convertpath = scriptpath.replace(r"\nativeMessaging\host\host","")
    print(convertpath)

except Exception as err:

    traceback.print_exc()
    #print(err)
    x = input("An error occured! Press Any key to exit...")

input("Press any key to Exit...")

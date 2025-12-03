import sys
import os
import traceback
import subprocess
import shutil
from datetime import datetime

"""
Dependence:
NEEDS FFMPEG AS PATHVARIABLE!!!!!!!!
"""

# ============== LOGGING ==============
LOG_DIR = os.path.expanduser("~\\Documents\\DerSauger_Logs")
LOG_FILE = os.path.join(LOG_DIR, "WAVing_All_VIDS.log")
LOG_RETENTION_DAYS = 30  # Logs älter als 30 Tage werden gelöscht
MAX_LOG_SIZE_MB = 10     # Maximale Größe einer Log-Datei

def ensure_log_dir():
    """Erstellt Log-Verzeichnis falls nicht vorhanden."""
    if not os.path.exists(LOG_DIR):
        os.makedirs(LOG_DIR)

def rotate_log_if_needed():
    """Rotiert Log-Datei wenn sie zu groß wird."""
    if os.path.exists(LOG_FILE):
        size_mb = os.path.getsize(LOG_FILE) / (1024 * 1024)
        if size_mb >= MAX_LOG_SIZE_MB:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            archived_name = LOG_FILE.replace(".log", f"_{timestamp}.log")
            os.rename(LOG_FILE, archived_name)

def cleanup_old_logs():
    """Löscht Logs älter als LOG_RETENTION_DAYS."""
    if not os.path.exists(LOG_DIR):
        return
    now = datetime.now()
    for filename in os.listdir(LOG_DIR):
        filepath = os.path.join(LOG_DIR, filename)
        if os.path.isfile(filepath):
            file_age_days = (now - datetime.fromtimestamp(os.path.getmtime(filepath))).days
            if file_age_days > LOG_RETENTION_DAYS:
                try:
                    os.remove(filepath)
                except Exception:
                    pass

def log(message, level="INFO"):
    """
    Schreibt Log-Nachricht in Datei und stdout.
    Levels: INFO, WARN, ERROR, DEBUG
    """
    ensure_log_dir()
    rotate_log_if_needed()
    
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_line = f"[{timestamp}] [{level}] {message}"
    
    # Console output
    print(log_line)
    
    # File output
    try:
        with open(LOG_FILE, "a", encoding="utf-8") as f:
            f.write(log_line + "\n")
    except Exception as e:
        print(f"[WARN] Could not write to log file: {e}")

def log_separator():
    """Fügt Trennlinie für neue Session hinzu."""
    log("=" * 60)
    log(f"Session started - WAVing_All_VIDS.py")
    log("=" * 60)

# ============== END LOGGING ==============
def getfilelist(filetype, path):

    allfiles = []
    allfiles = os.listdir(path)
    #print(allfiles)
    filetypefiles = []
    for file in allfiles:
        if file.lower().endswith(f".{filetype.lower()}"):
            filetypefiles.append(file)

    #print(webmfiles)
    return filetypefiles

def getfilelists(convertpath,supportedfiletypes):

    filelists = []
    log(f"Supported Formats: {supportedfiletypes}")
    for supportedfiletype in supportedfiletypes:
        #print(supportedfiletype)
        filelists.append(getfilelist(supportedfiletype,convertpath))

    return filelists

def removeillegalexpressions(filepath):

    if "&" in filepath:

        #print(f"RAWPATH: {filepath}")

        cleanedfilepath = filepath.replace("&","UND")
        #print(f"RAWPATH: {cleanedfilepath}")

        os.rename(filepath, cleanedfilepath)

        filepath = cleanedfilepath

    return filepath

def typeconvertcmd(filetype,filelist,supportedfiletypes):

    #!supportedfiletypes = [convertformat,"mkv","mp4","webm","avi","m4a","mp3","aax"]!
    convertformat = supportedfiletypes[0]
    convertcmd= ""

    for file in filelist:

        input = file
        output = input.replace(f".{filetype}","")
        convertcmd+=(f" && ffmpeg -y -i \"{input}\" \"{output}.{convertformat}\"")
        #print(webmfiles)

    return convertcmd

def createconvertcmd(convertpath,supportedfiletypes):

    convertcmd = f'cmd /c "cd /d {convertpath}'

    filelists = getfilelists(convertpath,supportedfiletypes)
    log(f"File lists: {filelists}", "DEBUG")


    for filelist in filelists:
        indexint = filelists.index(filelist) #nummer des momentanen
        filetype = supportedfiletypes[indexint]
        if filelist != []: log(f"Found {filetype} files: {filelist}")
        convertcmd+= typeconvertcmd(filetype,filelist,supportedfiletypes)


    convertcmd+= ' " '

    log(f"Convert command: {convertcmd}", "DEBUG")
    return convertcmd

def makedir(convertpath,new_fldr_name):

    new_fldr_name = new_fldr_name.upper()

    new_fldr = os.path.join(convertpath, new_fldr_name)
    #print(new_fldr)

    try:
      os.makedirs(new_fldr) ## it creates the destination folder in capslock
      log(f"Created folder: {new_fldr}")
    except:
      log(f"{new_fldr_name} Folder already exists", "DEBUG")

    return new_fldr

def makedirlist(convertpath,supportedfiletypes):
    filetypedirlist = []

    for filetype in supportedfiletypes:
        filetypedirlist.append(makedir(convertpath,filetype))
    #print(filetypedirlist)
    return filetypedirlist

def convertfiles(convertpath, supportedfiletypes):
    filelists = getfilelists(convertpath, supportedfiletypes)
    convertformat = supportedfiletypes[0]
    log(f"Starting conversion - Target format: {convertformat}")
    log(f"File lists to process: {filelists}", "DEBUG")
    for filelist in filelists:
        indexint = filelists.index(filelist)
        filetype = supportedfiletypes[indexint]
        # Skip files that are already in the target format
        if filetype == convertformat:
            log(f"Skipping {len(filelist)} file(s) already in {convertformat} format")
            continue
        for file in filelist:
            input_file = os.path.join(convertpath, file)
            output_file = os.path.join(convertpath, file.replace(f'.{filetype}', f'.{convertformat}'))
            cmd = ["ffmpeg", "-y", "-i", input_file, output_file]
            proc = subprocess.Popen(cmd, stderr=subprocess.STDOUT, stdout=subprocess.PIPE)
            log(f"Converting: {file} -> {convertformat}")
            while True:
                cmdState = proc.poll()
                if cmdState is not None:
                    break
                line = proc.stdout.readline()
                # FFmpeg output nur bei DEBUG level loggen (sehr verbose)
            if proc.returncode == 0:
                log(f"Successfully converted: {file}")
            else:
                log(f"Conversion failed for: {file} (exit code: {proc.returncode})", "ERROR")
    log("CONVERSION FINISHED!")
    
def removeduplicatindestionation(destination,file):

    destinationfile = os.path.join(destination, file)
    #print(f"To:{destinationfile}")
    destinationfile_exists = os.path.exists(destinationfile)
    if destinationfile_exists == True:
        os.remove(destinationfile)
        log(f"Duplicate removed: {file}", "WARN")

def movefilestoroot(convertpath, downloadpath, filetypefolderlist,supportedfiletypes):


    inputfiletypes = list(supportedfiletypes)
    #inputfiletypefolderlist = filetypefolderlist

    del inputfiletypes[0] #Removes the wav
    #del inputfiletypefolderlist[0]

    for inputfiletype in inputfiletypes:
        #indexint = inputfiletypefolderlist.index(inputfiletypefolder)
        #print(inputfiletype)
        movefiletofolder(inputfiletype,downloadpath,convertpath)
        #movefiletofolder(inputfiletype,downloadpath2,convertpath)

def movefiletofolder(filetype, src_fldr, destination):

    #print(filetype,src_fldr,destination)
    err_count = 0
    success_count = 0
    errors = []
    #print(src_fldr)
    #print(filetype)
    for file in os.listdir(src_fldr):
        if file.endswith(f".{filetype}"):
            #print(src_fldr)
            #print(file)
            #input('DEBUG WAITING')
            rawfilepath = os.path.join(src_fldr, file)
            #print(f"From:{filepath}")

            filepath = removeillegalexpressions(rawfilepath)
            # Get the actual filename after potential rename
            actual_filename = os.path.basename(filepath)
            removeduplicatindestionation(destination, actual_filename)

            try:
                shutil.move(filepath, destination)
                log(f"Moved: {file} -> {destination}", "DEBUG")
                success_count+=1
            except Exception as err:
                errors.append(err)
                err_count+=1
                log(f"Failed to move: {file} from {src_fldr} - {err}", "ERROR")

    if err_count > 0:
        log(f"{err_count} MOVING ERROR(S) OCCURRED", "ERROR")
        log(f"Errors: {errors}", "ERROR")
    if success_count > 0: log(f"{success_count} file(s) successfully moved")

def movefilestofolders(convertpath,filetypefolderlist,supportedfiletypes):

    #print(filetypefolderlist, supportedfiletypes)

    for filetypefolder in filetypefolderlist:
        indexint = filetypefolderlist.index(filetypefolder) #nummer des momentanen
        #print(indexint)
        filetype = supportedfiletypes[indexint]
        #print(indexint, filetype)
        movefiletofolder(filetype,convertpath,filetypefolder)

def close():
    if not sys.argv[1] == "noinput": input('Press ENTER to exit')
    sys.exit()



def Main():
    # Logging initialisieren
    cleanup_old_logs()
    log_separator()

    convertfolder = "KONVERTIERUNG"
    convertpath = "E:\\RENDER OUTPUT"
    downloadpath = "E:\\Runterladungen!"
    convertformat = "wav"

    #als methode auslagern
    if len(sys.argv)>4: #Remember that sys.argv[0] is the name of the script
        try:
            convertpath = sys.argv[2]
            downloadpath = sys.argv[3]
            convertformat = sys.argv[4] #convertformat wird umgesetzt
            convertformat = convertformat.lower() #convertformat wird auf klein getrimmt
            log(f"Arguments received - convertpath: {convertpath}, downloadpath: {downloadpath}, format: {convertformat}")
        except Exception as err:
            log(f"Error parsing arguments: {err}", "ERROR")
            input('Screenshot the error above and contact the Developer. Press ENTER to exit.')
            sys.exit(1)

            #erstemal checken ob ordner 'KONVERTIERUNG' an convertpath existiert

    supportedfiletypes = [convertformat,"mkv","mp4","webm","avi","m4a","mp3","aax","opus"]

    log(f"Convert path: {convertpath}")
    log(f"Download path: {downloadpath}")
    log(f"Target format: {convertformat}")

    convertpath = makedir(convertpath,convertfolder) # Ordner KONVERTIERUNG erstellen und als path speichern
    filetypefolderlist = makedirlist(convertpath,supportedfiletypes)

    log(f"Working directory: {convertpath}")

    movefilestoroot(convertpath, downloadpath, filetypefolderlist, supportedfiletypes)

    convertfiles(convertpath,supportedfiletypes)

    log("Moving files to type folders...")

    movefilestofolders(convertpath,filetypefolderlist,supportedfiletypes)

    log("Session completed successfully")

    if len(sys.argv)>1:
        if not sys.argv[1] == "noinput": input('Press ENTER to exit') #lieber statt 'noinput' 'directextit'
    else:
        input('Press ENTER to exit')

    os._exit(0)

if __name__ == '__main__':


    try:

        Main()

    except Exception as err:

        log(f"FATAL ERROR: {err}", "ERROR")
        log(traceback.format_exc(), "ERROR")
        traceback.print_exc()
        x = input("An error occured! Press ENTER to exit...")

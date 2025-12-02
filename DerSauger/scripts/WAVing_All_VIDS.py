import sys
import os
import traceback
import subprocess
import shutil

""""
Dependence:
NEEDS FFMPEG AS PATHVARIABLE!!!!!!!!
"""
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
    print("Supported Formats: ", supportedfiletypes)
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
    print(filelists)


    for filelist in filelists:
        indexint = filelists.index(filelist) #nummer des momentanen
        filetype = supportedfiletypes[indexint]
        if filelist != []: print(f"Found {filetype} files: {filelist}")
        convertcmd+= typeconvertcmd(filetype,filelist,supportedfiletypes)


    convertcmd+= ' " '

    print(convertcmd)
    return convertcmd

def makedir(convertpath,new_fldr_name):

    new_fldr_name = new_fldr_name.upper()

    new_fldr = os.path.join(convertpath, new_fldr_name)
    #print(new_fldr)

    try:
      os.makedirs(new_fldr) ## it creates the destination folder in capslock
    except:
      print(f"{new_fldr_name} Folder already exists!")

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
    print("Supported Formats:", supportedfiletypes)
    print(filelists)
    for filelist in filelists:
        indexint = filelists.index(filelist)
        filetype = supportedfiletypes[indexint]
        # Skip files that are already in the target format
        if filetype == convertformat:
            print(f"Skipping {len(filelist)} file(s) already in {convertformat} format")
            continue
        for file in filelist:
            input_file = os.path.join(convertpath, file)
            output_file = os.path.join(convertpath, file.replace(f'.{filetype}', f'.{convertformat}'))
            cmd = ["ffmpeg", "-y", "-i", input_file, output_file]
            proc = subprocess.Popen(cmd, stderr=subprocess.STDOUT, stdout=subprocess.PIPE)
            while True:
                cmdState = proc.poll()
                if cmdState is not None:
                    break
                line = proc.stdout.readline()
                print(line)
    print("CONVERSION FINISHED!")
    
def removeduplicatindestionation(destination,file):

    destinationfile = os.path.join(destination, file)
    #print(f"To:{destinationfile}")
    destinationfile_exists = os.path.exists(destinationfile)
    if destinationfile_exists == True:
        os.remove(destinationfile)
        print(f"DUPLICAT {file} REMOVED")

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
                #print(f"{file} MOVED FROM {src_fldr} TO {destination}")
                success_count+=1
            except Exception as err:
                errors.append(err)
                err_count+=1
                print(f"{file} COULD NOT BE MOVED FROM {src_fldr}")

    if err_count > 0:
        print(f"{err_count} MOVING ERROR(S) OCCURED")
        print(f"ERRORS: {errors}")
    if success_count > 0: print(f"{success_count} FILE(S) SUCCESFULLY MOVED")

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

    convertfolder = "KONVERTIERUNG"
    convertpath = "E:\RENDER OUTPUT"
    downloadpath = "E:\Runterladungen!"
    convertformat = "wav"

    #als methode auslagern
    if len(sys.argv)>4: #Remember that sys.argv[0] is the name of the script
        try:
            convertpath = sys.argv[2]
            downloadpath = sys.argv[3]
            convertformat = sys.argv[4] #convertformat wird umgesetzt
            convertformat = convertformat.lower() #convertformat wird auf klein getrimmt
        except Exception as err:
            print(err)
            input('Screenshot the error above and contact the Developer. Press ENTER to exit.')
            sys.exit(1)

            #erstemal checken ob ordner 'KONVERTIERUNG' an convertpath existiert

    supportedfiletypes = [convertformat,"mkv","mp4","webm","avi","m4a","mp3","aax","opus"]

    #print(downloadpath)
    #print(convertpath)
    #print(supportedfiletypes)

    convertpath = makedir(convertpath,convertfolder) # Ordner KONVERTIERUNG erstellen und als path speichern
    filetypefolderlist = makedirlist(convertpath,supportedfiletypes)


    print(convertpath)


    movefilestoroot(convertpath, downloadpath, filetypefolderlist, supportedfiletypes)

    convertfiles(convertpath,supportedfiletypes)

    print("FILES WILL BE NOW MOVED")

    movefilestofolders(convertpath,filetypefolderlist,supportedfiletypes)

    if len(sys.argv)>1:
        if not sys.argv[1] == "noinput": input('Press ENTER to exit') #lieber statt 'noinput' 'directextit'
    else:
        input('Press ENTER to exit')

    os._exit(0)

if __name__ == '__main__':


    try:

        Main()

    except Exception as err:

        traceback.print_exc()
        #print(err)
        x = input("An error occured! Press ENTER to exit...")

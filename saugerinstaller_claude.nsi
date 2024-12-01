; Top level definitions
!define REG_KEY "Software\Google\Chrome\NativeMessagingHosts\com.google.chrome.example.echo"

OutFile "DerSaugerInstaller.exe"
InstallDir "$PROGRAMFILES\DerSauger"
RequestExecutionLevel admin

; Unicode support
Unicode True

!include "MUI2.nsh"
!include "nsDialogs.nsh"
!include "FileFunc.nsh"
!include "LogicLib.nsh"
!include "StrFunc.nsh"
!include "WordFunc.nsh"

; Logging macro
!define LogEx `!insertmacro LogEx`
!macro LogEx TEXT
    FileOpen $0 "$INSTDIR\install.log" a
    FileWrite $0 "${TEXT}$\r$\n"
    FileClose $0
!macroend

; Variables
Var Dialog
Var FFmpegCheckbox
Var FFmpegState
Var YtDlpCheckbox
Var YtDlpState
Var Python39Path
Var Python3Path

; UI Pages
!insertmacro MUI_PAGE_WELCOME
!insertmacro MUI_PAGE_DIRECTORY
Page custom InstallOptionsPage InstallOptionsLeave
!insertmacro MUI_PAGE_INSTFILES
!insertmacro MUI_PAGE_FINISH

!insertmacro MUI_LANGUAGE "German"

Section "Installieren"
    SetOutPath "$INSTDIR"
    ${LogEx} "=== Installation started at $INSTDIR ==="
    
    CreateDirectory "$INSTDIR"
    File /r "DerSauger\*.*"
    ${LogEx} "Copied DerSauger files"

    ; Create uninstaller first
    WriteUninstaller "$INSTDIR\uninstall.exe"
    ${LogEx} "Created uninstaller"

    Exec '"$INSTDIR\README.txt"'

    ; Python installations check
    ${LogEx} "Checking Python installations..."
    Call CheckPythonNewest
    Call CheckPython39

    ; Virtual environments setup
    ${LogEx} "Setting up virtual environments..."
    Call InstallPython39Venv

    ${LogEx} "Checking package requirements..."
    Call CheckNeededPythonVersionForPackages
    Call CheckPythonNeeded
    Call InstallNeededPythonVenv

    ${If} $YtDlpState == ${BST_CHECKED}
        ${LogEx} "Installing yt-dlp..."
        Call InstallYtDlp
    ${EndIf}

    ; Registry handling
    ReadRegStr $R2 HKCU "${REG_KEY}" ""
    StrCmp $R2 "" RegKeyNotFound

    MessageBox MB_YESNO "Der Registrierungseintrag für den Native Messaging Host existiert bereits. Überschreiben?" IDYES RegOverwrite IDNO RegSkip
    RegOverwrite:
        ${LogEx} "Overwriting registry key ${REG_KEY}"
        WriteRegStr HKCU "${REG_KEY}" "" "$INSTDIR\nativeMessaging\com.google.chrome.example.echo-win.json"
        Goto RegKeyDone
    RegSkip:
        ${LogEx} "Keeping existing registry entry"
        MessageBox MB_OK "Der bestehende Registrierungseintrag wurde nicht geändert."
        Goto RegKeyDone
    RegKeyNotFound:
        ${LogEx} "Creating new registry key"
        WriteRegStr HKCU "${REG_KEY}" "" "$INSTDIR\nativeMessaging\com.google.chrome.example.echo-win.json"
    RegKeyDone:

    ${If} $FFmpegState == ${BST_CHECKED}
        ${LogEx} "Installing FFmpeg..."
        Call InstallFFmpeg
    ${EndIf}

    ; Environment update
    MessageBox MB_YESNO "Der Datei-Explorer muss neu gestartet werden, damit die Änderungen wirksam werden. Jetzt neu starten?" IDYES RestartExplorer IDNO NoRestart
    RestartExplorer:
        ${LogEx} "Restarting Explorer..."
        ExecWait '"$INSTDIR\Reloadpath.bat"'
        Goto EndInstall
    NoRestart:
        ${LogEx} "Explorer restart skipped"
        MessageBox MB_OK "Bitte starten Sie Ihren Computer neu, damit die Änderungen wirksam werden."
    EndInstall:
        ${LogEx} "=== Installation completed ==="
SectionEnd

Function CheckPython39
    ${LogEx} "Checking Python 3.9..."
    ReadRegStr $Python39Path HKLM "SOFTWARE\Python\PythonCore\3.9\InstallPath" ""
    ${If} $Python39Path == ""
        ReadRegStr $Python39Path HKCU "SOFTWARE\Python\PythonCore\3.9\InstallPath" ""
    ${EndIf}

    ${If} $Python39Path == ""
        ${LogEx} "Python 3.9 not found, attempting installation"
        MessageBox MB_OKCANCEL "Python 3.9 ist nicht installiert. Möchten Sie es jetzt installieren?" IDOK InstallPython39 IDCANCEL +2
        Abort

        InstallPython39:
            ExecWait '"$SYSDIR\winget.exe" install --id Python.Python.3.9 -e --silent'
            ${LogEx} "Python 3.9 installation attempted"
            ReadRegStr $Python39Path HKLM "SOFTWARE\Python\PythonCore\3.9\InstallPath" ""
            ${If} $Python39Path == ""
                ${LogEx} "Python 3.9 installation failed"
                MessageBox MB_OK "Python 3.9 Installation fehlgeschlagen."
                Abort
            ${EndIf}
    ${Else}
        StrCpy $Python39Path $Python39Path -1
        ${LogEx} "Python 3.9 found at: $Python39Path"
    ${EndIf}
FunctionEnd

Function CheckPythonNewest
    ${LogEx} "Checking latest Python installation..."
    nsExec::ExecToStack 'where python'
    Pop $0
    Pop $Python3Path

    ${If} $Python3Path == ""
        ${LogEx} "No Python installation found in PATH"
        MessageBox MB_OKCANCEL "Python 3 ist nicht installiert oder nicht im PATH. Möchten Sie es jetzt installieren?" IDOK InstallPython3 IDCANCEL +2
        Abort

        InstallPython3:
            ${LogEx} "Installing latest Python 3..."
            ExecWait '"$SYSDIR\winget.exe" install --id Python.Python.3 -e --silent'
            nsExec::ExecToStack 'where python'
            Pop $0
            Pop $Python3Path
            ${If} $Python3Path == ""
                ${LogEx} "Python installation failed"
                MessageBox MB_OK "Python 3 Installation fehlgeschlagen."
                Abort
            ${EndIf}
    ${EndIf}
    ${LogEx} "Latest Python found at: $Python3Path"
FunctionEnd

Function CheckNeededPythonVersionForPackages
    ${LogEx} "Checking package version requirements..."
    CreateDirectory "$PLUGINSDIR\tmp"
    
    ; Fixed PowerShell command
    nsExec::ExecToStack 'powershell -Command "$req = (Invoke-WebRequest -Uri https://pypi.org/pypi/yt-dlp/json -UseBasicParsing | ConvertFrom-Json).info.requires_python; if($req){$req}else{\">=3.9\"}"'
    Pop $0
    Pop $R0
    
    ${LogEx} "Required Python version: $R0"
    StrCpy $R1 $R0
FunctionEnd

Function InstallNeededPythonVenv
    ${LogEx} "Setting up Python virtual environments..."
    ${If} $Python39Path != ""
        ExecWait '"$Python39Path\python.exe" -m venv "$INSTDIR\app_venv"'
        ${LogEx} "Created app_venv"
        
        ExecWait '"$INSTDIR\app_venv\Scripts\python.exe" -m pip install --upgrade pip'
        ${LogEx} "Upgraded pip in app_venv"
        
        CreateDirectory "$INSTDIR\app_venv\pip"
        FileOpen $0 "$INSTDIR\app_venv\pip\pip.ini" w
        FileWrite $0 "[global]$\r$\n"
        FileWrite $0 "no-cache-dir = false$\r$\n"
        FileWrite $0 "find-links = $INSTDIR\packages$\r$\n"
        FileClose $0
        ${LogEx} "Created pip configuration"
        
        CreateDirectory "$INSTDIR\packages"
    ${EndIf}
    
    ${If} $YtDlpState == ${BST_CHECKED}
        ${If} $Python3Path != ""
            ExecWait '"$Python3Path" -m venv "$INSTDIR\ytdlp_venv"'
            ExecWait '"$INSTDIR\ytdlp_venv\Scripts\python.exe" -m pip install --upgrade pip'
            ${LogEx} "Created and configured ytdlp_venv"
        ${EndIf}
    ${EndIf}
    
    FileOpen $0 "$INSTDIR\activate_env.bat" w
    FileWrite $0 '@echo off$\r$\n'
    FileWrite $0 'call "$INSTDIR\app_venv\Scripts\activate.bat"$\r$\n'
    FileWrite $0 'set PATH=%PATH%;%~dp0\ytdlp_venv\Scripts$\r$\n'
    FileClose $0
    ${LogEx} "Created environment activation script"
FunctionEnd

Function InstallYtDlp
    ${LogEx} "Installing yt-dlp..."
    ExecWait '"$INSTDIR\ytdlp_venv\Scripts\python.exe" -m pip install --no-deps -U yt-dlp'
    ${LogEx} "yt-dlp installation completed"
FunctionEnd

Function InstallFFmpeg
    ${LogEx} "Installing FFmpeg..."
    ClearErrors
    ExecWait '"$SYSDIR\where.exe" winget' $0

    IfErrors FFmpegWingetNotFound FFmpegWingetFound

    FFmpegWingetFound:
        ExecWait '"$SYSDIR\winget.exe" install --id Gyan.FFmpeg --silent'
        ${LogEx} "FFmpeg installed via winget"
        Return

    FFmpegWingetNotFound:
        ${LogEx} "Winget not found, manual FFmpeg installation required"
        MessageBox MB_OK "Winget ist nicht installiert. Bitte installieren Sie FFmpeg manuell von https://www.gyan.dev/ffmpeg/builds/ und fügen Sie es dem PATH hinzu."
        Return
FunctionEnd

Function CheckPythonNeeded
    ${LogEx} "Verifying Python version requirements..."
    ${If} $R1 == ""
        ${LogEx} "No specific version requirement found, using default (>=3.9)"
        StrCpy $R1 ">=3.9"
    ${EndIf}

    ; Extract version number from requirement string using initialized StrRep
    Push $R1
    Push ">="
    Push ""
    Call StrRep
    Pop $R2
    ${LogEx} "Checking for Python version $R2"

    ; Check Python 3.9 first
    ${If} $Python39Path != ""
        ${LogEx} "Using Python 3.9 from: $Python39Path"
        Return
    ${EndIf}

    ; Check system Python
    ${If} $Python3Path != ""
        nsExec::ExecToStack '"$Python3Path" -c "import sys; print(\"%d.%d\" % sys.version_info[:2])"'
        Pop $0
        Pop $R3
        ${LogEx} "Found Python version: $R3"
        
        ; Compare versions
        ${VersionCompare} $R3 $R2 $R4
        ${If} $R4 >= 0
            ${LogEx} "System Python meets version requirement"
            Return
        ${EndIf}
    ${EndIf}

    ; No suitable version found
    ${LogEx} "No suitable Python version found, will install Python 3.9"
    Call CheckPython39
FunctionEnd

Function InstallOptionsPage
    nsDialogs::Create 1018
    Pop $Dialog
    ${If} $Dialog == error
        ${LogEx} "Failed to create options dialog"
        Abort
    ${EndIf}

    ${NSD_CreateCheckbox} 10 10 100% 12u "FFmpeg-Backend installieren"
    Pop $FFmpegCheckbox
    ${NSD_SetState} $FFmpegCheckbox ${BST_CHECKED}

    ${NSD_CreateCheckbox} 10 30 100% 12u "yt-dlp Backend installieren"
    Pop $YtDlpCheckbox
    ${NSD_SetState} $YtDlpCheckbox ${BST_CHECKED}

    nsDialogs::Show
FunctionEnd

Function InstallOptionsLeave
    ${NSD_GetState} $FFmpegCheckbox $FFmpegState
    ${NSD_GetState} $YtDlpCheckbox $YtDlpState
    ${LogEx} "Options selected: FFmpeg=$FFmpegState, yt-dlp=$YtDlpState"
FunctionEnd

Section "un.Uninstall"
    ${LogEx} "=== Uninstallation started ==="
    
    Call un.CleanupPythonEnvs
    
    Delete "$INSTDIR\*.*"
    RMDir /r "$INSTDIR"
    ${LogEx} "Removed installation directory"

    DeleteRegKey HKCU "${REG_KEY}"
    ${LogEx} "Removed registry entries"
    
    MessageBox MB_OK "Die Registrierungseinträge wurden entfernt."
    MessageBox MB_OK "Die Chrome-Erweiterung wurde deinstalliert."
    
    ${LogEx} "=== Uninstallation completed ==="
SectionEnd

Function un.CleanupPythonEnvs
    ${LogEx} "Cleaning up Python virtual environments..."
    RMDir /r "$INSTDIR\app_venv"
    RMDir /r "$INSTDIR\ytdlp_venv"
FunctionEnd

; Initialize string functions
${StrCase}
${StrClb}
${StrIOToNSIS}
${StrLoc}
${StrNSISToIO}
${StrRep}
${StrSort}
${StrStr}
${StrStrAdv}
${StrTok}
${StrTrimNewLines}

; Initialize string functions before use
!insertmacro StrCase
!insertmacro StrClb
!insertmacro StrIOToNSIS
!insertmacro StrLoc
!insertmacro StrNSISToIO
!insertmacro StrRep
!insertmacro StrSort
!insertmacro StrStr
!insertmacro StrStrAdv
!insertmacro StrTok
!insertmacro StrTrimNewLines
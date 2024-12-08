; Top level definitions
!define REG_KEY "Software\Google\Chrome\NativeMessagingHosts\com.google.chrome.dersauger.echo"


Name "DerSauger"
OutFile "DerSaugerInstaller.exe"
InstallDir "$LOCALAPPDATA\Programs\DerSauger"
RequestExecutionLevel user

; Unicode support
Unicode True

!include "MUI2.nsh"
;!include "nsDialogs.nsh"
!include "FileFunc.nsh"
;!include "LogicLib.nsh"

Var Dialog
Var FFmpegCheckbox
Var FFmpegState
Var YtDlpCheckbox
Var YtDlpState
Var Python39Path
Var PythonPackageNeededVersionDot
Var PythonPackageNeededVersionNoDot
Var PythonPackageNeededPath

; UI Pages
!insertmacro MUI_PAGE_WELCOME
!insertmacro MUI_PAGE_DIRECTORY
Page custom InstallOptionsPage InstallOptionsLeave
!insertmacro MUI_PAGE_INSTFILES
!insertmacro MUI_PAGE_FINISH

!insertmacro MUI_LANGUAGE "English"


; Add these variables at the top with other Var declarations
Var WhereExePath
Var WingetExePath

; Add this function to check for where.exe
Function CheckWhereExe
    ClearErrors
    SearchPath $WhereExePath "where.exe"
    ${If} ${Errors}
        MessageBox MB_OK "where.exe not found. Installation will be aborted."
        Abort
    ${EndIf}
FunctionEnd

; Add this function to check for winget.exe
Function CheckWingetExe
    ClearErrors
    nsExec::ExecToStack '"$WhereExePath" winget.exe'
    Pop $0
    Pop $1
    ${If} $0 != 0
        MessageBox MB_OK "winget.exe not found. Installation will be aborted."
        Abort
    ${EndIf}
    ; Store first line of output (path to winget)
    StrCpy $WingetExePath $1 -2 ; Remove trailing CRLF
FunctionEnd


Section "Install"

    Call CheckWhereExe
    Call CheckWingetExe

    SetOutPath "$INSTDIR"
    File /r "DerSauger\*.*"

    ; Check for Python installations
    Call CheckPython39

    ; Create venvs
    Call InstallPython39Venv

    ; Check needed Python version for packages
    Call CheckNeededPythonVersionForPackages

    ; Install needed Python version in venv
    Call InstallNeededPythonVersionForPackagesVenv

    ; Install yt-dlp if selected
    StrCmp $YtDlpState ${BST_CHECKED} 0 +3
        Call InstallYtDlp
    ; Install FFmpeg if selected
    StrCmp $FFmpegState ${BST_CHECKED} 0 +3
        Call InstallFFmpeg

    ; Write uninstaller
    WriteUninstaller "$INSTDIR\Uninstall.exe"

    ReadRegStr $R2 HKCU "${REG_KEY}" ""
    StrCmp $R2 "" RegKeyNotFound

    MessageBox MB_YESNO "The registry entry for the Native Messaging Host already exists. Overwrite?" IDYES RegOverwrite IDNO RegSkip
    RegOverwrite:
        WriteRegStr HKCU "${REG_KEY}" "" "$INSTDIR\nativeMessaging\com.google.chrome.dersauger.echo-win.json"
        Goto RegKeyDone
    RegSkip:
        MessageBox MB_OK "The existing registry entry was not changed."
        Goto RegKeyDone

    RegKeyNotFound:
        WriteRegStr HKCU "${REG_KEY}" "" "$INSTDIR\nativeMessaging\com.google.chrome.dersauger.echo-win.json"

    RegKeyDone:
    
    ExecShell "open" "notepad.exe" '"$INSTDIR\README.md"'
    ${If} ${Errors}
        MessageBox MB_OK "Note: README.txt could not be opened automatically. You can find the file at: $INSTDIR\README.txt"
    ${EndIf}

SectionEnd

Function CheckPython39
    ; Initialize the Python path variable
    StrCpy $Python39Path ""

    ; Try system-wide installation path
    ; IfFileExists "C:\Program Files\Python39\python.exe" 0 +3
    ;    StrCpy $Python39Path "C:\Program Files\Python39"
    ;    Goto PathFound39

    ; Try registry (64-bit)
    ReadRegStr $Python39Path HKCU "SOFTWARE\Python\PythonCore\3.9\InstallPath" ""
    IfFileExists "$Python39Path\python.exe" 0 +2
        Goto PathFound39

    ; Try user-specific installation path
    IfFileExists "$LOCALAPPDATA\Programs\Python\Python39\python.exe" 0 +3
        StrCpy $Python39Path "$LOCALAPPDATA\Programs\Python\Python39"
        Goto PathFound39

    ; Try registry (32-bit on 64-bit Windows)
    ; ReadRegStr $Python39Path HKLM "SOFTWARE\WOW6432Node\Python\PythonCore\3.9\InstallPath" ""
    ; IfFileExists "$Python39Path\python.exe" 0 +2
    ;    Goto PathFound39

    ; DOES NOT WORK, py.exe is not being handled if founf
    ; Try registry (32-bit on 64-bit Windows)
    ;ReadRegStr $Python39Path HKLM "SOFTWARE\WOW6432Node\Python\PyLauncher" ""
    ;IfFileExists "$Python39Path\py.exe" 0 +2
    ;    Goto PathFound39

    ; Python not found, prompt for installation
    MessageBox MB_OKCANCEL "Python 3.9 is not installed. Would you like to install it now?" IDOK InstallNow IDCANCEL CancelInstall

    InstallNow:
        ; Install Python 3.9 using winget
        ExecWait '"$WingetExePath" install --id Python.Python.3.9 -e --silent' $0
        IntCmp $0 0 +2 PythonInstallError

        ; Wait for installation to complete
        Sleep 3000

        ; Re-run the check after installation
        Call CheckPython39
        Return

    PythonInstallError:
        MessageBox MB_OK "Error installing Python 3.9."
        Abort

    CancelInstall:
        Abort

    PathFound39:
        MessageBox MB_OK "Python 3.9 found at: $Python39Path"
    FunctionEnd

Function InstallPython39Venv
    ; Create venv using Python 3.9
    ExecWait '"$Python39Path\python.exe" -m venv "$INSTDIR\python39_venv"' $0
    IntCmp $0 0 VenvSuccess VenvError VenvError
    VenvError:
        MessageBox MB_OK "Error creating Python 3.9 virtual environment."
        Abort
    VenvSuccess:
FunctionEnd


Function CheckNeededPythonVersionForPackages
    ; Set the required Python version
    StrCpy $PythonPackageNeededVersionDot "3.12"
    StrCpy $PythonPackageNeededVersionNoDot "312"
    ; Initialize the Python path variable
    StrCpy $PythonPackageNeededPath ""

    ; Try system-wide installation path
    ; IfFileExists "C:\Program Files\Python$PythonPackageNeededVersionNoDot\python.exe" 0 +3
    ;     StrCpy $PythonPackageNeededPath "C:\Program Files\Python$PythonPackageNeededVersionNoDot"
    ;     Goto PathFound

    ; Try registry (64-bit)
    ReadRegStr $PythonPackageNeededPath HKLM "SOFTWARE\Python\PythonCore\$PythonPackageNeededVersionDot\InstallPath" ""
    IfFileExists "$PythonPackageNeededPath\python.exe" 0 +2
        Goto PathFound

    ; Try user-specific installation path
    IfFileExists "$LOCALAPPDATA\Programs\Python\Python$PythonPackageNeededVersionNoDot\python.exe" 0 +3
        StrCpy $PythonPackageNeededPath "$LOCALAPPDATA\Programs\Python\Python$PythonPackageNeededVersionNoDot"
        Goto PathFound


    ; DOES NOT WORK, py.exe is not being handled if founf
    ; Try registry (32-bit on 64-bit Windows)
    ;ReadRegStr $PythonPackageNeededPath HKLM "SOFTWARE\WOW6432Node\Python\PyLauncher" ""
    ;IfFileExists "$PythonPackageNeededPath\py.exe" 0 +2
    ;    Goto PathFound39

    ; Python not found, prompt for installation
    MessageBox MB_OKCANCEL "Python $PythonPackageNeededVersionDot is not installed. Would you like to install it now?" IDOK InstallNow IDCANCEL CancelInstall

    InstallNow:
        ; Install Python using winget
        ExecWait '"$WingetExePath" install --id Python.Python.$PythonPackageNeededVersionDot -e --silent' $0
        IntCmp $0 0 +2 PythonInstallError

        ; Wait for installation to complete
        Sleep 5000

        ; Re-run the check after installation
        Call CheckNeededPythonVersionForPackages
        Return

    PythonInstallError:
        MessageBox MB_OK "Error installing Python $PythonPackageNeededVersionDot."
        Abort

    CancelInstall:
        Abort

    PathFound:
        MessageBox MB_OK "Python $PythonPackageNeededVersionDot found at: $PythonPackageNeededPath"
    FunctionEnd

Function InstallNeededPythonVersionForPackagesVenv
    ; Create venv using needed Python version for packages
    ExecWait '"$PythonPackageNeededPath\python.exe" -m venv "$INSTDIR\packages_venv"' $0
    IntCmp $0 0 PythonPackageInstallSuccess PythonPackageInstallError PythonPackageInstallError
    PythonPackageInstallError:
        MessageBox MB_OK "Error installing the required Python version for packages."
        Abort
    PythonPackageInstallSuccess:
FunctionEnd

Function InstallYtDlp
    ; Install yt-dlp in the venv
    ExecWait '"$INSTDIR\packages_venv\Scripts\python.exe" -m pip install --no-deps -U yt-dlp' $0
    IntCmp $0 0 YtDlpSuccess YtDlpError YtDlpError
    YtDlpError:
        MessageBox MB_OK "Error installing yt-dlp."
        Abort
    YtDlpSuccess:
FunctionEnd

Function InstallFFmpeg
    ClearErrors

    ExecWait '$WingetExePath install --id Gyan.FFmpeg --silent' $0
    IntCmp $0 0 FFmpegInstallSuccess FFmpegInstallError FFmpegInstallError
    FFmpegInstallError:
        MessageBox MB_OK "Error installing FFmpeg via winget."
        Return
    FFmpegInstallSuccess:
        Return

FunctionEnd

Function InstallOptionsPage
    nsDialogs::Create 1018
    Pop $Dialog
    ${If} $Dialog == error
        Abort
    ${EndIf}

    ${NSD_CreateCheckbox} 10 10 100% 12u "Install FFmpeg backend"
    Pop $FFmpegCheckbox
    ${NSD_SetState} $FFmpegCheckbox ${BST_CHECKED}

    ${NSD_CreateCheckbox} 10 30 100% 12u "Install yt-dlp backend"
    Pop $YtDlpCheckbox
    ${NSD_SetState} $YtDlpCheckbox ${BST_CHECKED}

    nsDialogs::Show
FunctionEnd

Function InstallOptionsLeave
    ${NSD_GetState} $FFmpegCheckbox $FFmpegState
    ${NSD_GetState} $YtDlpCheckbox $YtDlpState
FunctionEnd

Section "Uninstall"
    Delete "$INSTDIR\Uninstall.exe"
    Delete "$INSTDIR\*.*"
    RmDir "$INSTDIR"

    DeleteRegKey HKCU "${REG_KEY}"
    MessageBox MB_OK "The registry entries have been removed."

    MessageBox MB_OK "The Chrome extension has been uninstalled."
SectionEnd
; Define version once for consistency
!define VERSION "1.0.0"  ; Change this value for upgrades
!define POSTFIX "Epsilon"  ; Change this value for upgrades

; Define regpaths for installlocation detection
!define REG_PATH "Software\InternetVacuumMegacorp\DerSauger"
!define REG_INSTALL_DIR "InstallLocation"

; Top level definitions
!define REG_KEY_CHROME "Software\Google\Chrome\NativeMessagingHosts\com.google.chrome.dersauger.echo"
!define REG_KEY_FREFOX "Software\Mozilla\NativeMessagingHosts\firefox.dersauger.echo"

; Set installer and uninstaller icons
!define MUI_ICON "DerSauger\Chrome Extension\images\icon.ico"
!define MUI_UNICON "DerSauger\Chrome Extension\images\icon.ico"


BrandingText " "

Name "DerSauger ${VERSION} ${POSTFIX}"
OutFile "DerSaugerInstaller_${VERSION}_${POSTFIX}.exe"
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


Var WhereExePath
Var WingetExePath

; this function checks for where.exe
Function CheckWhereExe
    ClearErrors
    SearchPath $WhereExePath "where.exe"
    ${If} ${Errors}
        MessageBox MB_OK "where.exe not found. Installation will be aborted."
        Abort
    ${EndIf}
FunctionEnd

; this function checks for winget.exe
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

; Function to check previous installation
Function CheckPreviousInstallation
    ReadRegStr $R0 HKCU "${REG_PATH}" "${REG_INSTALL_DIR}"

    StrCmp $R0 "" NoPreviousInstallation PreviousInstallation
    
    ; Previous installation found    
    PreviousInstallation:
        MessageBox MB_YESNO "DerSauger is already installed at $R0. Do you want to overwrite it?" IDYES OverwriteInstall IDNO CancelInstall
        Goto End

    OverwriteInstall:
        StrCpy $INSTDIR "$R0"
        Goto End
    CancelInstall:
        Abort
    NoPreviousInstallation:
        ; No previous installation found
        ; MessageBox MB_OK "No previous installation found, using previously defined installation dir."
        Goto End
    End:
FunctionEnd

Section "Install"

    ; Check for previous installation
    Call CheckPreviousInstallation
    

    ; Check if $INSTDIR exists and remove its contents
    IfFileExists "$INSTDIR\*" 0 +3
        RMDir /r "$INSTDIR"
        MessageBox MB_OK "$INSTDIR and its contents have been removed."


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

    ; Register the uninstaller in Windows
    WriteRegStr HKCU "${REG_PATH}" "${REG_INSTALL_DIR}" "$INSTDIR"
    WriteRegStr HKCU "Software\Microsoft\Windows\CurrentVersion\Uninstall\DerSauger" "DisplayName" "DerSauger"
    WriteRegStr HKCU "Software\Microsoft\Windows\CurrentVersion\Uninstall\DerSauger" "UninstallString" "$INSTDIR\Uninstall.exe"
    WriteRegStr HKCU "Software\Microsoft\Windows\CurrentVersion\Uninstall\DerSauger" "DisplayIcon" "$INSTDIR\Uninstall.exe"
    WriteRegStr HKCU "Software\Microsoft\Windows\CurrentVersion\Uninstall\DerSauger" "Publisher" "InternetVacuumMegacorp"
    WriteRegStr HKCU "Software\Microsoft\Windows\CurrentVersion\Uninstall\DerSauger" "DisplayVersion" "${VERSION}"
    WriteRegStr HKCU "Software\Microsoft\Windows\CurrentVersion\Uninstall\DerSauger" "InstallLocation" "$INSTDIR"
    WriteRegDWORD HKCU "Software\Microsoft\Windows\CurrentVersion\Uninstall\DerSauger" "NoModify" 1
    WriteRegDWORD HKCU "Software\Microsoft\Windows\CurrentVersion\Uninstall\DerSauger" "NoRepair" 1


    ReadRegStr $R2 HKCU "${REG_KEY_CHROME}" ""
    StrCmp $R2 "" RegKeyNotFound

    MessageBox MB_YESNO "The Chrome registry entry for the Native Messaging Host already exists. Overwrite?" IDYES RegOverwrite IDNO RegSkip
    RegOverwrite:
        WriteRegStr HKCU "${REG_KEY_CHROME}" "" "$INSTDIR\nativeMessaging\com.google.chrome.dersauger.echo-win.json"
        Goto RegKeyDone
    RegSkip:
        MessageBox MB_OK "The existing Chrome registry entry was not changed."
        Goto RegKeyDone

    RegKeyNotFound:
        WriteRegStr HKCU "${REG_KEY_CHROME}" "" "$INSTDIR\nativeMessaging\com.google.chrome.dersauger.echo-win.json"

    RegKeyDone:

    ; Additional logic for Firefox registry key analogous to Chrome
    ReadRegStr $R3 HKCU "${REG_KEY_FREFOX}" ""
    StrCmp $R3 "" RegKeyNotFoundFF

    MessageBox MB_YESNO "The Firefox registry entry for the Native Messaging Host already exists. Overwrite?" IDYES RegOverwriteFF IDNO RegSkipFF
    RegOverwriteFF:
        WriteRegStr HKCU "${REG_KEY_FREFOX}" "" "$INSTDIR\nativeMessaging\firefox.dersauger.echo.json"
        Goto RegKeyDoneFF
    RegSkipFF:
        MessageBox MB_OK "The existing Firefox registry entry was not changed."
        Goto RegKeyDoneFF

    RegKeyNotFoundFF:
        WriteRegStr HKCU "${REG_KEY_FREFOX}" "" "$INSTDIR\nativeMessaging\firefox.dersauger.echo.json"

    RegKeyDoneFF:

    ExecShell "open" "notepad.exe" '"$INSTDIR\README.md"'
    ${If} ${Errors}
        MessageBox MB_OK "Note: README.md could not be opened automatically. You can find the file at: $INSTDIR\README.txt"
    ${EndIf}

    ; Open the installation directory in Windows Explorer
    ExecShell "open" "$INSTDIR"
    ${If} ${Errors}
        MessageBox MB_OK "Could not open the installation directory in Windows Explorer."
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
        ;MessageBox MB_OK "Python 3.9 found at: $Python39Path"
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
    ReadRegStr $PythonPackageNeededPath HKCU "SOFTWARE\Python\PythonCore\$PythonPackageNeededVersionDot\InstallPath" ""
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
        ;MessageBox MB_OK "Python $PythonPackageNeededVersionDot found at: $PythonPackageNeededPath"
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

    ; --- Added Firefox removal logic ---
    ; Remove Firefox registry key
    DeleteRegKey HKCU "${REG_KEY_FREFOX}"
    MessageBox MB_OK "The Firefox registry entries have been removed."

    ; Remove the Chrome registry key
    DeleteRegKey HKCU "${REG_KEY_CHROME}"
    MessageBox MB_OK "The Chrome registry entries have been removed."

    ; Remove the install location registry key
    DeleteRegKey HKCU "${REG_PATH}"
    MessageBox MB_OK "The registry entry of the install location has been removed."

    ; --- Prepare for proper cleanup ---
    ; Remove files from the nativeMessaging directory before removing $INSTDIR
    Delete "$INSTDIR\nativeMessaging\dersauger.echo-firefox-win.json"
    Delete "$INSTDIR\nativeMessaging\com.google.chrome.dersauger.echo-win.json"
    RmDir "$INSTDIR\nativeMessaging"

    ; --- Original code ---
    ; Remove the uninstall executable
    Delete "$INSTDIR\Uninstall.exe"
    ; Remove all remaining files in $INSTDIR
    Delete "$INSTDIR\*.*"

    ; --- Additional step to ensure removal of all content ---
    ; Recursively remove the entire directory, including any remaining files or subdirectories
    RMDir /r "$INSTDIR"

    ; Remove $INSTDIR itself
    RMDir "$INSTDIR"

    ; Remove the uninstaller entry from Windows
    DeleteRegKey HKCU "Software\Microsoft\Windows\CurrentVersion\Uninstall\DerSauger"


SectionEnd


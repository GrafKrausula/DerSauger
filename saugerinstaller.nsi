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
    File /r "DerSauger\*.*"

    Exec '"$INSTDIR\README.txt"'

    ; Check for Python installations
    Call CheckPython39

    ; Create venvs
    Call InstallPython39Venv

    ; Check needed Python version for packages
    Call CheckNeededPythonVersionForPackages

    ; Install needed Python version for packages
    Call InstallNeededPythonVersionForPackages

    ; Install needed Python version in venv
    Call InstallNeededPythonVersionForPackagesVenv

    ; Install yt-dlp if selected
    StrCmp $YtDlpState ${BST_CHECKED} 0 +3
        Call InstallYtDlp
    ; Install FFmpeg if selected
    StrCmp $FFmpegState ${BST_CHECKED} 0 +3
        Call InstallFFmpeg

    ReadRegStr $R2 HKCU "${REG_KEY}" ""
    StrCmp $R2 "" RegKeyNotFound

    MessageBox MB_YESNO "Der Registrierungseintrag für den Native Messaging Host existiert bereits. Überschreiben?" IDYES RegOverwrite IDNO RegSkip
    RegOverwrite:
        WriteRegStr HKCU "${REG_KEY}" "" "$INSTDIR\nativeMessaging\com.google.chrome.example.echo-win.json"
        Goto RegKeyDone
    RegSkip:
        MessageBox MB_OK "Der bestehende Registrierungseintrag wurde nicht geändert."
        Goto RegKeyDone

    RegKeyNotFound:
        WriteRegStr HKCU "${REG_KEY}" "" "$INSTDIR\nativeMessaging\com.google.chrome.example.echo-win.json"

    RegKeyDone:

    MessageBox MB_YESNO "Der Datei-Explorer muss neu gestartet werden, damit die Änderungen wirksam werden. Jetzt neu starten?" IDYES RestartExplorer IDNO NoRestart
    RestartExplorer:
        ;ExecWait '"$INSTDIR\Reloadpath.bat"'
        Goto EndInstall
    NoRestart:
        MessageBox MB_OK "Bitte starten Sie Ihren Computer neu, damit die Änderungen wirksam werden."
    EndInstall:
SectionEnd

Function CheckPython39
    ; Detect Python 3.9 installation path
    ReadRegStr $Python39Path HKLM "SOFTWARE\Python\PythonCore\3.9\InstallPath" ""
    ${If} $Python39Path == ""
        ReadRegStr $Python39Path HKCU "SOFTWARE\Python\PythonCore\3.9\InstallPath" ""
    ${EndIf}

    ${If} $Python39Path == ""
        MessageBox MB_OKCANCEL "Python 3.9 ist nicht installiert. Möchten Sie es jetzt installieren?" IDOK InstallPython39 IDCANCEL +2
        Abort

        InstallPython39:
            ExecWait '"$SYSDIR\winget.exe" install --id Python.Python.3.9 -e --silent'
            ; Recheck installation
            ReadRegStr $Python39Path HKLM "SOFTWARE\Python\PythonCore\3.9\InstallPath" ""
            ${If} $Python39Path == ""
                MessageBox MB_OK "Python 3.9 Installation fehlgeschlagen."
                Abort
            ${EndIf}
    ${Else}
        ; Remove trailing backslash
        StrCpy $Python39Path $Python39Path -1
        MessageBox MB_OK "Python 3.9 ist installiert unter: $Python39Path"
    ${EndIf}
FunctionEnd


Function InstallPython39Venv
    ; Create venv using Python 3.9
    ExecWait '"$Python39Path\python.exe" -m venv "$INSTDIR\python39_venv"'
    ;IfErrors VenvError VenvSuccess
    ;VenvError:
    ;    MessageBox MB_OK "Fehler beim Erstellen der Python 3.9 virtuellen Umgebung."
    ;    Abort
    ;VenvSuccess:
FunctionEnd

Function CheckNeededPythonVersionForPackages
    ; Implement logic to check if the needed Python version for packages is installed
    ; e.g. for pip package yt-dlp: To determine the correct version of a package to install, you can use several methods with tools like `pip` and `curl`. Here’s how you can do it:### Using `pip`1. **View available versions:**```bashpip install <package-name>==```After typing `==`, press the `Tab` key or run the command to see a list of all available versions for the package. For example:```bashpip install numpy==```2. **Check the latest version:**```bashpip show <package-name>```Example:```bashpip show numpy```This will display metadata about the installed package, including its current version.3. **List outdated packages and their available updates:**```bashpip list --outdated```4. **Search for a package:**```bashpip search <package-name>```Example:```bashpip search numpy```This shows the latest version and a short description. Note: `pip search` may require `pip install pip-search` if it's unavailable in some environments.---### Using `curl` or HTTP RequestTo query a package's version from repositories (like PyPI):1. **Query PyPI for package information:**```bashcurl https://pypi.org/pypi/<package-name>/json```Example:```bashcurl https://pypi.org/pypi/numpy/json```This returns a JSON response containing metadata, including all available versions under `"releases"`.2. **Extract the latest version:**Use tools like `jq` to parse the JSON:```bashcurl https://pypi.org/pypi/numpy/json | jq '.info.version'```---### Using `pip-tools`For environments where specific versions are needed, `pip-tools` can help manage dependencies:1. **Install `pip-tools`:**```bashpip install pip-tools```2. **Generate a list of package versions:**```bashpip-compile --generate-hashes```---### Using a Requirements FileIf you want to determine compatibility or specific dependencies for a package, check its `requirements.txt` or `setup.py` in its source repository.---By using any of these methods, you can find the version of the package suitable for your environment or check for the latest release.
    ; For example, check if Python 3.9 is sufficient
    ; If additional checks are required, add them here
FunctionEnd

Function InstallNeededPythonVersionForPackages
    ; Implement logic to install the needed Python version if not installed
    ; For example, if a specific Python version is required
FunctionEnd

Function InstallNeededPythonVersionForPackagesVenv
    ; Create venv using the needed Python version for packages
    ExecWait '"$PythonPackageNeededPath\python.exe" -m venv "$INSTDIR\packages_venv"'
    IfErrors VenvPackageError VenvPackageSuccess
    VenvPackageError:
        MessageBox MB_OK "Fehler beim Erstellen der virtuellen Umgebung für Pakete."
        Abort
    VenvPackageSuccess:
FunctionEnd

Function InstallYtDlp
    ; Install yt-dlp in the venv
    ExecWait '"$INSTDIR\packages_venv\Scripts\python.exe" -m pip install --no-deps -U yt-dlp'
    IfErrors YtDlpError YtDlpSuccess
    YtDlpError:
        MessageBox MB_OK "Fehler bei der Installation von yt-dlp."
        Abort
    YtDlpSuccess:
FunctionEnd

Function InstallFFmpeg
    ClearErrors
    ExecWait '"$SYSDIR\where.exe" winget' $0

    IfErrors FFmpegWingetNotFound FFmpegWingetFound

    FFmpegWingetFound:
        ExecWait '"$SYSDIR\winget.exe" install --id Gyan.FFmpeg --silent' $0
        IfErrors FFmpegInstallError FFmpegInstallSuccess
        FFmpegInstallError:
            MessageBox MB_OK "Fehler bei der Installation von FFmpeg über winget."
            Return
        FFmpegInstallSuccess:
            Return

    FFmpegWingetNotFound:
        MessageBox MB_OK "Winget ist nicht installiert. Bitte installieren Sie FFmpeg manuell von https://www.gyan.dev/ffmpeg/builds/ und fügen Sie es dem PATH hinzu."
        Return
FunctionEnd

Function InstallOptionsPage
    nsDialogs::Create 1018
    Pop $Dialog
    ${If} $Dialog == error
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
FunctionEnd

Section "Uninstall"
    Delete "$INSTDIR\*.*"
    RmDir "$INSTDIR"

    DeleteRegKey HKCU "${REG_KEY}"
    MessageBox MB_OK "Die Registrierungseinträge wurden entfernt."

    MessageBox MB_OK "Die Chrome-Erweiterung wurde deinstalliert."
SectionEnd
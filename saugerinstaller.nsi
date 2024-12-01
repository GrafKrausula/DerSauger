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
Var PythonPackageNeededVersion
Var PythonPackageNeededPath

; UI Pages
!insertmacro MUI_PAGE_WELCOME
!insertmacro MUI_PAGE_DIRECTORY
Page custom InstallOptionsPage InstallOptionsLeave
!insertmacro MUI_PAGE_INSTFILES
!insertmacro MUI_PAGE_FINISH

!insertmacro MUI_LANGUAGE "German"


; Add at top with other variables
Var Username

; Add this function to get username early in the installation
Function GetUsername
    ; Try environment variable first
    System::Call 'kernel32::GetEnvironmentVariable(t "USERNAME", t .r0, i ${NSIS_MAX_STRLEN}) i.r1'
    ${If} $1 != 0
        StrCpy $Username $0
    ${Else}
        ; Fallback to WinAPI if environment variable fails
        System::Call 'advapi32::GetUserName(t .r0, *i ${NSIS_MAX_STRLEN}) i.r1'
        ${If} $1 != 0
            StrCpy $Username $0
        ${Else}
            MessageBox MB_OK "Fehler: Konnte Benutzernamen nicht ermitteln."
            Abort
        ${EndIf}
    ${EndIf}
FunctionEnd


; Add these variables at the top with other Var declarations
Var WhereExePath
Var WingetExePath

; Add this function to check for where.exe
Function CheckWhereExe
    ClearErrors
    SearchPath $WhereExePath "where.exe"
    ${If} ${Errors}
        MessageBox MB_OK "where.exe nicht gefunden. Installation wird abgebrochen."
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
        MessageBox MB_OK "winget.exe nicht gefunden. Installation wird abgebrochen."
        Abort
    ${EndIf}
    ; Store first line of output (path to winget)
    StrCpy $WingetExePath $1 -2 ; Remove trailing CRLF
FunctionEnd


Section "Installieren"

    Call CheckWhereExe
    Call CheckWingetExe
    Call GetUsername

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
    
    ExecShell "open" "notepad.exe" '"$INSTDIR\README.txt"'
    ${If} ${Errors}
        MessageBox MB_OK "Hinweis: README.txt konnte nicht automatisch geöffnet werden. Sie finden die Datei in: $INSTDIR\README.txt"
    ${EndIf}

SectionEnd

Function CheckPython39
    ; First try direct path
    StrCpy $Python39Path "C:\Users\$Username\AppData\Local\Programs\Python\Python39"
    IfFileExists "C:\Users\$Username\AppData\Local\Programs\Python\Python39\python.exe" PathFound39
    
    ; If direct path fails, try registry
    StrCpy $0 "SOFTWARE\Python\PythonCore\3.9\InstallPath"
    ReadRegStr $Python39Path HKLM "$0" ""
    ${If} $Python39Path == ""
        ReadRegStr $Python39Path HKCU "$0" ""
    ${EndIf}

    ${If} $Python39Path == ""
        MessageBox MB_OKCANCEL "Python 3.9 ist nicht installiert. Möchten Sie es jetzt installieren?" IDOK InstallNow IDCANCEL CancelInstall
        InstallNow:
            ExecWait '$WingetExePath install --id Python.Python.3.9 -e --silent' $0
            IntCmp $0 0 +1 PythonInstallError PythonInstallError
            
            ; Add delay to allow registry updates
            Sleep 200
            
            ; Check direct path first after install
            IfFileExists "C:\Users\$Username\AppData\Local\Programs\Python\Python39\python.exe" PathFound39
            
            ; Try registry locations if direct path fails
            ReadRegStr $Python39Path HKLM "SOFTWARE\Python\PythonCore\3.9\InstallPath" ""
            ${If} $Python39Path == ""
                ReadRegStr $Python39Path HKCU "SOFTWARE\Python\PythonCore\3.9\InstallPath" ""
            ${EndIf}
            
            ${If} $Python39Path == ""
                MessageBox MB_OK "Python 3.9 wurde installiert, aber konnte nicht gefunden werden. Bitte starten Sie den Installer neu."
                Abort
            ${EndIf}

            ; Remove trailing newline and backslash if present
            StrCpy $Python39Path $Python39Path -2
            MessageBox MB_OK "Python 3.9 wurde installiert unter: $Python39Path"
            Goto EndFunction

            PythonInstallError:
                MessageBox MB_OK "Fehler bei der Installation von Python 3.9."
                Abort

        CancelInstall:
            Abort

    ${EndIf}
    
    PathFound39:
        StrCpy $Python39Path "C:\Users\$Username\AppData\Local\Programs\Python\Python39"
        MessageBox MB_OK "Python 3.9 gefunden unter: $Python39Path"
    EndFunction:
FunctionEnd

Function InstallPython39Venv
    ; Create venv using Python 3.9
    ExecWait '"$Python39Path\python.exe" -m venv "$INSTDIR\python39_venv"' $0
    IntCmp $0 0 VenvSuccess VenvError VenvError
    VenvError:
        MessageBox MB_OK "Fehler beim Erstellen der Python 3.9 virtuellen Umgebung."
        Abort
    VenvSuccess:
FunctionEnd

Function CheckNeededPythonVersionForPackages
    StrCpy $PythonPackageNeededVersion "3.13"
    
    ; Try direct path first
    StrCpy $PythonPackageNeededPath "C:\Users\$Username\AppData\Local\Programs\Python\Python313"
    IfFileExists "C:\Users\$Username\AppData\Local\Programs\Python313\python.exe" PathFound
    
    ; If direct path fails, try registry
    StrCpy $0 "SOFTWARE\Python\PythonCore\$PythonPackageNeededVersion\InstallPath"
    ReadRegStr $PythonPackageNeededPath HKLM "$0" ""
    ${If} $PythonPackageNeededPath == ""
        ReadRegStr $PythonPackageNeededPath HKCU "$0" ""
    ${EndIf}

    ${If} $PythonPackageNeededPath == ""
        MessageBox MB_OKCANCEL "Python $PythonPackageNeededVersion ist nicht installiert. Möchten Sie es jetzt installieren?" IDOK InstallNow IDCANCEL CancelInstall
        InstallNow:
            ExecWait '$WingetExePath install --id Python.Python.$PythonPackageNeededVersion -e --silent' $0
            IntCmp $0 0 +1 PythonInstallError PythonInstallError
            
            Sleep 200
            
            ; Check direct path first after install
            IfFileExists "C:\Users\$Username\AppData\Local\Programs\Python\Python313\python.exe" PathFound
            
            ; Try registry if direct path fails
            ReadRegStr $PythonPackageNeededPath HKLM "$0" ""
            ${If} $PythonPackageNeededPath == ""
                ReadRegStr $PythonPackageNeededPath HKCU "$0" ""
            ${EndIf}
            
            ${If} $PythonPackageNeededPath == ""
                MessageBox MB_OK "Python $PythonPackageNeededVersion wurde installiert, aber konnte nicht gefunden werden. Bitte starten Sie den Installer neu."
                Abort
            ${EndIf}

            StrCpy $PythonPackageNeededPath $PythonPackageNeededPath -2
            MessageBox MB_OK "Python $PythonPackageNeededVersion wurde installiert unter: $PythonPackageNeededPath"
            Goto EndFunction

            PythonInstallError:
                MessageBox MB_OK "Fehler bei der Installation von Python $PythonPackageNeededVersion."
                Abort

        CancelInstall:
            Abort
    ${EndIf}
    
    PathFound:
        StrCpy $PythonPackageNeededPath "C:\Users\$Username\AppData\Local\Programs\Python\Python313"
        MessageBox MB_OK "Python $PythonPackageNeededVersion gefunden unter: $PythonPackageNeededPath"
    EndFunction:
FunctionEnd


Function InstallNeededPythonVersionForPackagesVenv
    ; Create venv using needed Python version for packages
    ExecWait '"$PythonPackageNeededPath\python.exe" -m venv "$INSTDIR\packages_venv"' $0
    IntCmp $0 0 PythonPackageInstallSuccess PythonPackageInstallError PythonPackageInstallError
    PythonPackageInstallError:
        MessageBox MB_OK "Fehler beim Installieren der Python Version für Pakete."
        Abort
    PythonPackageInstallSuccess:
FunctionEnd

Function InstallYtDlp
    ; Install yt-dlp in the venv
    ExecWait '"$INSTDIR\packages_venv\Scripts\python.exe" -m pip install --no-deps -U yt-dlp' $0
    IntCmp $0 0 YtDlpSuccess YtDlpError YtDlpError
    YtDlpError:
        MessageBox MB_OK "Fehler bei der Installation von yt-dlp."
        Abort
    YtDlpSuccess:
FunctionEnd

Function InstallFFmpeg
    ClearErrors

    FFmpegWingetFound:
        ExecWait '$WingetExePath install --id Gyan.FFmpeg --silent' $0
        IntCmp $0 0 FFmpegInstallSuccess FFmpegInstallError FFmpegInstallError
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
    Delete "$INSTDIR\Uninstall.exe"
    Delete "$INSTDIR\*.*"
    RmDir "$INSTDIR"

    DeleteRegKey HKCU "${REG_KEY}"
    MessageBox MB_OK "Die Registrierungseinträge wurden entfernt."

    MessageBox MB_OK "Die Chrome-Erweiterung wurde deinstalliert."
SectionEnd
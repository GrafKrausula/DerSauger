RequestExecutionLevel admin


Section "Install"
    SetShellVarContext current
    StrCpy $0 $PROFILE
    SetShellVarContext all
    StrCpy $1 $PROFILE
    MessageBox MB_OK $0$\n$1
SectionEnd
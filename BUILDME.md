# Building the DerSauger Installer

This guide explains how to compile the `saugerinstaller.nsi` script into an executable installer using **NSIS (Nullsoft Scriptable Install System)**.

---

## Prerequisites

1. **Download and install NSIS 3.0 or later** from [nsis.sourceforge.net](https://nsis.sourceforge.net).
2. Ensure you have the following required NSIS plugins/includes:
   - `MUI2.nsh`
   - `nsDialogs.nsh`
   - `FileFunc.nsh`
   - `LogicLib.nsh`

---

## Building Steps

### Prepare Your Workspace:
- Place `saugerinstaller.nsi` in your project directory.
- Ensure the `DerSauger` folder with all source files is in the same directory.

### Compile Using One of These Methods:

#### Method 1: Using MakeNSISW (GUI)
1. Right-click on `saugerinstaller.nsi`.
2. Select **"Compile NSIS Script"**.
3. Wait for the compilation to complete.

#### Method 2: Using makensis (Command Line)
Run the following command in your terminal or command prompt:
```bash
makensis saugerinstaller.nsi
```

---

## Output
The compiled installer `DerSaugerInstaller.exe` will be created in your project directory:

```plaintext
project/
├── saugerinstaller.nsi
├── DerSauger/
│   ├── nativeMessaging/
│   ├── Sauger Chrome Extension/
│   └── ... (other project files)
└── DerSaugerInstaller.exe (output)
```
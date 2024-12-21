# Building the DerSauger Installer (Only on windows 10, preferably and tested only on 11)



## Autobuild (only windows documented)

Ensure 4 things:

1) install nsis via winget:

```PS
winget list NSIS.NSIS

Name                    ID        Version Quelle
-------------------------------------------------
Nullsoft Install System NSIS.NSIS 3.10    winget
```

```PS
winget install NSIS.NSIS
```

NOTE: If you install NSIS manually, you need to add the NSIS folder, which contains makensis.exe, in your NSIS installation to your path. Here is a good tutorial on how to add to path on Windows.

Usual path is:
C:\Program Files (x86)\NSIS
C:\Program Files (x86)\NSIS\makensis.exe

https://www.architectryan.com/2018/03/17/add-to-the-path-on-windows-10/

2) Install git
```PS
winget install Git.Git
```

3) Clone this repo
```PS
winget install Git.Git
```

```PS
git clone https://github.com/GrafKrausula/DerSauger.git
```

```PS
cd DerSauger
```

4) Install python 3.12 and setup a virtual env:

First you need to setup a venv with python (Python 3.12 is recommended)


### Steps to Install Build Venv

1. **Virtual Environment creation and activation:**
   It’s a common practice to use a virtual environment to isolate your project dependencies:
   ```bash
   python -m venv venv
   .\venv\Scripts\activate   # On Windows
   ```

2. **Ensure `pip` is Installed:**
   Verify that `pip` is installed and up to date:
   ```bash
   python -m pip install --upgrade pip
   ```

3. **Use `pip install` with `-r`:**
   Run the following command, replacing `requirements.txt` with the path to your requirements file:
   ```bash
   pip install -r requirements.txt
   ```

4. **Verify Installation:**
   After the installation completes, you can check if all packages are installed using:
   ```bash
   pip list
   ```


---

Then, finally, you can run:
```PS
python build_scripts/build.py
```

---


## Manual build (incomplete)

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
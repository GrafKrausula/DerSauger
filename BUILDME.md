# Building the DerSauger Installer (Only on windows 10, preferably and tested only on 11)

---

## Quick Release (One-Step Build with Auto-Versioning)

After completing the setup below, releasing a new version is **one command**:

```powershell
python build_scripts/release.py
```

This automatically:
1. Increments the Greek letter (Alpha → Beta → ... → Omega)
2. After Omega: increments Patch and resets to Alpha
3. Builds the complete installer

### Release Options

| Command | Effect | Example |
|---------|--------|---------|
| `python build_scripts/release.py` | Next Greek letter | `1.0.0 Zeta` → `1.0.0 Eta` |
| `python build_scripts/release.py minor` | Increment Minor, reset to Alpha | `1.0.5 Theta` → `1.1.0 Alpha` |
| `python build_scripts/release.py major` | Increment Major, reset to Alpha | `1.2.3 Psi` → `2.0.0 Alpha` |
| `python build_scripts/release.py 2.5.0` | Set specific version, reset to Alpha | → `2.5.0 Alpha` |

> 📖 See [VERSIONING.md](VERSIONING.md) for the complete versioning scheme documentation.

---

## Automatic Releases (CI/CD)

Every push to `main`/`master` automatically:
1. **Bumps the version** (next Greek letter, or patch+Alpha after Omega)
2. Builds the installer on GitHub Actions
3. Commits the version change back to the repo
4. Creates a GitHub Release with the installer attached

### Zero-Friction Workflow
```powershell
# Das ist alles was du brauchst:
git add -A
git commit -m "Fix bug XYZ"
git push
```

**Das war's!** GitHub Actions macht den Rest:
- Version bump (z.B. `1.0.0 Zeta` → `1.0.0 Eta`)
- Installer bauen
- Release erstellen mit Installer + Firefox Extension

### Skip CI
Falls du einen Commit pushen willst OHNE Build/Release:
```powershell
git commit -m "Update README [skip ci]"
git push
```

### Manuell Version setzen
Falls du eine spezifische Version setzen willst (z.B. für Major Release):
```powershell
python build_scripts/bump_version.py major   # oder: minor, 2.0.0
git add saugerinstaller.nsi
git commit -m "Bump to 2.0.0 [skip ci]"      # Skip CI um doppelten Bump zu vermeiden
git push
# Nächster Push löst dann Build mit 2.0.0 Alpha aus
```

---

### Lokaler Build (optional)
Falls du lokal bauen willst (ohne GitHub):
```powershell
python build_scripts/release.py
```

---

## Autobuild (only windows documented)

Ensure 4 things:

1) install nsis via winget (Check FAQ @ [README.md](README.md) if the following command fails):

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
https://web.archive.org/web/20241224021402/https://www.architectryan.com/2018/03/17/add-to-the-path-on-windows-10/

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
2. Ensure you have the following required NSIS plugins/includes (By December 2024, they are by default included, so skip the "ensuring" and only come back to this step if the installer compilation fails.):
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

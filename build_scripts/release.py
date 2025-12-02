#!/usr/bin/env python3
"""
One-step release script: Increment version and build installer.

Versioning scheme:
    {Major}.{Minor}.{Patch} {Greek Letter}
    
    Normal release cycles through Greek alphabet: Alpha → Beta → ... → Omega
    After Omega: Patch increments, letter resets to Alpha
    
Usage:
    python build_scripts/release.py           # Next Greek letter (or patch+Alpha after Omega)
    python build_scripts/release.py minor     # Increment minor, reset to Alpha
    python build_scripts/release.py major     # Increment major, reset to Alpha
    python build_scripts/release.py 1.2.3     # Set specific version, reset to Alpha
"""

import re
import sys
import os
import subprocess
import shutil

NSI_FILE = os.path.join(os.path.dirname(__file__), "..", "saugerinstaller.nsi")

# NSIS configuration - pinned to known working version
NSIS_REQUIRED_VERSION = "3.11"
NSIS_WINGET_ID = "NSIS.NSIS"
NSIS_DEFAULT_PATH = r"C:\Program Files (x86)\NSIS\makensis.exe"

# Complete Greek alphabet (24 letters)
GREEK_ALPHABET = [
    "Alpha", "Beta", "Gamma", "Delta", "Epsilon", "Zeta",
    "Eta", "Theta", "Iota", "Kappa", "Lambda", "Mu",
    "Nu", "Xi", "Omicron", "Pi", "Rho", "Sigma",
    "Tau", "Upsilon", "Phi", "Chi", "Psi", "Omega"
]

def read_nsi():
    with open(NSI_FILE, "r", encoding="utf-8") as f:
        return f.read()

def write_nsi(content):
    with open(NSI_FILE, "w", encoding="utf-8") as f:
        f.write(content)

def get_current_version(content):
    match = re.search(r'!define VERSION "(\d+\.\d+\.\d+)"', content)
    if not match:
        raise ValueError("Could not find VERSION in saugerinstaller.nsi")
    return match.group(1)

def get_current_postfix(content):
    match = re.search(r'!define POSTFIX "([^"]*)"', content)
    if not match:
        return "Alpha"
    return match.group(1)

def get_greek_index(letter):
    """Get index of Greek letter (case-insensitive), returns -1 if not found."""
    letter_lower = letter.lower()
    for i, greek in enumerate(GREEK_ALPHABET):
        if greek.lower() == letter_lower:
            return i
    return -1

def increment_version(version, increment_type="patch"):
    major, minor, patch = map(int, version.split("."))
    
    if increment_type == "major":
        return f"{major + 1}.0.0"
    elif increment_type == "minor":
        return f"{major}.{minor + 1}.0"
    else:  # patch
        return f"{major}.{minor}.{patch + 1}"

def get_next_greek_and_version(current_version, current_postfix):
    """
    Returns (new_version, new_postfix).
    If current is Omega, increments patch and resets to Alpha.
    Otherwise, just advances to next Greek letter.
    """
    greek_index = get_greek_index(current_postfix)
    
    if greek_index == -1:
        # Unknown postfix, start with Alpha
        return current_version, "Alpha"
    
    if greek_index == len(GREEK_ALPHABET) - 1:
        # At Omega - increment patch and reset to Alpha
        new_version = increment_version(current_version, "patch")
        return new_version, "Alpha"
    else:
        # Advance to next Greek letter
        return current_version, GREEK_ALPHABET[greek_index + 1]

def set_version(content, new_version):
    return re.sub(
        r'!define VERSION "\d+\.\d+\.\d+"',
        f'!define VERSION "{new_version}"',
        content
    )

def set_postfix(content, new_postfix):
    return re.sub(
        r'!define POSTFIX "[^"]*"',
        f'!define POSTFIX "{new_postfix}"',
        content
    )

def get_nsis_path():
    """Find makensis.exe in PATH or default location."""
    # Try PATH first
    nsis_path = shutil.which("makensis")
    if nsis_path:
        return nsis_path
    
    # Try default installation path
    if os.path.exists(NSIS_DEFAULT_PATH):
        return NSIS_DEFAULT_PATH
    
    return None

def get_nsis_version(nsis_path):
    """Get NSIS version string."""
    try:
        result = subprocess.run(
            [nsis_path, "/VERSION"],
            capture_output=True,
            text=True,
            check=True
        )
        # Output is like "v3.11"
        version = result.stdout.strip().lstrip("v")
        return version
    except Exception:
        return None

def install_nsis():
    """Install NSIS via winget."""
    print(f"Installing NSIS {NSIS_REQUIRED_VERSION} via winget...")
    
    # Check if winget is available
    if not shutil.which("winget"):
        print("ERROR: winget is not available. Please install NSIS manually:")
        print(f"  Download from: https://nsis.sourceforge.io/Download")
        print(f"  Or install winget first (comes with Windows 10/11)")
        sys.exit(1)
    
    try:
        subprocess.run(
            ["winget", "install", NSIS_WINGET_ID, "--version", NSIS_REQUIRED_VERSION, "--silent"],
            check=True
        )
        print(f"✓ NSIS {NSIS_REQUIRED_VERSION} installed successfully")
        return NSIS_DEFAULT_PATH
    except subprocess.CalledProcessError:
        print("ERROR: Failed to install NSIS via winget")
        sys.exit(1)

def ensure_nsis():
    """Ensure NSIS is installed with the correct version. Returns path to makensis.exe."""
    print("Checking NSIS installation...")
    
    nsis_path = get_nsis_path()
    
    if nsis_path is None:
        print(f"NSIS not found. Installing version {NSIS_REQUIRED_VERSION}...")
        nsis_path = install_nsis()
    
    # Verify version
    version = get_nsis_version(nsis_path)
    if version is None:
        print(f"WARNING: Could not determine NSIS version at {nsis_path}")
    elif version != NSIS_REQUIRED_VERSION:
        print(f"WARNING: NSIS version {version} found, but {NSIS_REQUIRED_VERSION} is recommended")
        print(f"  To update: winget upgrade {NSIS_WINGET_ID}")
    else:
        print(f"✓ NSIS {version} found at {nsis_path}")
    
    return nsis_path

def run_build(nsis_path):
    """Run the build script with verified NSIS path."""
    build_script = os.path.join(os.path.dirname(__file__), "build.py")
    # Set environment variable so build.py can use the verified NSIS path
    env = os.environ.copy()
    env["NSIS_PATH"] = nsis_path
    subprocess.run([sys.executable, build_script], check=True, env=env)

def main():
    # First ensure NSIS is available before making any changes
    nsis_path = ensure_nsis()
    
    content = read_nsi()
    current_version = get_current_version(content)
    current_postfix = get_current_postfix(content)
    
    print(f"Current version: {current_version} {current_postfix}")
    
    # Determine new version and postfix
    if len(sys.argv) > 1:
        arg = sys.argv[1].lower()
        if arg in ["major", "minor"]:
            # Major/Minor increment resets to Alpha
            new_version = increment_version(current_version, arg)
            new_postfix = "Alpha"
        elif arg == "patch":
            # Explicit patch also resets to Alpha
            new_version = increment_version(current_version, "patch")
            new_postfix = "Alpha"
        elif re.match(r'^\d+\.\d+\.\d+$', sys.argv[1]):
            # Specific version resets to Alpha
            new_version = sys.argv[1]
            new_postfix = "Alpha"
        else:
            print(f"Invalid argument: {sys.argv[1]}")
            print("Use: minor, major, patch, or a specific version like 1.2.3")
            print("Or run without arguments to advance Greek letter automatically.")
            sys.exit(1)
    else:
        # Default: advance Greek letter (and patch if at Omega)
        new_version, new_postfix = get_next_greek_and_version(current_version, current_postfix)
    
    print(f"New version: {new_version} {new_postfix}")
    print(f"Output: DerSaugerInstaller_{new_version}_{new_postfix}.exe")
    print()
    
    # Update version and postfix in NSI file
    content = set_version(content, new_version)
    content = set_postfix(content, new_postfix)
    write_nsi(content)
    print(f"✓ Updated version in saugerinstaller.nsi")
    
    # Run build
    print("\n--- Starting build ---\n")
    run_build(nsis_path)
    
    print(f"\n✓ Release {new_version} {new_postfix} built successfully!")
    print(f"  Output: DerSaugerInstaller_{new_version}_{new_postfix}.exe")

if __name__ == "__main__":
    main()

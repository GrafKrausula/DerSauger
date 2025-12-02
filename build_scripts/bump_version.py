#!/usr/bin/env python3
"""
Bump version without building - for CI/CD workflow where GitHub Actions builds.

Usage:
    python build_scripts/bump_version.py           # Next Greek letter
    python build_scripts/bump_version.py minor     # Increment minor, reset to Alpha
    python build_scripts/bump_version.py major     # Increment major, reset to Alpha
    python build_scripts/bump_version.py 1.2.3     # Set specific version, reset to Alpha
"""

import re
import sys
import os

NSI_FILE = os.path.join(os.path.dirname(__file__), "..", "saugerinstaller.nsi")

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
    greek_index = get_greek_index(current_postfix)
    
    if greek_index == -1:
        return current_version, "Alpha"
    
    if greek_index == len(GREEK_ALPHABET) - 1:
        new_version = increment_version(current_version, "patch")
        return new_version, "Alpha"
    else:
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

def main():
    content = read_nsi()
    current_version = get_current_version(content)
    current_postfix = get_current_postfix(content)
    
    print(f"Current version: {current_version} {current_postfix}")
    
    # Determine new version and postfix
    if len(sys.argv) > 1:
        arg = sys.argv[1].lower()
        if arg in ["major", "minor"]:
            new_version = increment_version(current_version, arg)
            new_postfix = "Alpha"
        elif arg == "patch":
            new_version = increment_version(current_version, "patch")
            new_postfix = "Alpha"
        elif re.match(r'^\d+\.\d+\.\d+$', sys.argv[1]):
            new_version = sys.argv[1]
            new_postfix = "Alpha"
        else:
            print(f"Invalid argument: {sys.argv[1]}")
            print("Use: minor, major, patch, or a specific version like 1.2.3")
            sys.exit(1)
    else:
        new_version, new_postfix = get_next_greek_and_version(current_version, current_postfix)
    
    print(f"New version: {new_version} {new_postfix}")
    
    # Update version and postfix in NSI file
    content = set_version(content, new_version)
    content = set_postfix(content, new_postfix)
    write_nsi(content)
    
    print(f"✓ Updated saugerinstaller.nsi")
    print(f"\nNext steps:")
    print(f"  git add saugerinstaller.nsi")
    print(f"  git commit -m \"Release {new_version} {new_postfix}\"")
    print(f"  git push")
    print(f"\nGitHub Actions will build and create the release automatically.")

if __name__ == "__main__":
    main()

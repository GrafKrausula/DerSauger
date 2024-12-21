import zipfile
import os
import subprocess
import sys
from generate_extension_icons import scale_png_to_sizes

def check_command(command, install_instructions):
    """Check if a command is available and provide installation instructions if not."""
    try:
        subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True)
    except FileNotFoundError:
        print(f"Error: {command[0]} is not installed.")
        print(f"Install it by running: {install_instructions}\n")
        sys.exit(1)

def check_nsis():
    """Check for NSIS availability and fallback to alternative path if necessary."""
    try:
        # Attempt to check using default `makensis`
        subprocess.run(["makensis", "/VERSION"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True)
        return "makensis"
    except FileNotFoundError:
        alternative_path = r"C:\Program Files (x86)\NSIS\makensis.exe"
        if os.path.exists(alternative_path):
            print(f"Using alternative NSIS path: {alternative_path}")
            return alternative_path
        else:
            print("Error: NSIS is not installed.")
            print("Install it by running: winget install NSIS.NSIS\n")
            sys.exit(1)

def check_prerequisites():
    """Ensure all prerequisites are met."""
    print("Checking prerequisites...")

    # Check for NSIS
    nsis_path = check_nsis()

    # Check for Git
    check_command(["git", "--version"], "winget install Git.Git")

    # Check for Python
    try:
        python_version = subprocess.check_output([sys.executable, "--version"], stderr=subprocess.STDOUT).decode().strip()
        if not python_version.startswith("Python 3.12"):
            print(f"Warning: Python 3.12 is recommended. Current version: {python_version}")
    except FileNotFoundError:
        print("Error: Python is not installed.")
        print("Install it from https://www.python.org/downloads/ or using winget:")
        print("    winget install Python.Python.3\n")
        sys.exit(1)

    # Check for virtual environment
    if not os.path.exists(".venv"):
        print("Virtual environment not found. Creating one...")
        subprocess.run([sys.executable, "-m", "venv", "venv"], check=True)
        print("Virtual environment created. Activate it with: .\\venv\\Scripts\\activate (on Windows)")

    print("All prerequisites are met!\n")
    return nsis_path

def install_requirements():
    """Install required Python packages."""
    print("Installing Python dependencies...")
    subprocess.run([sys.executable, "-m", "pip", "install", "--upgrade", "pip"], check=True)
    subprocess.run([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"], check=True)
    print("Dependencies installed successfully!\n")

def generate_icons():
    """Generate extension icons by scaling the base icon."""
    print("Generating extension icons...")
    folders = [
        r".\DerSauger\Firefox Extension\images", 
        r".\DerSauger\Chrome Extension\images"
    ]

    icon_base = "Sauger.png"

    for folder in folders:
        input_file = os.path.join(folder, icon_base)
        if not os.path.exists(input_file):
            print(f"Error: {input_file} does not exist. Ensure the base icon is available.")
            sys.exit(1)
        print(f"Scaling {input_file} to multiple sizes...")
        scale_png_to_sizes(input_file, folder)
    print("Icons generated successfully!\n")

def zip_firefox_extension():
    """Package the Firefox extension into a zip file."""
    print("Zipping Firefox extension...")
    firefox_folder = r".\DerSauger\Firefox Extension"
    zip_file = r".\DerSauger\Firefox_Extension.zip"

    if not os.path.exists(firefox_folder):
        print(f"Error: {firefox_folder} does not exist.")
        sys.exit(1)

    with zipfile.ZipFile(zip_file, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for root, _, files in os.walk(firefox_folder):
            for file in files:
                file_path = os.path.join(root, file)
                arcname = os.path.relpath(file_path, start=firefox_folder)
                zipf.write(file_path, arcname)
    print("Firefox extension packaged successfully!\n")

def build_installer(nsis_path):
    """Build the installer using NSIS."""
    print("Building the installer...")
    nsis_script = r".\saugerinstaller.nsi"

    if not os.path.exists(nsis_script):
        print(f"Error: {nsis_script} does not exist. Ensure the installer script is available.")
        sys.exit(1)

    subprocess.run([nsis_path, nsis_script], check=True)
    print("Installer built successfully!\n")

if __name__ == "__main__":
    nsis_path = check_prerequisites()
    install_requirements()
    zip_firefox_extension()
    build_installer(nsis_path)
    generate_icons()
    print("Build process completed successfully!")

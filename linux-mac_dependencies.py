import platform
import subprocess
import sys
import shutil

# ANSI escape codes for colors
GREEN = "\033[92m"
RESET = "\033[0m"

def print_green(message):
    """Print a message in green."""
    print(f"{GREEN}{message}{RESET}")

def check_command(command):
    """Check if a command is available."""
    return shutil.which(command) is not None

def check_python_package(package):
    """Check if a Python package is installed."""
    try:
        __import__(package)
        return True
    except ImportError:
        return False

def install_dependencies():
    system = platform.system()
    
    if system == "Windows":
        print_green("This script is not intended for Windows users.")
        print_green("Please run 'setup.py' instead to install all necessary dependencies.")
        print_green("Command: python setup.py")
        return

    if system == "Linux":
        print("Checking dependencies for Linux...")
        if not check_command("apt-get"):
            print("apt-get not found. Please install dependencies manually.")
            return
        
        packages_to_install = []
        if not check_command("python3-config"):
            packages_to_install.append("python3-dev")
        if not check_command("pkg-config"):
            packages_to_install.append("portaudio19-dev")
        
        if packages_to_install:
            print(f"Installing: {' '.join(packages_to_install)}")
            try:
                subprocess.run(["sudo", "apt-get", "update"], check=True)
                subprocess.run(["sudo", "apt-get", "install", "-y"] + packages_to_install, check=True)
                print("System dependencies installed successfully.")
            except subprocess.CalledProcessError:
                print("Failed to install system dependencies. Please run the commands manually:")
                print(f"sudo apt-get update && sudo apt-get install -y {' '.join(packages_to_install)}")
        else:
            print("All system dependencies are already installed.")

    elif system == "Darwin":  # macOS
        print("Checking dependencies for macOS...")
        if not check_command("brew"):
            print("Homebrew not found. Please install Homebrew or install portaudio manually.")
            return
        
        if not check_command("portaudio"):
            print("Installing portaudio...")
            try:
                subprocess.run(["brew", "install", "portaudio"], check=True)
                print("portaudio installed successfully.")
            except subprocess.CalledProcessError:
                print("Failed to install portaudio. Please run the command manually:")
                print("brew install portaudio")
        else:
            print("portaudio is already installed.")

    else:
        print("Unsupported operating system.")
        return

    print("\nChecking Python dependencies...")
    packages_to_install = []
    for package in ["sounddevice", "PySide6"]:
        if not check_python_package(package):
            packages_to_install.append(package)
    
    if packages_to_install:
        print(f"Installing Python packages: {' '.join(packages_to_install)}")
        try:
            subprocess.run([sys.executable, "-m", "pip", "install"] + packages_to_install, check=True)
            print("Python dependencies installed successfully.")
        except subprocess.CalledProcessError:
            print("Failed to install Python dependencies. Please run the command manually:")
            print(f"{sys.executable} -m pip install {' '.join(packages_to_install)}")
    else:
        print("All Python dependencies are already installed.")

if __name__ == "__main__":
    install_dependencies()
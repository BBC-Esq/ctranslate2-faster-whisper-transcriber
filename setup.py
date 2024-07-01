import subprocess
import sys
import os
from pathlib import Path
import shutil

def run_command(command):
    try:
        subprocess.run(command, shell=True, check=True)
    except subprocess.CalledProcessError as e:
        print(f"Error running command: {command}")
        print(f"Error message: {e}")
        sys.exit(1)

def move_file(src, dst):
    try:
        if not src.exists():
            print(f"Source file not found: {src}")
            return False
        shutil.move(str(src), str(dst))
        print(f"Moved {src.name} to {dst}")
        return True
    except PermissionError:
        print(f"Permission denied when trying to move {src}")
    except Exception as e:
        print(f"Error moving {src}: {e}")
    return False

def main():
    # Step 1: Upgrade pip, setuptools, and wheel
    run_command("python -m pip install --upgrade pip setuptools wheel")

    # Step 2: Install requirements
    run_command("pip install -r requirements.txt")

    # Step 3: Move files
    current_dir = Path(__file__).parent.resolve()
    python_lib_path = current_dir / 'Lib' / 'site-packages'

    files_to_move = [
        (python_lib_path / 'nvidia' / 'cublas' / 'bin' / 'cublas64_12.dll', current_dir),
        (python_lib_path / 'nvidia' / 'cublas' / 'bin' / 'cublasLt64_12.dll', current_dir),
        (python_lib_path / 'nvidia' / 'cudnn' / 'bin' / 'cudnn_cnn_infer64_8.dll', current_dir)
    ]

    all_files_moved = True
    for src, dst in files_to_move:
        if not move_file(src, dst):
            all_files_moved = False

    # Step 4: Print result message
    if all_files_moved:
        print("\033[92mInstallation was successful! The program is ready to use.")
        print(f"To run it, enter the command: python ct2_main.py\033[0m")
    else:
        print("\033[91mInstallation completed with errors. Some files could not be moved.")
        print("Please check the error messages above and try to resolve the issues manually.\033[0m")

if __name__ == "__main__":
    main()
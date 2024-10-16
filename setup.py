import subprocess
import sys
import os
import time
from pathlib import Path

def install_libraries_with_retry(max_retries=3, delay=3):
    libraries = [
        "av==12.3.0",
        "certifi==2024.7.4",
        "cffi==1.16.0",
        "chardet==5.2.0",
        "charset-normalizer==3.3.2",
        "colorama==0.4.6",
        "coloredlogs==15.0.1",
        "ctranslate2==4.3.1",
        "faster-whisper==1.0.2",
        "filelock==3.15.4",
        "flatbuffers==24.3.25",
        "fsspec==2024.9.0",
        "huggingface-hub==0.25.1",
        "humanfriendly==10.0",
        "idna==3.7",
        "mpmath==1.3.0",
        "numpy==1.26.4",
        "nvidia-cublas-cu12==12.1.3.1",
        "nvidia-cuda-nvrtc-cu12==12.1.105",
        "nvidia-cuda-runtime-cu12==12.1.105",
        "nvidia-cudnn-cu12==8.9.7.29",
        "onnxruntime==1.19.2",
        "packaging==24.1",
        "pip==24.2",
        "protobuf==5.28.2",
        "psutil==6.0.0",
        "pycparser==2.22",
        "pyreadline3==3.5.4",
        "PyYAML==6.0.1",
        "requests==2.32.3",
        "setuptools==75.1.0",
        "shiboken6==6.7.3",
        "sounddevice==0.4.7",
        "sympy==1.13.3",
        "tokenizers==0.19.1",
        "tqdm==4.66.4",
        "typing_extensions==4.12.2",
        "urllib3==2.2.2",
    ]


    failed_installations = []
    multiple_attempts = []

    for library in libraries:
        for attempt in range(max_retries):
            try:
                print(f"\nAttempt {attempt + 1} of {max_retries}: Installing {library}")
                command = [sys.executable, "-m", "uv", "pip", "install", library, "--no-deps", "--no-cache-dir"]
                subprocess.run(command, check=True, capture_output=True, text=True)
                print(f"Successfully installed {library}")
                if attempt > 0:
                    multiple_attempts.append((library, attempt + 1))
                break
            except subprocess.CalledProcessError as e:
                print(f"Attempt {attempt + 1} failed. Error: {e.stderr.strip()}")
                if attempt < max_retries - 1:
                    print(f"Retrying in {delay} seconds...")
                    time.sleep(delay)
                else:
                    print(f"Failed to install {library} after {max_retries} attempts.")
                    failed_installations.append(library)

    print("\n--- Installation Summary ---")
    if failed_installations:
        print("\nThe following libraries failed to install:")
        for lib in failed_installations:
            print(f"- {lib}")
    
    if multiple_attempts:
        print("\nThe following libraries required multiple attempts to install:")
        for lib, attempts in multiple_attempts:
            print(f"- {lib} (took {attempts} attempts)")
    
    if not failed_installations and not multiple_attempts:
        print("\nAll libraries installed successfully on the first attempt.")
    elif not failed_installations:
        print("\nAll libraries were eventually installed successfully.")

    return failed_installations, multiple_attempts

def main():
    start_time = time.time()
    
    # install uv
    print("\033[92mInstalling uv:\033[0m")
    subprocess.run(["pip", "install", "uv"], check=True)

    print("\033[92mInstalling PySide6:\033[0m")
    subprocess.run(["uv", "pip", "install", "pyside6", "--no-cache-dir", "--link-mode=copy"], check=True)
    
    # Upgrade pip, setuptools, and wheel using uv
    print("\033[92mUpgrading pip, setuptools, and wheel:\033[0m")
    subprocess.run(f"{sys.executable} -m uv pip install --upgrade pip setuptools wheel", shell=True, check=True)
    
    # Step 2: Install libraries with retry using uv
    print("\033[92mInstalling dependencies:\033[0m")
    failed, multiple = install_libraries_with_retry()
    
    if not failed:
        print("\033[92mInstallation was successful! The program is ready to use.")
        print(f"To run it, enter the command: python ct2_main.py\033[0m")
    else:
        print("\033[91mInstallation encountered some issues. Please review the installation summary above.\033[0m")

    end_time = time.time()
    total_time = end_time - start_time
    hours, rem = divmod(total_time, 3600)
    minutes, seconds = divmod(rem, 60)

    print(f"\033[92m\nTotal installation time: {int(hours):02d}:{int(minutes):02d}:{seconds:05.2f}\033[0m")

if __name__ == "__main__":
    main()
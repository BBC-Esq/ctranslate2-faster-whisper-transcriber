# Record and Transcribe Audio Using Ctranslate2!
### Record audio and save a transcription to your system's clipboard with ctranslate2 and faster-whisper.

## Prerequisites
1) Python 3.10 or 3.11.
2) [Git](https://git-scm.com/downloads)
3) [git-lfs](https://git-lfs.com/)

## Obtain Repository

Download the latest release and unzip the files to your chosen directory.

## Setup
Navigate to the folder containing ```ct2_main.py```, open a command prompt, and create a virtual environment:
```
python -m venv .
```
```
.\Scripts\activate
```
  > ‼️On Linux and MacOS run: ```source bin/activate```
```
python -m pip3 install --upgrade pip
```
## Install Platform-Specific Libraries
* Linux
```
sudo apt-get install python3-dev
```
```
sudo apt-get install portaudio19-dev
```
* MacOS
```
brew install portaudio
```
## Install Dependencies
```
pip3 install -r requirements.txt
```
* [Go here](https://github.com/SYSTRAN/faster-whisper) for instructions on how to install cublas/cudnn and any other dependencies specifically required by ```faster-whisper```.
## Install Hardware-Specific Libraries
* Nvidia GPU using CUDA 11.8 (linux or windows)
```
pip3 install faster-whisper==0.9.0
```
* Nvidia GPU using CUDA 12.1+ (linux or windows)
```
pip3 install pip install faster-whisper==1.0.0
```
> ‼️ I've received some reports of strange behavior since 1.0.0 was released.  If you encounter issues you can try using version 0.9.0, but note that it's not compatible with CUDA 12.
```pip3 install faster-whisper==0.9.0```
* AMD and MacOS systems
```
pip3 install pip install faster-whisper==1.0.0
```
> ‼️ I've received some reports of strange behavior since 1.0.0 was released.  If you encounter issues you can try using version 0.9.0, but note that it's not compatible with CUDA 12.
```pip3 install faster-whisper==0.9.0```
# Usage
Within the virtual environment run this command:
```
python ct2_main.py
```
‼️ If you receive an error something similar to this ```qt.qpa.plugin: Could not load the Qt platform plugin "xcb" in "/usr/lib/x86_64-linux-gnu/qt5/plugins/platforms"``` please check [here for a possible solution.](https://github.com/BBC-Esq/ctranslate2-faster-whisper-transcriber/issues/1).

The first time using the program, click "Update Settings" button to download the model.  After that, you can change the model and quantization (and device) by simply changing the settings and clicking "Update Settings" again.<br><br>
Click start recording, speak, then stop recording.  Then just use ```control + v``` or right click "paste" the transcription into wherever you want; for example, into the chat box for your LLM!<br><br>
Remember, anytime you want to restart the program, make sure to activate the virtual environment first!

# Record and Transcribe Audio Using Ctranslate2!
### Record audio and save a transcription to your system's clipboard with ctranslate2 and faster-whisper.

## Prerequisites
1) [Python 3.11](https://www.python.org/downloads/release/python-3119/)
2) [Git](https://git-scm.com/downloads)
3) [git-lfs](https://git-lfs.com/)

# Installation

### Step 1

Download the latest release in ZIP and extract to your computer.  Then navigate to the folder containing the ```ct2_main.py``` file, open a command prompt, and create a virtual environment.
```
python -m venv .
```
### Step 2
Activate the virtual environment.
```
.\Scripts\activate
```
  > ‼️On Linux and MacOS run: ```source bin/activate```
### Step 3
Run the installation script.
```
python setup.py
```
### Step 4 (only for Linux or Mac users)
The ```setup.py``` script should handle everything, but if you encounter errors on Linux or MacOS you might need to install additional dependencies.  You can try using [linux-mac_dependencies.py](https://github.com/BBC-Esq/ctranslate2-faster-whisper-transcriber/blob/main/linux-mac_dependencies.py) or the following:
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

# Usage
Within the virtual environment run this command:
```
python ct2_main.py
```
‼️ If you receive an error something similar to this ```qt.qpa.plugin: Could not load the Qt platform plugin "xcb"``` please check [here for a possible solution.](https://github.com/BBC-Esq/ctranslate2-faster-whisper-transcriber/issues/1).

<details><summary>EXAMPLE COMMANDS</summary>

![image](https://github.com/BBC-Esq/ctranslate2-faster-whisper-transcriber/assets/108230321/a00f9625-4aad-44e9-b6aa-5ebddd63ace4)

</details>

The first time using the program, click "Update Settings" button to download the model.  After that, you can change the model and quantization (and device) by simply changing the settings and clicking "Update Settings" again.<br><br>
Click start recording, speak, then stop recording.  Then just use ```control + v``` or right click "paste" the transcription into wherever you want; for example, into the chat box for your LLM!<br><br>
Remember, anytime you want to restart the program, make sure to activate the virtual environment first!

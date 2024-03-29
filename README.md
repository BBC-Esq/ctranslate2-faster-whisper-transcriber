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
## Install Faster-Whisper
```
pip3 install faster-whisper==0.10.1
```
## Nvidia GPU support
Only systems with GPU acceleration need to follow this step:
  > [Go here](https://github.com/SYSTRAN/faster-whisper) for instructions on how to get the "cublas" and "cudnn" libraries and place them in the directory.<br>
  > Alternatively, [you can go here](https://github.com/Purfview/whisper-standalone-win/releases/tag/libs).

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

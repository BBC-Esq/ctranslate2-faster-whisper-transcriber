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
## Install Hardware-Specific Libraries
* Nvidia GPU (using CUDA 11.8)
```
pip3 install torch==2.1.2 torchvision==0.16.2 torchaudio==2.1.2 --index-url https://download.pytorch.org/whl/cu118
```
```
pip3 install https://files.pythonhosted.org/packages/ff/11/401db7f4bfdcec3c4bd685297c2fb11a3caa0a0fa3288bd209f973b877bb/faster_whisper-0.9.0-py3-none-any.whl
```
* Nvidia GPU (using CUDA 12.1+)
```
pip3 install pip install torch==2.1.2 torchvision==0.16.2 torchaudio==2.1.2 --index-url https://download.pytorch.org/whl/cu121
```
```
pip3 install pip install faster-whisper==1.0.0
```
* AMD GPU (rocM 5.6 on Linux)
```
pip3 install pip install torch==2.1.2 torchvision==0.16.2 torchaudio==2.1.2 --index-url https://download.pytorch.org/whl/rocm5.6
```
```
pip3 install pip3 install https://files.pythonhosted.org/packages/ff/11/401db7f4bfdcec3c4bd685297c2fb11a3caa0a0fa3288bd209f973b877bb/faster_whisper-0.9.0-py3-none-any.whl
```
* AMD GPU (on windows)
  * Not supported by Pytorch.  Install CPU version of Pytorch.
* MacOS
```
pip3 install torch==2.1.2 torchvision==0.16.2 torchaudio==2.1.2
```
* CPU Only
```
pip3 install pip install torch==2.1.2 torchvision==0.16.2 torchaudio==2.1.2 --index-url https://download.pytorch.org/whl/cpu
```

# Usage
Within the virtual environment run this command:
```
python ct2_main.py
```
The first time using the program, click "Update Settings" button to download the model.  After that, you can change the model and quantization (and device) by simply changing the settings and clicking "Update Settings" again.<br><br>
Click start recording, speak, then stop recording.  Then just use ```control + v``` or right click "paste" the transcription into wherever you want; for example, into the chat box for your LLM!<br><br>
Remember, anytime you want to restart the program, make sure to activate the virtual environment first!

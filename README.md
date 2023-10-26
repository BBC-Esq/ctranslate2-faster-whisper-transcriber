# Record and Transcribe Audio Using Ctranslate2!
### Record audio and save a transcription to your system's clipboard with ctranslate2 and faster-whisper.

## Prerequisites
> Tested on [Python 3.10.11](https://www.python.org/downloads/release/python-31011/).
> You must have both [Git](https://git-scm.com/downloads) and [git-lfs](https://git-lfs.com/) installed.<br>
> If you intend to use CUDA acceleration, you must also install [CUDA 11.8](https://developer.nvidia.com/cuda-11-8-0-download-archive).
  > * Unfortunately, Ctranslate2 does not currently support GPU-acceleration on AMD GPUs or Apple's Metal/MPS. However, CPU acceleration still works.

## Installation

Step 1 - Download the latest release and unzip the files to your chosen directory.

Step 2 - Navigate to the folder with ```ct2_main.py``` in it, open a command prompt, and create a virtual environment:
```
python -m venv .
```
  > NOTE: For any ```python``` or ```pip``` commands in these instructions, if you still have Python 2 installed, make sure and run ```python3``` and ```pip3``` instead to make sure the correct Python interpreter is used.

Step 3 - Activate the virtual environment:
```
.\Scripts\activate
```
  > ‼️On Linux and MacOS run: ```source bin/activate```

Step 4 - Upgrade Pip
```
python -m pip install --upgrade pip
```

Step 5 - If you want to use CUDA acceleration run:
```
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118
```

Step 6 - Install additional requirements:
> ‼️On Linux systems run this first: ```sudo apt-get install portaudio19-dev``` and ```sudo apt-get install python3-dev```

> ‼️On MacOS systems run this first: ```brew install portaudio```
```
pip install -r requirements.txt
```

## Usage
Within the virtual environment run this command:
```
python ct2_main.py
```
The first time using the program, I recommend using the default settings and clicking "Update Settings" button to download the model.  After that, simply change the settings and click "Update Settings" for them to take effect.<br><br>
Now just use ```control + v``` or right click "paste" after the transcription is saved to the clipboard; for example, into the chat box for your LLM!
Remember, anytime you want to restart the program, make sure to activate the virtual environment first!

## Contact

### Feel free to contact me on here or at bbc@chintellalaw.com.  Any suggestions (positive or negative) are welcome.

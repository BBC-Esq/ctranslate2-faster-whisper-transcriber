# Record and Transcribe Audio Using Ctranslate2!
Record audio and save a transcription to your system's clipboard with ctranslate2 and faster-whisper.

## Using with No Installation Approach
There are two executables in the [latest release](https://github.com/BBC-Esq/ctranslate2-faster-whisper-transcriber/releases/tag/v1.1) no installation needed.  Linux users will need to follow [these additional instructions](https://github.com/BBC-Esq/ctranslate2-faster-whisper-transcriber/blob/main/linux_instructions.png).

## Installation Instructions
> Make sure you have at least [Python 3.10+](https://www.python.org/downloads/release/python-31011/).
> You must have both [Git](https://git-scm.com/downloads) and [git-lfs](https://git-lfs.com/) installed.<br>
> If you intend to use CUDA acceleration, you must also install [CUDA 11.8](https://developer.nvidia.com/cuda-11-8-0-download-archive).
  > * Unfortunately, Ctranslate2 does not currently support GPU-acceleration on AMD GPUs or Apple's Metal/MPS. However, CPU acceleration still works.

Step 1 - Download the latest release ZIP file and extract it to a folder.

Step 2 - Within the folder containing ```main.py```, create a command prompt and create a virtual environment by running:
```
python -m venv .
```
  > NOTE: For any ```python``` or ```pip``` commands in these instructions, if you installed Python 3 but still have Python 2 installed, you should use ```Python3``` or ```pip3``` instead to make sure that the correct version of Python is used.

Step 3 - Activate the virtual environment:
```
.\Scripts\activate
```
  > ‼️On Linux run: ```source bin/activate```

Step 4 - Upgrade Pip
```
python -m pip install --upgrade pip
```

Step 5 - If you want to use CUDA acceleration run:
```
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118
```

Step 6 - Install additional requirements:
> ‼️On Linux systems run this first: ```sudo apt-get install portaudio19-dev```

> ‼️On MacOS systems run this first: ```brew install portaudio```
```
pip install -r requirements.txt
```

## Usage
Within the virtual environment run this command:
```
python main.py
```
The model will download to cache the first time you use the program.
Now just use ```control + v``` or right click "paste" after the transcription is saved to the clipboard; for example, into the chat box for your LLM!
Remember, anytime you want to restart the program, make sure to activate the virtual environment first!

## Changing Model Size or Quantization
You can change the size/quantization of the model used by changing ```line 17``` of ```main.py``` to/from any of the following:

>  * ```tiny```
>  * ```tiny.en```
>  * ```base```
>  * ```base.en```
>  * ```small```
>  * ```small.en```
>  * ```medium```
>  * ```medium.en```
>  * ```large-v2```

Look within ```main.py``` for more detailed instructions.

### Feel free to contact me on here or at bbc@chintellalaw.com.  Any suggestions (positive or negative) are welcome.

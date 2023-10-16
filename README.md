# Record and Transcribe Audio Using Ctranslate2!
Record audio and save a transcription to your system's clipboard with ctranslate2 and faster-whisper.

## No Installation Usage
There are two executables in the [latest release](https://github.com/BBC-Esq/ctranslate2-faster-whisper-transcriber/releases/tag/v1.1) no installation needed.  Linux users will need to follow [these additional instructions]([https://github.com/BBC-Esq/ctranslate2-faster-whisper-transcriber/blob/main/linux_instructions.png](https://github.com/BBC-Esq/ctranslate2-faster-whisper-transcriber/blob/main/linux_instructions.png?raw=true)).

## Installation Instructions
> Make sure have at least [Python 3.10+](https://www.python.org/downloads/release/python-31011/).
> You must have both [Git](https://git-scm.com/downloads) and [git-lfs](https://git-lfs.com/) installed.<br>
> If you intend to use CUDA acceleration, you must also install [CUDA 11.8](https://developer.nvidia.com/cuda-11-8-0-download-archive).
  > * Unfortuantely, Ctranslate2 does not currentlly support gpu-acceleration on AMD GPUs or Apple's metal/mps.  However, CPU acceleration still works.

Step1 - Download the latest releaze ZIP file, extract to a folder.

Step2 - Within the folder containing ```main.py```, create a command prompt and create a virtual environment by running:
```
python -m venv .
```
  > NOTE: For any ```python``` commands in these instructions, if you installed Python 3 but still have Python 2 installed, you should use ```Python3``` when running the commands to make sure that the correct version of Python is used.

Step3 - Activate the virtual environment:
```
.\Scripts\activate
```
  > On linux run: ```source bin/activate```

Step4 - Upgrade Pip
```
python -m pip install --upgrade pip
```

Step5 - If you want to use CUDA acceleration run:
```
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118
```

Step6 - Install additional requirements:
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
Remember, anytime you want to restart the program make sure and activate the virtual environment first!

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

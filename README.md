# Record and Transcribe Audio Using Ctranslate2!
Record audio and save a transcription to your system's clipboard with ctranslate2 and faster-whisper.

## Installation
Download the latest release and save to disk.
> If you intend to use CUDA acceleration instead of CPU you must also install [CUDA 11.8](https://developer.nvidia.com/cuda-11-8-0-download-archive) prior to the next steps.
  > * Unfortuantely, Ctranslate2 does not currentlly support gpu-acceleration on AMD GPUs or Apple's metal/mps.  However, CPU acceleration will still kick in.

Within the folder saved, create a command prompt and create a virtual environment:
```
python -m venv .
```
Activate the virtual environment:
```
.\Scripts\activate
```
ONLY use the following command if you have an Nvidia GPU:
> Don't forget to install CUDA 11.8 first.
```
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118
```
Install additional requirements:
```
pip install -r requirements.txt
```
Run the program!
```
python main.py
```
> Please note!  You can change the size/quality of the model used by changing ```line 17``` of ```main.py``` to/from any of the following:

>  * ```tiny```
>  * ```tiny.en```
>  * ```base```
>  * ```base.en```
>  * ```small```
>  * ```small.en```
>  * ```medium```
>  * ```medium.en```
>  * ```large-v2```

### See more detailed instructions within the ```main.py``` script itself.

### That's it!  The model will download to cache the first time you use the program.

Now just use ```control + v``` or right click "paste" after the transcription is saved to the clipboard; for example, into the chat box for your LLM!

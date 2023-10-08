# Record and Transcribe Audio Using Ctranslate2 and Faster-Whisper!
Record audio and save a transcription to your system's clipboard with ctranslate2 and faster-whisper.

## Installation
Download the latest release and save to disk.

Within the folder saved, create a command prompt and create a virtual environment:
```
python -m venv .
```
Activate the virtual environment:
```
.\Scripts\activate
```
Install the requirements:
```
pip install -r requirements.txt
```
Run the program!
```
python main.py
```
> Please note!  You can change the size/quality of the model used by changing ```line 17``` of ```main.py``` from ```large-v2``` to any of the following:

>  * ```tiny```
>  * ```tiny.en```
>  * ```base```
>  * ```base.en```
>  * ```small```
>  * ```small.en```
>  * ```medium```
>  * ```medium.en```

## That's it!  The model will download to cache the first time you use the program.

Now just use ```control + v``` or right click "paste" after the transcription is saved to the clipboard; for example, into the chat box for your LLM!

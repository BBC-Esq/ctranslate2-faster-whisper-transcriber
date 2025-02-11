# Record and Transcribe Audio Using Ctranslate2!
Easily record audio to your system's clipboard so you can copy and paste it.

## Requirments
1) Python 3.11 or Python 3.12
2) [Git](https://git-scm.com/downloads)
3) [git-lfs](https://git-lfs.com/)
4) Windows
  > I am open to Linux and MacOS support but would need someone to help me test it.

# Installation

### Step 1
Download the latest release (i.e. the .zip file) and extract its contents to your computer.  Then navigate to the folder containing ```ct2_main.py``` and create a virtual environment.
```
python -m venv .
```
### Step 2
Activate the virtual environment.
```
.\Scripts\activate
```
### Step 3
Run the installation script.
```
python setup.py
```

# Usage

### Step 1
Activate the virtual environment and start the program:
```
python ct2_main.py
```
### Step 2
Choose the Whisper model you want to use and click "Update Settings". The first time you choose a particular model it will automatically download it.<br><br>

### Step 3
Start recording...speak...stop recording, then use ```control + v``` or right-click and "paste" the transcription into whatever program you want; for example, into the browser window for ChatGPT.<br><br>

# Creating an .exe file

* ```pip install pyinstaller```
* ```pyinstaller --onefile ct2_main.py```



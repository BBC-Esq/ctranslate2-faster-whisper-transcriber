import sys
import pyaudio
import wave
import os
import tempfile
import threading
import pyperclip
from faster_whisper import WhisperModel
from PySide6.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QLabel
from PySide6.QtCore import Qt

class VoiceRecorder:
    def __init__(self, window, format=pyaudio.paInt16, channels=1, rate=44100, chunk=1024):
        self.format, self.channels, self.rate, self.chunk = format, channels, rate, chunk
        self.window = window
        self.is_recording, self.frames = False, []
        self.model = WhisperModel("ctranslate2-4you/whisper-base.en-ct2-float32", device="auto", compute_type="float32", cpu_threads=8)
    
    """
    
    NOTES:
    
    "auto" - uses CUDA if available or falls back to CPU.  You can specify "CUDA" or "CPU" if you want.  Unfortunately, Ctranslate2 doesn't
    support AMD GPU acceleration currently, although it does support acceleration on AMD CPUs.
    
    "cpu-threads" - specifies the number of cpu threads to use when CPU is used (not CUDA). It is OK to keep this even if you use CUDA
    because it will be simply be disregarded.  Always leave at least 2-4 threads available for background tasks.
    
    To change the size of the model, change "base.en" to/from any of the following:

    tiny
    tiny.en
    base
    base.en
    small
    small.en
    medium
    medium.en
    large-v2

    To change the quantization of the model, change "float32" in TWO places.  For example:

    self.model = WhisperModel("ctranslate2-4you/whisper-tiny.en-ct2-float16", device="auto", compute_type="float16", cpu_threads=8)

    For CPU usage, I strongly recommend only using "float32" or "int8_float32" (if you need to save some VRAM).
    For CUDA usage, you have more flexibility.  My recommendations are:

    bfloat16 (only supported by NVIDIA RTX 4060 and up)
    float16 (only supported by NVIDIA GTX 1650 and up)
    int8_float32 (to save VRAM...supported by NVIDIA GTX 1650 and up)
    float32 (you must use float32 for NVIDIA GPUs prior to GTX 1650)

    Ctranslate2 will change the quantization at runtime if you don't use specify a compatible quant, but this adds overhead and
    will harm performance.
    
    """

    def transcribe_audio(self, audio_file):
        segments, _ = self.model.transcribe(audio_file)
        pyperclip.copy("\n".join([segment.text for segment in segments]))
        self.window.update_status("Audio saved and transcribed")

    def record_audio(self):
        self.window.update_status("Recording...")
        p = pyaudio.PyAudio()
        try:
            stream = p.open(format=self.format, channels=self.channels, rate=self.rate, input=True, frames_per_buffer=self.chunk)
            [self.frames.append(stream.read(self.chunk)) for _ in iter(lambda: self.is_recording, False)]
            stream.stop_stream()
            stream.close()
        finally:
            p.terminate()

    def save_audio(self):
        self.is_recording = False
        temp_filename = tempfile.mktemp(suffix=".wav")
        with wave.open(temp_filename, "wb") as wf:
            wf.setnchannels(self.channels)
            wf.setsampwidth(pyaudio.PyAudio().get_sample_size(self.format))
            wf.setframerate(self.rate)
            wf.writeframes(b"".join(self.frames))
        self.transcribe_audio(temp_filename)
        os.remove(temp_filename)
        self.frames.clear()

    def start_recording(self):
        if not self.is_recording:
            self.is_recording = True
            threading.Thread(target=self.record_audio).start()

class MyWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.recorder = VoiceRecorder(self)
        layout = QVBoxLayout(self)

        for text, callback in [("Record", self.recorder.start_recording), 
                               ("Stop and Copy to Clipboard", self.recorder.save_audio)]:
            button = QPushButton(text, self)
            button.clicked.connect(callback)
            layout.addWidget(button)

        self.status_label = QLabel('', self)
        layout.addWidget(self.status_label)
        self.setFixedSize(300, 150)
        
        self.setWindowFlag(Qt.WindowStaysOnTopHint)

    def update_status(self, text):
        self.status_label.setText(text)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyle('Fusion')
    window = MyWindow()
    window.show()
    sys.exit(app.exec())

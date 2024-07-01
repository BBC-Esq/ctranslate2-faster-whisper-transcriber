import sounddevice as sd
import numpy as np
import wave
import os
import tempfile
import threading
from faster_whisper import WhisperModel
import yaml
from PySide6.QtWidgets import QApplication
from PySide6.QtGui import QClipboard

class VoiceRecorder:
    def __init__(self, window, samplerate=44100, channels=1, dtype='int16'):
        self.samplerate, self.channels, self.dtype = samplerate, channels, dtype
        self.window = window
        self.is_recording, self.frames = False, []
        self.load_settings()

    def load_settings(self):
        try:
            with open("config.yaml", "r") as f:
                config = yaml.safe_load(f)
                if "device_type" not in config:
                    config["device_type"] = "cpu"
                if "model_name" not in config:
                    config["model_name"] = "base.en"
                if "quantization_type" not in config:
                    config["quantization_type"] = "int8"
                self.update_model(config["model_name"], config["quantization_type"], config["device_type"])
        except FileNotFoundError:
            self.update_model("base.en", "int8", "cpu")

    def save_settings(self, model_name, quantization_type, device_type):
        try:
            with open("config.yaml", "r") as f:
                config = yaml.safe_load(f)
        except FileNotFoundError:
            config = {}
        config["model_name"] = model_name
        config["quantization_type"] = quantization_type
        config["device_type"] = device_type
        with open("config.yaml", "w") as f:
            yaml.safe_dump(config, f)

    def update_model(self, model_name, quantization_type, device_type):
        model_str = f"ctranslate2-4you/whisper-{model_name}-ct2-{quantization_type}"
        self.model = WhisperModel(model_str, device=device_type, compute_type=quantization_type, cpu_threads=26)
        self.window.update_status(f"Model updated to {model_name} with {quantization_type} quantization on {device_type} device")
        self.save_settings(model_name, quantization_type, device_type)

    def transcribe_audio(self, audio_file):
        segments, _ = self.model.transcribe(audio_file)
        clipboard_text = "\n".join([segment.text for segment in segments])
        
        clipboard = QApplication.clipboard()
        clipboard.setText(clipboard_text)
        
        self.window.update_status("Audio saved and transcribed")

    def record_audio(self):
        self.window.update_status("Recording...")
        def callback(indata, frames, time, status):
            if status:
                print(status)
            self.frames.append(indata.copy())
        with sd.InputStream(samplerate=self.samplerate, channels=self.channels, dtype=self.dtype, callback=callback):
            while self.is_recording:
                sd.sleep(100)

    def save_audio(self):
        self.is_recording = False
        temp_filename = tempfile.mktemp(suffix=".wav")
        data = np.concatenate(self.frames, axis=0)
        with wave.open(temp_filename, "wb") as wf:
            wf.setnchannels(self.channels)
            wf.setsampwidth(2)  # Always 2 for int16
            wf.setframerate(self.samplerate)
            wf.writeframes(data.tobytes())
        self.transcribe_audio(temp_filename)
        os.remove(temp_filename)
        self.frames.clear()

    def start_recording(self):
        if not self.is_recording:
            self.is_recording = True
            threading.Thread(target=self.record_audio).start()
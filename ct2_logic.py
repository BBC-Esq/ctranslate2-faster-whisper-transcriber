import sounddevice as sd
import numpy as np
import wave
import os
import tempfile
import threading
from faster_whisper import WhisperModel
import yaml
from PySide6.QtWidgets import QApplication
from PySide6.QtCore import QObject, Signal, Slot

class VoiceRecorder(QObject):
    update_status_signal = Signal(str)
    enable_widgets_signal = Signal(bool)
    copy_to_clipboard_signal = Signal(str)

    def __init__(self, window, samplerate=44100, channels=1, dtype='int16'):
        super().__init__()
        self.samplerate, self.channels, self.dtype = samplerate, channels, dtype
        self.window = window
        self.is_recording, self.frames = False, []
        self.model = None
        self.load_settings()

        # Connect the signal to the slot
        self.copy_to_clipboard_signal.connect(self.copy_to_clipboard)

    def load_settings(self):
        try:
            with open("config.yaml", "r") as f:
                config = yaml.safe_load(f)
                model_name = config.get("model_name", "base.en")
                quantization_type = config.get("quantization_type", "int8")
                device_type = config.get("device_type", "cpu")
                self.update_model(model_name, quantization_type, device_type)
        except FileNotFoundError:
            self.update_model("base.en", "int8", "cpu")

    def save_settings(self, model_name, quantization_type, device_type):
        config = {
            "model_name": model_name,
            "quantization_type": quantization_type,
            "device_type": device_type
        }
        with open("config.yaml", "w") as f:
            yaml.safe_dump(config, f)

    def update_model(self, model_name, quantization_type, device_type):
        self.enable_widgets_signal.emit(False)
        self.update_status_signal.emit(f"Updating model to {model_name}...")
        
        def update_model_thread():
            try:
                if model_name.startswith("distil-whisper"):
                    model_str = f"ctranslate2-4you/{model_name}-ct2-{quantization_type}"
                else:
                    model_str = f"ctranslate2-4you/whisper-{model_name}-ct2-{quantization_type}"
                
                self.model = WhisperModel(model_str, device=device_type, compute_type=quantization_type, cpu_threads=26)
                self.save_settings(model_name, quantization_type, device_type)
                self.update_status_signal.emit(f"Model updated to {model_name} on {device_type} device")
            except Exception as e:
                self.update_status_signal.emit(f"Error updating model: {str(e)}")
            finally:
                self.enable_widgets_signal.emit(True)
        
        threading.Thread(target=update_model_thread).start()

    def transcribe_audio(self, audio_file):
        self.update_status_signal.emit("Transcribing audio...")
        try:
            segments, _ = self.model.transcribe(audio_file)
            clipboard_text = "\n".join([segment.text for segment in segments])
            
            # Emit signal to copy text to clipboard in main thread
            self.copy_to_clipboard_signal.emit(clipboard_text)
            
            self.update_status_signal.emit("Audio transcribed and copied to clipboard")
        except Exception as e:
            self.update_status_signal.emit(f"Transcription failed: {e}")
        finally:
            self.enable_widgets_signal.emit(True)
            try:
                os.remove(audio_file)
            except OSError as e:
                print(f"Error deleting temporary file: {e}")

    @Slot(str)
    def copy_to_clipboard(self, text):
        QApplication.instance().clipboard().setText(text)

    def record_audio(self):
        self.update_status_signal.emit("Recording...")
        def callback(indata, frames, time, status):
            if status:
                print(status)
            self.frames.append(indata.copy())
        with sd.InputStream(samplerate=self.samplerate, channels=self.channels, dtype=self.dtype, callback=callback):
            while self.is_recording:
                sd.sleep(100)

    def save_audio(self):
        self.is_recording = False
        self.enable_widgets_signal.emit(False)
        temp_filename = tempfile.mktemp(suffix=".wav")
        data = np.concatenate(self.frames, axis=0)
        with wave.open(temp_filename, "wb") as wf:
            wf.setnchannels(self.channels)
            wf.setsampwidth(2)  # Always 2 for int16
            wf.setframerate(self.samplerate)
            wf.writeframes(data.tobytes())
        
        self.update_status_signal.emit("Audio saved, starting transcription...")
        threading.Thread(target=self.transcribe_audio, args=(temp_filename,)).start()
        self.frames.clear()

    def start_recording(self):
        if not self.is_recording:
            self.is_recording = True
            threading.Thread(target=self.record_audio).start()

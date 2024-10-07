import sounddevice as sd
import numpy as np
import wave
import os
import tempfile
from PySide6.QtWidgets import QApplication
from PySide6.QtCore import QObject, Signal, Slot, QThread
from faster_whisper import WhisperModel
import yaml
import threading
import logging
from ct2_llm import LLMFormatter

logger = logging.getLogger(__name__)

class ModelLoaderThread(QThread):
    model_loaded = Signal(object, str)
    error_occurred = Signal(str)

    def __init__(self, model_name, quantization_type, device_type):
        super().__init__()
        self.model_name = model_name
        self.quantization_type = quantization_type
        self.device_type = device_type

    def run(self):
        try:
            if self.model_name.startswith("distil-whisper"):
                model_str = f"ctranslate2-4you/{self.model_name}-ct2-{self.quantization_type}"
            else:
                model_str = f"ctranslate2-4you/whisper-{self.model_name}-ct2-{self.quantization_type}"

            model = WhisperModel(
                model_str,
                device=self.device_type,
                compute_type=self.quantization_type,
                cpu_threads=26
            )
            self.model_loaded.emit(model, self.model_name)
        except Exception as e:
            error_message = f"Error loading model: {str(e)}"
            logger.error(error_message)
            self.error_occurred.emit(error_message)

class TranscriptionThread(QThread):
    transcription_done = Signal(str)
    error_occurred = Signal(str)

    def __init__(self, model, audio_file):
        super().__init__()
        self.model = model
        self.audio_file = audio_file

    def run(self):
        try:
            segments, _ = self.model.transcribe(self.audio_file)
            clipboard_text = "\n".join([segment.text for segment in segments])
            # Find all instances of "  " and replace them with " "
            clipboard_text = clipboard_text.replace("  ", " ")
            # strip leading and trailing whitespace from the clipboard
            clipboard_text = clipboard_text.strip()

            llm_formatter = LLMFormatter()
            clipboard_text = llm_formatter.format_transcription(clipboard_text)

            print(clipboard_text)

            self.transcription_done.emit(clipboard_text)
        except Exception as e:
            error_message = f"Transcription failed: {str(e)}"
            logger.error(error_message)
            self.error_occurred.emit(error_message)
        finally:
            try:
                os.remove(self.audio_file)
            except OSError as e:
                logger.warning(f"Error deleting temporary file: {e}")

class VoiceRecorder(QObject):
    update_status_signal = Signal(str)
    enable_widgets_signal = Signal(bool)

    def __init__(self, window, samplerate=44100, channels=1, dtype='int16'):
        super().__init__()
        self.samplerate = samplerate
        self.channels = channels
        self.dtype = dtype
        self.window = window
        self.is_recording = False
        self.frames = []
        self.model = None
        self.model_lock = threading.Lock()
        self.load_settings()

    def load_settings(self):
        try:
            with open("config.yaml", "r") as f:
                config = yaml.safe_load(f)
                model_name = config.get("model_name", "base.en")
                quantization_type = config.get("quantization_type", "int8")
                device_type = config.get("device_type", "cpu")
                self.update_model(model_name, quantization_type, device_type)
        except FileNotFoundError:
            logger.warning("config.yaml not found. Using default settings.")
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
        
        self.model_loader_thread = ModelLoaderThread(model_name, quantization_type, device_type)
        self.model_loader_thread.model_loaded.connect(self.on_model_loaded)
        self.model_loader_thread.error_occurred.connect(self.on_model_load_error)
        self.model_loader_thread.start()

    @Slot(object, str)
    def on_model_loaded(self, model, model_name):
        with self.model_lock:
            self.model = model
        self.save_settings(model_name, self.model_loader_thread.quantization_type, self.model_loader_thread.device_type)
        self.update_status_signal.emit(f"Model updated to {model_name} on {self.model_loader_thread.device_type} device")
        self.enable_widgets_signal.emit(True)

    @Slot(str)
    def on_model_load_error(self, error_message):
        self.update_status_signal.emit(error_message)
        self.enable_widgets_signal.emit(True)

    def transcribe_audio(self, audio_file):
        self.update_status_signal.emit("Transcribing audio...")
        with self.model_lock:
            if self.model is None:
                self.update_status_signal.emit("No model loaded.")
                self.enable_widgets_signal.emit(True)
                return
            model = self.model

        self.transcription_thread = TranscriptionThread(model, audio_file)
        self.transcription_thread.transcription_done.connect(self.on_transcription_done)
        self.transcription_thread.error_occurred.connect(self.on_transcription_error)
        self.transcription_thread.start()

    @Slot(str)
    def on_transcription_done(self, clipboard_text):
        QApplication.instance().clipboard().setText(clipboard_text)
        self.update_status_signal.emit("Audio transcribed and copied to clipboard")
        self.enable_widgets_signal.emit(True)

    @Slot(str)
    def on_transcription_error(self, error_message):
        self.update_status_signal.emit(error_message)
        self.enable_widgets_signal.emit(True)

    def record_audio(self):
        self.update_status_signal.emit("Recording...")
        def callback(indata, frames, time, status):
            if status:
                logger.warning(status)
            self.frames.append(indata.copy())
        try:
            with sd.InputStream(samplerate=self.samplerate, channels=self.channels, dtype=self.dtype, callback=callback):
                while self.is_recording:
                    sd.sleep(100)
        except Exception as e:
            error_message = f"Recording error: {e}"
            logger.error(error_message)
            self.update_status_signal.emit(error_message)
            self.enable_widgets_signal.emit(True)

    def save_audio(self):
        self.is_recording = False
        self.enable_widgets_signal.emit(False)
        temp_filename = tempfile.mktemp(suffix=".wav")
        data = np.concatenate(self.frames, axis=0)
        try:
            with wave.open(temp_filename, "wb") as wf:
                wf.setnchannels(self.channels)
                wf.setsampwidth(2)  # Always 2 for int16
                wf.setframerate(self.samplerate)
                wf.writeframes(data.tobytes())
            
            self.update_status_signal.emit("Audio saved, starting transcription...")
            self.transcribe_audio(temp_filename)
        except Exception as e:
            error_message = f"Error saving audio: {e}"
            logger.error(error_message)
            self.update_status_signal.emit(error_message)
            self.enable_widgets_signal.emit(True)
        finally:
            self.frames.clear()

    def start_recording(self):
        if not self.is_recording:
            self.is_recording = True
            threading.Thread(target=self.record_audio).start()
        else:
            self.update_status_signal.emit("Already recording.")

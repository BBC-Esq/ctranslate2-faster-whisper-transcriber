import sounddevice as sd
import numpy as np
import wave
import os
import psutil
from PySide6.QtWidgets import QApplication
from PySide6.QtCore import QObject, Signal, Slot, QThread, QMutex, QWaitCondition
from faster_whisper import WhisperModel
import yaml
import logging
import tempfile
from contextlib import contextmanager
from pathlib import Path
import queue

from ct2_utils import get_resource_path

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
            if self.isInterruptionRequested():
                return

            if self.model_name.startswith("distil-whisper"):
                model_str = f"ctranslate2-4you/{self.model_name}-ct2-{self.quantization_type}"
            else:
                model_str = f"ctranslate2-4you/whisper-{self.model_name}-ct2-{self.quantization_type}"

            if self.isInterruptionRequested():
                return

            model = WhisperModel(
                model_str,
                device=self.device_type,
                compute_type=self.quantization_type,
                cpu_threads=psutil.cpu_count(logical=False)
            )

            if self.isInterruptionRequested():
                return

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
            if self.isInterruptionRequested():
                return

            segments, _ = self.model.transcribe(self.audio_file)

            if self.isInterruptionRequested():
                return

            clipboard_text = "\n".join([segment.text for segment in segments])
            self.transcription_done.emit(clipboard_text)
        except Exception as e:
            error_message = f"Transcription failed: {str(e)}"
            logger.error(error_message)
            self.error_occurred.emit(error_message)
        finally:
            try:
                Path(self.audio_file).unlink(missing_ok=True)
            except OSError as e:
                logger.warning(f"Error deleting temporary file: {e}")

class RecordingThread(QThread):
    update_status_signal = Signal(str)
    recording_error = Signal(str)
    recording_finished = Signal()

    def __init__(self, samplerate, channels, dtype):
        super().__init__()
        self.samplerate = samplerate
        self.channels = channels
        self.dtype = dtype
        self.is_recording = QWaitCondition()
        self.mutex = QMutex()
        self.buffer = queue.Queue()

    @contextmanager
    def audio_stream(self):
        stream = sd.InputStream(samplerate=self.samplerate, channels=self.channels, dtype=self.dtype, callback=self.audio_callback)
        try:
            with stream:
                yield
        finally:
            stream.close()

    def audio_callback(self, indata, frames, time, status):
        if status:
            logger.warning(status)
        self.buffer.put(indata.copy())

    def run(self):
        self.mutex.lock()
        self.update_status_signal.emit("Recording...")

        try:
            with self.audio_stream():
                while not self.isInterruptionRequested():
                    self.is_recording.wait(self.mutex)
        except Exception as e:
            error_message = f"Recording error: {e}"
            logger.error(error_message)
            self.recording_error.emit(error_message)
        finally:
            self.mutex.unlock()
            self.recording_finished.emit()

    def stop(self):
        self.requestInterruption()
        self.is_recording.wakeAll()

class VoiceRecorder(QObject):
    update_status_signal = Signal(str)
    enable_widgets_signal = Signal(bool)

    def __init__(self, window, samplerate=44100, channels=1, dtype='int16'):
        super().__init__()
        self.samplerate = samplerate
        self.channels = channels
        self.dtype = dtype
        self.window = window
        self.model = None
        self.model_mutex = QMutex()
        self.load_settings()

    def load_settings(self):
        config_path = Path(get_resource_path("config.yaml"))
        try:
            with config_path.open("r") as f:
                config = yaml.safe_load(f)
                model_name = config.get("model_name", "base.en")
                quantization_type = config.get("quantization_type", "int8")
                device_type = config.get("device_type", "cpu")
                self.update_model(model_name, quantization_type, device_type)
        except FileNotFoundError:
            logger.warning("config.yaml not found. Using default settings.")
            self.update_model("base.en", "int8", "cpu")

    def save_settings(self, model_name, quantization_type, device_type):
        config_path = Path(get_resource_path("config.yaml"))
        try:
            with config_path.open("r") as f:
                config = yaml.safe_load(f) or {}
        except FileNotFoundError:
            config = {}

        config.update({
            "model_name": model_name,
            "quantization_type": quantization_type,
            "device_type": device_type
        })

        logger.debug(f"Saving updated settings to config: {config}")
        with config_path.open("w") as f:
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
        self.model_mutex.lock()
        self.model = model
        self.model_mutex.unlock()
        self.save_settings(model_name, self.model_loader_thread.quantization_type, self.model_loader_thread.device_type)
        self.update_status_signal.emit(f"Model updated to {model_name} on {self.model_loader_thread.device_type} device")
        self.enable_widgets_signal.emit(True)

    @Slot(str)
    def on_model_load_error(self, error_message):
        self.update_status_signal.emit(error_message)
        self.enable_widgets_signal.emit(True)

    def transcribe_audio(self, audio_file):
        self.update_status_signal.emit("Transcribing audio...")
        self.model_mutex.lock()
        if self.model is None:
            self.model_mutex.unlock()
            self.update_status_signal.emit("No model loaded.")
            self.enable_widgets_signal.emit(True)
            return
        model = self.model
        self.model_mutex.unlock()

        self.transcription_thread = TranscriptionThread(model, audio_file)
        self.transcription_thread.transcription_done.connect(self.on_transcription_done)
        self.transcription_thread.error_occurred.connect(self.on_transcription_error)
        self.transcription_thread.start()

    @Slot(str)
    def on_transcription_done(self, clipboard_text):
        QApplication.instance().clipboard().setText(clipboard_text)
        self.window.update_clipboard(clipboard_text)
        self.update_status_signal.emit("Audio transcribed and copied to clipboard")
        self.enable_widgets_signal.emit(True)

    @Slot(str)
    def on_transcription_error(self, error_message):
        self.update_status_signal.emit(error_message)
        self.enable_widgets_signal.emit(True)

    @Slot(str)
    def on_recording_error(self, error_message):
        self.update_status_signal.emit(error_message)
        self.enable_widgets_signal.emit(True)

    @Slot()
    def on_recording_finished(self):
        self.save_audio()

    def start_recording(self):
        if not hasattr(self, 'recording_thread') or not self.recording_thread.isRunning():
            self.recording_thread = RecordingThread(self.samplerate, self.channels, self.dtype)
            self.recording_thread.update_status_signal.connect(self.update_status_signal)
            self.recording_thread.recording_error.connect(self.on_recording_error)
            self.recording_thread.recording_finished.connect(self.on_recording_finished)
            self.recording_thread.start()
        else:
            self.update_status_signal.emit("Already recording.")

    def stop_recording(self):
        if hasattr(self, 'recording_thread') and self.recording_thread.isRunning():
            self.recording_thread.stop()
        else:
            self.update_status_signal.emit("Not currently recording.")

    def save_audio(self):
        self.enable_widgets_signal.emit(False)
        audio_data = []
        while not self.recording_thread.buffer.empty():
            audio_data.append(self.recording_thread.buffer.get())
        data = np.concatenate(audio_data)

        with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as temp_file:
            temp_filename = temp_file.name

        try:
            with wave.open(temp_filename, "wb") as wf:
                wf.setnchannels(self.channels)
                wf.setsampwidth(2)
                wf.setframerate(self.samplerate)
                wf.writeframes(data.tobytes())

            self.update_status_signal.emit("Audio saved, starting transcription...")
            self.transcribe_audio(temp_filename)
        except Exception as e:
            error_message = f"Error saving audio: {e}"
            logger.error(error_message)
            self.update_status_signal.emit(error_message)
            self.enable_widgets_signal.emit(True)

    def stop_all_threads(self):
        if hasattr(self, 'recording_thread') and self.recording_thread.isRunning():
            self.recording_thread.stop()
            self.recording_thread.wait(timeout=5000)

        if hasattr(self, 'model_loader_thread') and self.model_loader_thread.isRunning():
            self.model_loader_thread.requestInterruption()
            self.model_loader_thread.wait(timeout=5000)

        if hasattr(self, 'transcription_thread') and self.transcription_thread.isRunning():
            self.transcription_thread.requestInterruption()
            self.transcription_thread.wait(timeout=5000)
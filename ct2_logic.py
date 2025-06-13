import time
import sounddevice as sd
import numpy as np
import wave
import psutil
from PySide6.QtWidgets import QApplication
from PySide6.QtCore import QObject, Signal, Slot, QThread, QMutex, QRunnable, QThreadPool
from faster_whisper import WhisperModel
import yaml
import logging
import tempfile
from contextlib import contextmanager
from pathlib import Path
import queue
import gc
import threading

from ct2_utils import get_resource_path
import module_nltk

logger = logging.getLogger(__name__)

class _LoaderSignals(QObject):
    model_loaded = Signal(object, str, str, str)
    error_occurred = Signal(str)

class ModelLoaderRunnable(QRunnable):
    def __init__(self, model_name, quantization_type, device_type):
        super().__init__()
        self.model_name = model_name
        self.quantization_type = quantization_type
        self.device_type = device_type
        self.signals = _LoaderSignals()
        self.setAutoDelete(True)

    def run(self):
        try:
            if self.model_name.startswith("distil-whisper"):
                model_str = f"ctranslate2-4you/{self.model_name}-ct2-{self.quantization_type}"
            else:
                model_str = f"ctranslate2-4you/whisper-{self.model_name}-ct2-{self.quantization_type}"
            model = WhisperModel(model_str, device=self.device_type, compute_type=self.quantization_type, cpu_threads=psutil.cpu_count(logical=False))
            self.signals.model_loaded.emit(model, self.model_name, self.quantization_type, self.device_type)
        except Exception as e:
            self.signals.error_occurred.emit(f"Error loading model: {e}")

class TranscriptionThread(QThread):
    transcription_done = Signal(str)
    error_occurred = Signal(str)

    def __init__(self, model, expected_id, audio_file):
        super().__init__()
        self.model = model
        self.expected_id = expected_id
        self.audio_file = audio_file

    def run(self):
        try:
            if id(self.model) != self.expected_id or self.isInterruptionRequested():
                return
            segments, _ = self.model.transcribe(self.audio_file)
            if self.isInterruptionRequested():
                return
            self.transcription_done.emit("\n".join([s.text for s in segments]))
        except Exception as e:
            self.error_occurred.emit(f"Transcription failed: {e}")
        finally:
            try:
                Path(self.audio_file).unlink(missing_ok=True)
            except OSError:
                pass

class RecordingThread(QThread):
    update_status_signal = Signal(str)
    recording_error = Signal(str)
    recording_finished = Signal()

    def __init__(self, samplerate, channels, dtype):
        super().__init__()
        self.samplerate = samplerate
        self.channels = channels
        self.dtype = dtype
        self.buffer = queue.Queue()

    @contextmanager
    def audio_stream(self):
        stream = sd.InputStream(samplerate=self.samplerate, channels=self.channels, dtype=self.dtype, callback=self.audio_callback)
        try:
            with stream:
                yield
        finally:
            stream.close()

    def audio_callback(self, indata, frames, timestamp, status):
        if status:
            logger.warning(status)
        self.buffer.put(indata.copy())

    def run(self):
        self.update_status_signal.emit("Recording.")
        try:
            with self.audio_stream():
                gate = threading.Event()
                while not self.isInterruptionRequested():
                    gate.wait(timeout=1.0)
        except Exception as e:
            self.recording_error.emit(f"Recording error: {e}")
        finally:
            self.recording_finished.emit()

    def stop(self):
        self.requestInterruption()

class VoiceRecorder(QObject):
    update_status_signal = Signal(str)
    enable_widgets_signal = Signal(bool)

    def __init__(self, window, samplerate=44100, channels=1, dtype="int16"):
        super().__init__()
        self.samplerate = samplerate
        self.channels = channels
        self.dtype = dtype
        self.window = window
        self.model = None
        self.model_mutex = QMutex()
        self.thread_pool = QThreadPool.globalInstance()
        self.load_settings()

    def load_settings(self):
        config_path = Path(get_resource_path("config.yaml"))
        try:
            with config_path.open("r") as f:
                c = yaml.safe_load(f) or {}
            self.update_model(c.get("model_name", "base.en"), c.get("quantization_type", "int8"), c.get("device_type", "cpu"))
        except FileNotFoundError:
            self.update_model("base.en", "int8", "cpu")

    def save_settings(self, model_name, quantization_type, device_type):
        config_path = Path(get_resource_path("config.yaml"))
        try:
            with config_path.open("r") as f:
                c = yaml.safe_load(f) or {}
        except FileNotFoundError:
            c = {}
        c.update({"model_name": model_name, "quantization_type": quantization_type, "device_type": device_type})
        with config_path.open("w") as f:
            yaml.safe_dump(c, f)

    def update_model(self, model_name, quantization_type, device_type):
        self.enable_widgets_signal.emit(False)
        self.update_status_signal.emit(f"Updating model to {model_name}.")
        runnable = ModelLoaderRunnable(model_name, quantization_type, device_type)
        runnable.signals.model_loaded.connect(self.on_model_loaded)
        runnable.signals.error_occurred.connect(self.on_model_load_error)
        self.thread_pool.start(runnable)

    @Slot(object, str, str, str)
    def on_model_loaded(self, model, model_name, quantization_type, device_type):
        self.model_mutex.lock()
        if self.model is not None:
            del self.model
            gc.collect()
        self.model = model
        self.model_mutex.unlock()
        self.save_settings(model_name, quantization_type, device_type)
        self.update_status_signal.emit(f"Model updated to {model_name} on {device_type}")
        self.enable_widgets_signal.emit(True)

    @Slot(str)
    def on_model_load_error(self, msg):
        self.update_status_signal.emit(msg)
        self.enable_widgets_signal.emit(True)

    def transcribe_audio(self, audio_file):
        self.update_status_signal.emit("Transcribing audio.")
        self.model_mutex.lock()
        if self.model is None:
            self.model_mutex.unlock()
            self.update_status_signal.emit("No model loaded.")
            self.enable_widgets_signal.emit(True)
            return
        model = self.model
        expected_id = id(model)
        self.model_mutex.unlock()
        self.transcription_thread = TranscriptionThread(model, expected_id, audio_file)
        self.transcription_thread.transcription_done.connect(self.on_transcription_done)
        self.transcription_thread.error_occurred.connect(self.on_transcription_error)
        self.transcription_thread.start()

    @Slot(str)
    def on_transcription_done(self, text):
        if hasattr(self.window, "curate_checkbox") and self.window.curate_checkbox.isChecked():
            text = module_nltk.curate_text(text)

        text = '\n'.join(line.lstrip(' ') for line in text.splitlines())

        QApplication.instance().clipboard().setText(text)
        if hasattr(self.window, "update_clipboard"):
            self.window.update_clipboard(text)
        self.update_status_signal.emit("Audio transcribed and copied to clipboard")
        self.enable_widgets_signal.emit(True)

    @Slot(str)
    def on_transcription_error(self, msg):
        self.update_status_signal.emit(msg)
        self.enable_widgets_signal.emit(True)

    @Slot(str)
    def on_recording_error(self, msg):
        self.update_status_signal.emit(msg)
        self.enable_widgets_signal.emit(True)

    @Slot()
    def on_recording_finished(self):
        self.save_audio()

    def start_recording(self):
        if not hasattr(self, "recording_thread") or not self.recording_thread.isRunning():
            self.recording_thread = RecordingThread(self.samplerate, self.channels, self.dtype)
            self.recording_thread.update_status_signal.connect(self.update_status_signal)
            self.recording_thread.recording_error.connect(self.on_recording_error)
            self.recording_thread.recording_finished.connect(self.on_recording_finished)
            self.recording_thread.start()
        else:
            self.update_status_signal.emit("Already recording.")

    def stop_recording(self):
        if hasattr(self, "recording_thread") and self.recording_thread.isRunning():
            self.recording_thread.stop()
        else:
            self.update_status_signal.emit("Not currently recording.")

    def _samplewidth_from_dtype(self):
        return {"int16": 2, "int32": 4, "float32": 4}.get(self.dtype, 2)

    def save_audio(self):
        self.enable_widgets_signal.emit(False)
        with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as tf:
            fname = tf.name
        try:
            with wave.open(fname, "wb") as wf:
                wf.setnchannels(self.channels)
                wf.setsampwidth(self._samplewidth_from_dtype())
                wf.setframerate(self.samplerate)
                while not self.recording_thread.buffer.empty():
                    wf.writeframes(self.recording_thread.buffer.get().tobytes())
            self.update_status_signal.emit("Audio saved, starting transcription.")
            self.transcribe_audio(fname)
        except Exception as e:
            self.update_status_signal.emit(f"Error saving audio: {e}")
            self.enable_widgets_signal.emit(True)

    def stop_all_threads(self):
        if hasattr(self, "recording_thread") and self.recording_thread.isRunning():
            self.recording_thread.stop()
            self.recording_thread.wait()
        if hasattr(self, "transcription_thread") and self.transcription_thread.isRunning():
            self.transcription_thread.requestInterruption()
            self.transcription_thread.wait()

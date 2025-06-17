# core/audio/manager.py
from typing import Optional
from pathlib import Path
import tempfile
import wave
from PySide6.QtCore import QObject, Signal, Slot
from .recording import RecordingThread

class AudioManager(QObject):
    recording_started = Signal()
    recording_stopped = Signal()
    audio_ready = Signal(str)  # file path
    audio_error = Signal(str)
    
    def __init__(self, samplerate: int = 44_100, channels: int = 1, dtype: str = "int16"):
        super().__init__()
        self.samplerate = samplerate
        self.channels = channels
        self.dtype = dtype
        self._recording_thread: Optional[RecordingThread] = None
    
    def start_recording(self) -> bool:
        """Start audio recording."""
        if self._recording_thread and self._recording_thread.isRunning():
            return False
            
        self._recording_thread = RecordingThread(
            self.samplerate, self.channels, self.dtype
        )
        self._recording_thread.recording_error.connect(self.audio_error)
        self._recording_thread.recording_finished.connect(self._on_recording_finished)
        self._recording_thread.start()
        self.recording_started.emit()
        return True
    
    def stop_recording(self) -> None:
        """Stop audio recording."""
        if self._recording_thread and self._recording_thread.isRunning():
            self._recording_thread.stop()
            self.recording_stopped.emit()
    
    @Slot()
    def _on_recording_finished(self) -> None:
        """Handle recording completion and save to file."""
        try:
            audio_file = self._save_recording_to_file()
            self.audio_ready.emit(str(audio_file))
        except Exception as e:
            self.audio_error.emit(f"Failed to save audio: {e}")
    
    def _save_recording_to_file(self) -> Path:
        """Save recorded audio to temporary WAV file."""
        with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as tf:
            path = Path(tf.name)
        
        with wave.open(str(path), "wb") as wf:
            wf.setnchannels(self.channels)
            wf.setsampwidth(self._sample_width())
            wf.setframerate(self.samplerate)
            while not self._recording_thread.buffer.empty():
                wf.writeframes(self._recording_thread.buffer.get().tobytes())
        
        return path
    
    def _sample_width(self) -> int:
        return {"int16": 2, "int32": 4, "float32": 4}.get(self.dtype, 2)
    
    def cleanup(self) -> None:
        """Clean up audio resources."""
        if self._recording_thread and self._recording_thread.isRunning():
            self._recording_thread.stop()
            self._recording_thread.wait()
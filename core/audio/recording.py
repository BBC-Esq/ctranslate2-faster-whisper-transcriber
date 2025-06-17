"""
Audio-capture thread and tiny WAV helpers.

Placed in: myapp/core/audio/recording.py
"""
from __future__ import annotations

import logging
import queue
import tempfile
import threading
import wave
from contextlib import contextmanager
from pathlib import Path
from typing import Iterator

import sounddevice as sd
from PySide6.QtCore import QThread, Signal


logger = logging.getLogger(__name__)


class RecordingThread(QThread):

    update_status_signal = Signal(str)
    recording_error = Signal(str)
    recording_finished = Signal()

    def __init__(self, samplerate: int = 44_100, channels: int = 1, dtype: str = "int16") -> None:
        super().__init__()
        self.samplerate = samplerate
        self.channels = channels
        self.dtype = dtype
        self.buffer: queue.Queue = queue.Queue()

    @contextmanager
    def _audio_stream(self) -> Iterator[None]:
        stream = sd.InputStream(
            samplerate=self.samplerate,
            channels=self.channels,
            dtype=self.dtype,
            callback=self._audio_callback,
        )
        try:
            with stream:
                yield
        finally:
            stream.close()

    def _audio_callback(self, indata, frames, timestamp, status) -> None:  # noqa: D401, N802
        if status:
            logger.warning(status)
        self.buffer.put(indata.copy())

    def run(self) -> None:  # noqa: D401
        self.update_status_signal.emit("Recording.")
        try:
            with self._audio_stream():
                gate = threading.Event()
                while not self.isInterruptionRequested():
                    gate.wait(timeout=1.0)
        except Exception as exc:  # pragma: no cover
            self.recording_error.emit(f"Recording error: {exc}")
        finally:
            self.recording_finished.emit()

    def stop(self) -> None:
        self.requestInterruption()

    @staticmethod
    def _sample_width_from_dtype(dtype: str) -> int:
        return {"int16": 2, "int32": 4, "float32": 4}.get(dtype, 2)

    def dump_to_wav(self, outfile: str | Path) -> Path:

        outfile = Path(outfile)
        with wave.open(str(outfile), "wb") as wf:
            wf.setnchannels(self.channels)
            wf.setsampwidth(self._sample_width_from_dtype(self.dtype))
            wf.setframerate(self.samplerate)

            while not self.buffer.empty():
                wf.writeframes(self.buffer.get().tobytes())
        return outfile

    def dump_to_temp_wav(self) -> Path:

        tmp = tempfile.NamedTemporaryFile(suffix=".wav", delete=False)
        tmp.close()
        return self.dump_to_wav(tmp.name)

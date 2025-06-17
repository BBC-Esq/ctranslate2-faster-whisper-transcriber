"""
Model loading utilities.
"""
from __future__ import annotations

import logging
from typing import Optional

import psutil
from faster_whisper import WhisperModel

logger = logging.getLogger(__name__)

def _make_repo_string(model_name: str, quantization_type: str) -> str:
    if model_name.startswith("distil-whisper"):
        return f"ctranslate2-4you/{model_name}-ct2-{quantization_type}"
    return f"ctranslate2-4you/whisper-{model_name}-ct2-{quantization_type}"

def load_model(
    model_name: str,
    quantization_type: str = "float32",
    device_type: str = "cpu",
    cpu_threads: Optional[int] = None,
) -> WhisperModel:

    repo = _make_repo_string(model_name, quantization_type)
    logger.info("Loading Whisper model %s on %s …", repo, device_type)

    if cpu_threads is None:
        cpu_threads = psutil.cpu_count(logical=False) or 1

    try:
        model = WhisperModel(
            repo,
            device=device_type,
            compute_type=quantization_type,
            cpu_threads=cpu_threads,
        )
    except Exception as exc:
        logger.exception("Failed to load model %s", repo)
        raise RuntimeError(f"Error loading model {repo}: {exc}") from exc

    logger.info("Model %s ready", repo)
    return model


class ModelLoader:

    def __init__(
        self,
        model_name: str,
        quantization_type: str = "int8",
        device_type: str = "cpu",
        cpu_threads: Optional[int] = None,
    ) -> None:
        self.model_name = model_name
        self.quantization_type = quantization_type
        self.device_type = device_type
        self.cpu_threads = cpu_threads

    def __call__(self) -> WhisperModel:
        return load_model(
            self.model_name,
            self.quantization_type,
            self.device_type,
            self.cpu_threads,
        )

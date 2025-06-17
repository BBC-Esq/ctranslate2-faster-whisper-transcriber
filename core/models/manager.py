# core/models/manager.py
from typing import Optional
from PySide6.QtCore import QObject, Signal, QMutex, QRunnable, QThreadPool
import gc
from .loader import load_model

class _LoaderSignals(QObject):
    model_loaded = Signal(object, str, str, str)  # model, model_name, quant, device
    error_occurred = Signal(str)

class _ModelLoaderRunnable(QRunnable):
    def __init__(self, model_name: str, quant_type: str, device: str) -> None:
        super().__init__()
        self.setAutoDelete(True)
        self.model_name = model_name
        self.quant_type = quant_type
        self.device = device
        self.signals = _LoaderSignals()

    def run(self) -> None:
        try:
            model = load_model(self.model_name, self.quant_type, self.device)
            self.signals.model_loaded.emit(
                model, self.model_name, self.quant_type, self.device
            )
        except Exception as exc:
            self.signals.error_occurred.emit(str(exc))

class ModelManager(QObject):
    model_loaded = Signal(str, str, str)  # name, quant, device
    model_error = Signal(str)
    
    def __init__(self):
        super().__init__()
        self._model = None
        self._model_mutex = QMutex()
        self._thread_pool = QThreadPool.globalInstance()
        self._current_settings = {}
    
    def load_model(self, model_name: str, quant: str, device: str) -> None:
        """Load a new model asynchronously."""
        runnable = _ModelLoaderRunnable(model_name, quant, device)
        runnable.signals.model_loaded.connect(self._on_model_loaded)
        runnable.signals.error_occurred.connect(self._on_model_error)
        self._thread_pool.start(runnable)
    
    def get_model(self):
        """Thread-safe model access."""
        self._model_mutex.lock()
        model = self._model
        expected_id = id(model) if model else None
        self._model_mutex.unlock()
        return model, expected_id
    
    def _on_model_loaded(self, model, name: str, quant: str, device: str) -> None:
        self._model_mutex.lock()
        if self._model is not None:
            del self._model
            gc.collect()
        self._model = model
        self._model_mutex.unlock()
        
        self._current_settings = {
            "model_name": name,
            "quantization_type": quant, 
            "device_type": device
        }
        self.model_loaded.emit(name, quant, device)
    
    def _on_model_error(self, error: str) -> None:
        self.model_error.emit(error)
    
    def cleanup(self) -> None:
        """Clean up model resources."""
        self._model_mutex.lock()
        if self._model is not None:
            del self._model
            self._model = None
        self._model_mutex.unlock()
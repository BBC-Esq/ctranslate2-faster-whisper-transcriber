import sys
import os
from pathlib import Path
import queue
from contextlib import contextmanager
import yaml
import logging

from ct2_utils import get_resource_path

logger = logging.getLogger(__name__)

def ensure_config_exists():
    config_path = Path(get_resource_path("config.yaml"))
    if not config_path.exists():
        default_config = {
            "device_type": "",
            "model_name": "",
            "quantization_type": "",
            "supported_quantizations": {
                "cpu": [],
                "cuda": []
            }
        }
        with open(config_path, "w") as f:
            yaml.safe_dump(default_config, f)
        logger.debug(f"Created default config file at: {config_path}")

ensure_config_exists()

def set_cuda_paths():
    venv_base = Path(sys.executable).parent.parent
    nvidia_base_path = venv_base / 'Lib' / 'site-packages' / 'nvidia'
    cuda_path = nvidia_base_path / 'cuda_runtime' / 'bin'
    cublas_path = nvidia_base_path / 'cublas' / 'bin'
    cudnn_path = nvidia_base_path / 'cudnn' / 'bin'
    paths_to_add = [str(cuda_path), str(cublas_path), str(cudnn_path)]
    env_vars = ['CUDA_PATH', 'PATH']

    for env_var in env_vars:
        current_value = os.environ.get(env_var, '')
        new_value = os.pathsep.join(paths_to_add + [current_value] if current_value else paths_to_add)
        os.environ[env_var] = new_value

set_cuda_paths()

from PySide6.QtWidgets import QApplication
from ct2_gui import MyWindow
from ct2_utils import CheckQuantizationSupport

if __name__ == "__main__":
    quantization_checker = CheckQuantizationSupport()
    cuda_available = quantization_checker.has_cuda_device()
    quantization_checker.update_supported_quantizations()
    app = QApplication(sys.argv)
    app.setStyle('Fusion')
    window = MyWindow(cuda_available)
    window.show()
    sys.exit(app.exec())
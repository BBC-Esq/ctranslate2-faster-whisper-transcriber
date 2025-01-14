import sys
import os
from pathlib import Path
import queue
from contextlib import contextmanager

def set_cuda_paths():
    venv_base = Path(sys.executable).parent.parent
    nvidia_base_path = venv_base / 'Lib' / 'site-packages' / 'nvidia'
    cuda_path = nvidia_base_path / 'cuda_runtime' / 'bin'
    cublas_path = nvidia_base_path / 'cublas' / 'bin'
    cudnn_path = nvidia_base_path / 'cudnn' / 'bin'
    paths_to_add = [str(cuda_path), str(cublas_path), str(cudnn_path)]
    env_vars = ['CUDA_PATH', 'CUDA_PATH_V12_1', 'PATH']

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
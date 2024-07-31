import sys
import os
import glob
from pathlib import Path

def set_cuda_paths():
    script_dir = Path(__file__).parent.resolve()
    cuda_path = script_dir / 'Lib' / 'site-packages' / 'nvidia'
    cublas_path = cuda_path / 'cublas' / 'bin'
    cudnn_path = cuda_path / 'cudnn' / 'bin'

    paths_to_add = [str(cuda_path), str(cublas_path), str(cudnn_path)]

    env_vars = ['CUDA_PATH', 'CUDA_PATH_V12_1', 'PATH']

    for env_var in env_vars:
        current_value = os.environ.get(env_var, '')
        new_value = os.pathsep.join(paths_to_add + [current_value] if current_value else paths_to_add)
        os.environ[env_var] = new_value

    # print("CUDA paths have been set or updated in the environment variables.")

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
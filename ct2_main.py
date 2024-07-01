import sys
import os
import glob
from pathlib import Path
from PySide6.QtWidgets import QApplication
from ct2_gui import MyWindow
from ct2_utils import CheckQuantizationSupport

def set_cuda_paths():
    script_dir = Path(__file__).parent.resolve()
    nvidia_base_path = script_dir / 'Lib' / 'site-packages' / 'nvidia'
    cublas_bin_path = script_dir / 'Lib' / 'site-packages' / 'nvidia' / 'cublas' / 'bin'
    cudnn_bin_path = script_dir / 'Lib' / 'site-packages' / 'nvidia' / 'cudnn' / 'bin'
    
    # Set CUDA_PATH and CUDA_PATH_V12_2
    for env_var in ['CUDA_PATH', 'CUDA_PATH_V12_2']:
        current_path = os.environ.get(env_var, '')
        new_paths = [str(nvidia_base_path), str(cublas_bin_path), str(cudnn_bin_path)]
        os.environ[env_var] = os.pathsep.join(filter(None, new_paths + [current_path]))

    # Add nvidia folder, cudnn bin folder, and cublas bin folder to system PATH
    current_path = os.environ.get('PATH', '')
    new_paths = [str(nvidia_base_path), str(cublas_bin_path), str(cudnn_bin_path)]
    new_path = os.pathsep.join(filter(None, new_paths + [current_path]))
    os.environ['PATH'] = new_path

if __name__ == "__main__":
    set_cuda_paths()
    
    quantization_checker = CheckQuantizationSupport()
    cuda_available = quantization_checker.has_cuda_device()
    quantization_checker.update_supported_quantizations()
    
    app = QApplication(sys.argv)
    app.setStyle('Fusion')
    window = MyWindow(cuda_available)
    window.show()
    sys.exit(app.exec())
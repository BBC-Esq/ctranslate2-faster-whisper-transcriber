import sys
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
"""
Application entry-point.
"""
from __future__ import annotations

import warnings

warnings.filterwarnings(
    "ignore",
    category=UserWarning,
    message=r".*pkg_resources is deprecated as an API.*"
)

import sys
import signal

from PySide6.QtWidgets import QApplication

from gui.main_window import MainWindow

def _install_sigint_handler() -> None:
    signal.signal(signal.SIGINT, signal.SIG_DFL)

def run_gui() -> None:
    app = QApplication(sys.argv)
    app.setStyle('Fusion')
    _install_sigint_handler()

    cuda_ok = False
    try:
        import torch
        cuda_ok = torch.cuda.is_available()
    except ImportError:
        pass

    window = MainWindow(cuda_available=cuda_ok)
    window.show()

    sys.exit(app.exec())

def main() -> None:
    run_gui()

if __name__ == "__main__":
    main()
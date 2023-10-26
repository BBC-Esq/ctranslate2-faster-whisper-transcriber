import sys
from PySide6.QtWidgets import QApplication
from ct2_gui import MyWindow

if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyle('Fusion')
    window = MyWindow()
    window.show()
    sys.exit(app.exec())

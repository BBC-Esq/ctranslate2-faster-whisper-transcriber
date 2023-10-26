from PySide6.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QLabel, QComboBox, QHBoxLayout, QGroupBox
from PySide6.QtCore import Qt
from ct2_logic import VoiceRecorder

class MyWindow(QWidget):
    def __init__(self):
        super().__init__()

        layout = QVBoxLayout(self)

        self.status_label = QLabel('', self)
        layout.addWidget(self.status_label)

        self.recorder = VoiceRecorder(self)

        for text, callback in [("Record", self.recorder.start_recording),
                               ("Stop and Copy to Clipboard", self.recorder.save_audio)]:
            button = QPushButton(text, self)
            button.clicked.connect(callback)
            layout.addWidget(button)

        settings_group = QGroupBox("Settings")
        settings_layout = QVBoxLayout()

        # Model, Quantization, and Device dropdowns
        h_layout = QHBoxLayout()

        model_label = QLabel('Model')
        h_layout.addWidget(model_label)
        self.model_dropdown = QComboBox(self)
        self.model_dropdown.addItems(["tiny", "tiny.en", "base", "base.en", "small", "small.en", "medium", "medium.en", "large-v2"])
        h_layout.addWidget(self.model_dropdown)
        self.model_dropdown.setCurrentText("base.en")

        quantization_label = QLabel('Quantization')
        h_layout.addWidget(quantization_label)
        self.quantization_dropdown = QComboBox(self)
        self.quantization_dropdown.addItems(["int8", "int8_float32", "int8_float16", "int8_bfloat16", "float16", "bfloat16", "float32"])
        h_layout.addWidget(self.quantization_dropdown)
        self.quantization_dropdown.setCurrentText("float32")

        device_label = QLabel('Device')
        h_layout.addWidget(device_label)
        self.device_dropdown = QComboBox(self)
        self.device_dropdown.addItems(["auto", "cpu", "cuda"])
        h_layout.addWidget(self.device_dropdown)
        self.device_dropdown.setCurrentText("auto")

        settings_layout.addLayout(h_layout)

        # Update Model button
        update_model_btn = QPushButton("Update Settings", self)
        update_model_btn.clicked.connect(self.update_model)
        settings_layout.addWidget(update_model_btn)

        settings_group.setLayout(settings_layout)
        layout.addWidget(settings_group)

        self.setFixedSize(425, 250)
        self.setWindowFlag(Qt.WindowStaysOnTopHint)

    def update_model(self):
        self.recorder.update_model(self.model_dropdown.currentText(), self.quantization_dropdown.currentText(), self.device_dropdown.currentText())

    def update_status(self, text):
        self.status_label.setText(text)

if __name__ == "__main__":
    app = QApplication([])
    window = MyWindow()
    window.show()
    app.exec()

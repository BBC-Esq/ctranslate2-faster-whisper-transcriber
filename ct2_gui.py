from PySide6.QtWidgets import (QApplication, QWidget, QVBoxLayout, QPushButton, 
    QLabel, QComboBox, QHBoxLayout, QGroupBox, QTextEdit)
from PySide6.QtCore import Qt
from ct2_logic import VoiceRecorder
import yaml

class ClipboardWindow(QWidget):
    def __init__(self, main_window=None):
        super().__init__()
        self.main_window = main_window
        self.setWindowTitle("Current Transcription")

        layout = QVBoxLayout(self)

        self.text_display = QTextEdit()
        self.text_display.setReadOnly(True)
        layout.addWidget(self.text_display)

        self.setWindowFlags(Qt.Window | Qt.WindowStaysOnTopHint)
        self.resize(300, self.main_window.height() if main_window else 250)
        self.hide()

    def update_text(self, text):
        self.text_display.setText(text)

    def update_history(self, text):
        current_text = self.clipboard_history.toPlainText()
        if current_text:
            self.clipboard_history.setText(f"{text}\n\n{current_text}")
        else:
            self.clipboard_history.setText(text)
            
    def showEvent(self, event):
        if self.main_window:
            main_geo = self.main_window.geometry()
            self.setGeometry(
                main_geo.x() - self.width(), 
                main_geo.y(),
                self.width(),
                main_geo.height()
            )
        super().showEvent(event)

class MyWindow(QWidget):
    def __init__(self, cuda_available=False):
        super().__init__()

        layout = QVBoxLayout(self)

        self.clipboard_window = ClipboardWindow(self)

        view_btn = QPushButton("View Clipboard History", self)
        view_btn.clicked.connect(self.toggle_clipboard)
        layout.addWidget(view_btn)

        self.status_label = QLabel('', self)
        layout.addWidget(self.status_label)

        self.recorder = VoiceRecorder(self)

        try:
            with open("config.yaml", "r") as f:
                config = yaml.safe_load(f)
                model = config.get("model_name", "base.en")
                quantization = config.get("quantization_type", "int8")
                device = config.get("device_type", "auto")
                self.supported_quantizations = config.get("supported_quantizations", {"cpu": [], "cuda": []})
        except FileNotFoundError:
            model, quantization, device = "base.en", "int8", "cpu"
            self.supported_quantizations = {"cpu": [], "cuda": []}

        self.record_button = QPushButton("Record", self)
        self.record_button.clicked.connect(self.recorder.start_recording)
        layout.addWidget(self.record_button)

        self.stop_button = QPushButton("Stop and Transcribe", self)
        self.stop_button.clicked.connect(self.recorder.stop_recording)
        layout.addWidget(self.stop_button)

        settings_group = QGroupBox("Settings")
        settings_layout = QVBoxLayout()

        h_layout = QHBoxLayout()

        model_label = QLabel('Model')
        h_layout.addWidget(model_label)
        self.model_dropdown = QComboBox(self)
        self.model_dropdown.addItems([
            "tiny", "tiny.en", "base", "base.en", "small", "small.en", "medium", "medium.en", "large-v3",
            "distil-whisper-small.en", "distil-whisper-medium.en", "distil-whisper-large-v3"
        ])
        h_layout.addWidget(self.model_dropdown)
        self.model_dropdown.setCurrentText(model)

        quantization_label = QLabel('Quantization')
        h_layout.addWidget(quantization_label)
        self.quantization_dropdown = QComboBox(self)
        h_layout.addWidget(self.quantization_dropdown)

        device_label = QLabel('Device')
        h_layout.addWidget(device_label)
        self.device_dropdown = QComboBox(self)

        if cuda_available:
            self.device_dropdown.addItems(["cpu", "cuda"])
        else:
            self.device_dropdown.addItems(["cpu"])

        h_layout.addWidget(self.device_dropdown)
        self.device_dropdown.setCurrentText(device)

        settings_layout.addLayout(h_layout)

        self.update_model_btn = QPushButton("Update Settings", self)
        self.update_model_btn.clicked.connect(self.update_model)
        settings_layout.addWidget(self.update_model_btn)

        settings_group.setLayout(settings_layout)
        layout.addWidget(settings_group)

        self.setFixedSize(425, 250)
        self.setWindowFlag(Qt.WindowStaysOnTopHint)

        self.device_dropdown.currentTextChanged.connect(self.update_quantization_options)
        self.model_dropdown.currentTextChanged.connect(self.update_quantization_options)
        self.update_quantization_options()

        self.recorder.update_status_signal.connect(self.update_status)
        self.recorder.enable_widgets_signal.connect(self.set_widgets_enabled)

    def toggle_clipboard(self):
        if self.clipboard_window.isVisible():
            self.clipboard_window.hide()
        else:
            self.clipboard_window.show()

    def update_clipboard(self, text):
        self.clipboard_window.update_text(text)

    def update_quantization_options(self):
        model = self.model_dropdown.currentText()
        device = self.device_dropdown.currentText()
        self.quantization_dropdown.clear()
        options = self.get_quantization_options(model, device)
        self.quantization_dropdown.addItems(options)
        if self.quantization_dropdown.currentText() not in options and options:
            self.quantization_dropdown.setCurrentText(options[0])

    def get_quantization_options(self, model, device):
        distil_models = {
            "distil-whisper-small.en": ["float16", "bfloat16", "float32"],
            "distil-whisper-medium.en": ["float16", "bfloat16", "float32"],
            "distil-whisper-large-v2": ["float16", "float32"],
            "distil-whisper-large-v3": ["float16", "bfloat16", "float32"]
        }
        if model in distil_models:
            return distil_models[model]
        else:
            return self.supported_quantizations.get(device, [])

    def update_model(self):
        model_name = self.model_dropdown.currentText()
        quantization = self.quantization_dropdown.currentText()
        device = self.device_dropdown.currentText()
        self.recorder.update_model(model_name, quantization, device)

    def update_status(self, text):
        self.status_label.setText(text)

    def set_widgets_enabled(self, enabled):
        self.record_button.setEnabled(enabled)
        self.stop_button.setEnabled(enabled)
        self.model_dropdown.setEnabled(enabled)
        self.quantization_dropdown.setEnabled(enabled)
        self.device_dropdown.setEnabled(enabled)
        self.update_model_btn.setEnabled(enabled)

    def moveEvent(self, event):
        if self.clipboard_window.isVisible():
            self.clipboard_window.move(
                self.x() - self.clipboard_window.width(),
                self.y()
            )
        super().moveEvent(event)

    def closeEvent(self, event):
        self.clipboard_window.close()
        if hasattr(self, 'recorder'):
            self.recorder.stop_all_threads()
        super().closeEvent(event)
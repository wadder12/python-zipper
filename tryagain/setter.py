from PyQt6.QtWidgets import QDialog, QVBoxLayout, QLabel, QLineEdit, QComboBox, QSpinBox

class SettingsDialog(QDialog):

    def __init__(self, parent=None):
        super().__init__(parent)
        self.label_default_dir = QLabel("Default Extraction Directory:", self)
        self.default_dir_input = QLineEdit(self)
        self.label_theme = QLabel("Theme:", self)
        self.theme_selector = QComboBox(self)
        self.theme_selector.addItems(["Light", "Dark"])
        self.label_history = QLabel("Max History Items:", self)
        self.history_spinbox = QSpinBox(self)
        self.history_spinbox.setRange(1, 1000)
        self.history_spinbox.setValue(100)
        layout = QVBoxLayout()
        layout.addWidget(self.label_default_dir)
        layout.addWidget(self.default_dir_input)
        layout.addWidget(self.label_theme)
        layout.addWidget(self.theme_selector)
        layout.addWidget(self.label_history)
        layout.addWidget(self.history_spinbox)
        self.setLayout(layout)
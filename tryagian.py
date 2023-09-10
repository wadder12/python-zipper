import sys
import os
from pyunpack import Archive
import zipfile
import tarfile
from moviepy.editor import VideoFileClip
from PyQt6.QtWidgets import (QApplication, QMainWindow, QPushButton, QVBoxLayout, 
                             QFileDialog, QWidget, QProgressBar, QTextEdit, 
                             QDialog, QLabel, QLineEdit, QComboBox, QSpinBox)

from zipfile import ZIP_STORED, ZIP_DEFLATED, ZIP_BZIP2, ZIP_LZMA

import requests

class SettingsDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        layout = QVBoxLayout()
        self.label_default_dir = QLabel("Default Extraction Directory:", self)
        self.default_dir_input = QLineEdit(self)
        self.label_theme = QLabel("Theme:", self)
        self.theme_selector = QComboBox(self)
        self.theme_selector.addItems(["Light", "Dark"])
        self.label_history = QLabel("Max History Items:", self)
        self.history_spinbox = QSpinBox(self)
        self.history_spinbox.setRange(1, 1000)
        self.history_spinbox.setValue(100)
        self.copyright_label = QLabel("© 2023 UNZIPIT. All rights reserved.", self)
        self.version_label = QLabel("Version 1.0.0", self)
        layout.addWidget(self.label_default_dir)
        layout.addWidget(self.default_dir_input)
        layout.addWidget(self.label_theme)
        layout.addWidget(self.theme_selector)
        layout.addWidget(self.label_history)
        layout.addWidget(self.history_spinbox)
        layout.addWidget(self.copyright_label)
        layout.addWidget(self.version_label)
        self.setLayout(layout)

class MyApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()
        self.browse_btn = QPushButton("Browse Files", self)
        self.browse_btn.clicked.connect(self.browseFiles)
        self.convert_btn = QPushButton("Convert Files", self)
        self.convert_btn.clicked.connect(self.convertFile)
        self.unzip_btn = QPushButton("Unzip", self)
        self.unzip_btn.clicked.connect(self.unzipFile)
        self.zip_btn = QPushButton("Zip", self)
        self.zip_btn.clicked.connect(self.zipFile)
        self.settings_btn = QPushButton("Settings", self)
        self.settings_btn.clicked.connect(self.openSettings)
        self.progress_bar = QProgressBar(self)
        self.history = QTextEdit(self)
        self.history.setReadOnly(True)

        # Compression Level Selector
        self.compression_label = QLabel("Compression Level:", self)
        self.compression_selector = QComboBox(self)
        self.compression_selector.addItems(["No Compression", "Fastest", "Balanced", "Smallest"])

        layout.addWidget(self.browse_btn)
        layout.addWidget(self.convert_btn)
        layout.addWidget(self.zip_btn)
        layout.addWidget(self.unzip_btn)
        layout.addWidget(self.compression_label)
        layout.addWidget(self.compression_selector)
        layout.addWidget(self.progress_bar)
        layout.addWidget(self.settings_btn)
        layout.addWidget(self.history)

        central_widget = QWidget(self)
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

        self.setGeometry(100, 100, 500, 400)
        self.setWindowTitle('UNZIPIT')
        self.show()

        self.settings = SettingsDialog(self)
        self.settings.theme_selector.currentTextChanged.connect(self.changeTheme)

    def check_for_updates(self):
        current_version = "1.0.0"  # This should be your app's current version. Update this whenever you release a new version.
        latest_version = self.get_latest_version_from_github()

        if latest_version and latest_version != current_version:
            # Logic to notify the user about the update
            self.history.append(f"New update available! Current version: {current_version}, Latest version: {latest_version}")
            # Optionally: Provide a link/button to download and install the update.

    def get_latest_version_from_github(self):
        repo_url = "https://api.github.com/repos/wadder12/python-zipper/releases/latest"
        try:
            response = requests.get(repo_url)
            response.raise_for_status()  # Raise an exception for HTTP errors
            data = response.json()
            if "tag_name" in data:
                return data["tag_name"]  # This assumes you use tag names for version numbers.
            return None
        except requests.RequestException as e:
            self.history.append(f"Error checking for updates: {str(e)}")
            return None

    def browseFiles(self):
        files, _ = QFileDialog.getOpenFileNames(self, "Select Files")
        if files:
            self.selected_files = files
            self.history.append(f"Selected files: {', '.join(files)}")

    def unzipFile(self):
        if hasattr(self, 'selected_files'):
            for file in self.selected_files:
                try:
                    if file.endswith((".zip", ".rar", ".7z", ".tar")):
                        self._extract_file(file)
                except Exception as e:
                    self.history.append(f"Error unzipping {file}: {str(e)}")

    def zipFile(self):
        if hasattr(self, 'selected_files'):
            output_file, _ = QFileDialog.getSaveFileName(self, "Save Archive File", filter="Zip Files (*.zip);;Tar Files (*.tar)")
            if output_file:
                try:
                    if output_file.endswith(".zip"):
                        self._zip_files(output_file)
                    elif output_file.endswith(".tar"):
                        self._tar_files(output_file)
                except Exception as e:
                    self.history.append(f"Error archiving files to {output_file}: {str(e)}")

    def _extract_file(self, file):
        Archive(file).extractall('.')
        self.history.append(f"Successfully extracted {file}")

    def convertFile(self):
        if hasattr(self, 'selected_files'):
            for file in self.selected_files:
                if file.endswith('.mp4'):
                    output_gif = os.path.splitext(file)[0] + '.gif'
                    clip = VideoFileClip(file)
                    clip.write_gif(output_gif)
                    self.history.append(f"Converted {file} to {output_gif}")

    def openSettings(self):
        self.settings.exec()

    def changeTheme(self, theme):
        if theme == "Dark":
            self.setStyleSheet(dark_stylesheet)
        else:
            self.setStyleSheet(light_stylesheet)

    def _zip_files(self, output_file):
        compression_modes = {
            "No Compression": ZIP_STORED,
            "Fastest": ZIP_DEFLATED,
            "Balanced": ZIP_BZIP2,
            "Smallest": ZIP_LZMA
        }
        mode = compression_modes[self.compression_selector.currentText()]
        with zipfile.ZipFile(output_file, 'w', compression=mode) as zip_ref:
            for file in self.selected_files:
                zip_ref.write(file)
            self.history.append(f"Successfully zipped files to {output_file}")

    def _tar_files(self, output_file):
        with tarfile.open(output_file, 'w') as tar_ref:
            for file in self.selected_files:
                tar_ref.add(file)
            self.history.append(f"Successfully archived files to {output_file}")

dark_stylesheet = """
    QMainWindow {
        background-color: #333;
    }
    QPushButton {
        background-color: #555;
        border: 2px solid #888;
        color: white;
    }
    QPushButton:hover {
        background-color: #666;
    }
    QTextEdit {
        background-color: #222;
        color: #AAA;
    }
    QProgressBar {
        border: 2px solid #888;
        text-align: center;
    }
    QProgressBar::chunk {
        background-color: #05B8CC;
    }
"""

light_stylesheet = """
    QMainWindow {
        background-color: #EEE;
    }
    QPushButton {
        background-color: #CCC;
        border: 2px solid #AAA;
        color: #333;
    }
    QPushButton:hover {
        background-color: #DDD;
    }
    QTextEdit {
        background-color: #FFF;
        color: #333;
    }
    QProgressBar {
        border: 2px solid #AAA;
        text-align: center;
    }
    QProgressBar::chunk {
        background-color: #05B8CC;
    }
"""

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyApp()
    sys.exit(app.exec())

import sys
import tarfile
import zipfile
import os
from moviepy.editor import VideoFileClip
from PyQt6.QtWidgets import (QApplication, QMainWindow, QPushButton, QVBoxLayout, 
                             QFileDialog, QWidget, QProgressBar, QTextEdit, 
                             QDialog, QLabel, QLineEdit)

class SettingsDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        layout = QVBoxLayout()

        self.label = QLabel("Default Extraction Directory:", self)
        self.default_dir_input = QLineEdit(self)

        layout.addWidget(self.label)
        layout.addWidget(self.default_dir_input)

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

        layout.addWidget(self.browse_btn)
        layout.addWidget(self.convert_btn)
        layout.addWidget(self.zip_btn)
        layout.addWidget(self.unzip_btn)
        layout.addWidget(self.progress_bar)
        layout.addWidget(self.settings_btn)
        layout.addWidget(self.history)

        central_widget = QWidget(self)
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

        self.setGeometry(100, 100, 500, 400)
        self.setWindowTitle('My Zip/Unzip App')
        self.show()

    def browseFiles(self):
        files, _ = QFileDialog.getOpenFileNames(self, "Select Files")
        if files:
            self.selected_files = files
            self.history.append(f"Selected files: {', '.join(files)}")

    def unzipFile(self):
        if hasattr(self, 'selected_files'):
            for file in self.selected_files:
                try:
                    if file.endswith(".zip"):
                        self._unzip_file(file)
                    elif file.endswith(".tar"):
                        self._untar_file(file)
                except Exception as e:
                    self.history.append(f"Error unzipping {file}: {str(e)}")

    def _unzip_file(self, file_path):
        with zipfile.ZipFile(file_path, 'r') as zip_ref:
            total_size = sum([info.file_size for info in zip_ref.infolist()])
            extracted_size = 0
            output_dir = os.path.dirname(file_path)
            for member in zip_ref.infolist():
                extracted_size += member.file_size
                self._update_progress(extracted_size, total_size)
                zip_ref.extract(member, output_dir)
            self.history.append(f"Unzipped: {file_path} to {output_dir}")

    def _untar_file(self, file_path):
        with tarfile.open(file_path, 'r') as tar_ref:
            members = tar_ref.getmembers()
            total_size = sum([info.size for info in members])
            extracted_size = 0
            output_dir = os.path.dirname(file_path)
            for member in members:
                extracted_size += member.size
                self._update_progress(extracted_size, total_size)
                tar_ref.extract(member, output_dir)
            self.history.append(f"Untarred: {file_path} to {output_dir}")

    def zipFile(self):
        if hasattr(self, 'selected_files'):
            output_file, _ = QFileDialog.getSaveFileName(self, "Save Zip File", filter="Zip Files (*.zip);;Tar Files (*.tar)")
            if output_file:
                try:
                    if output_file.endswith(".zip"):
                        self._zip_files(output_file)
                    elif output_file.endswith(".tar"):
                        self._tar_files(output_file)
                except Exception as e:
                    self.history.append(f"Error zipping files to {output_file}: {str(e)}")

    def _zip_files(self, output_file):
        with zipfile.ZipFile(output_file, 'w') as zipf:
            total_size = sum([os.path.getsize(f) for f in self.selected_files])
            zipped_size = 0
            for file in self.selected_files:
                zipped_size += os.path.getsize(file)
                self._update_progress(zipped_size, total_size)
                zipf.write(file, os.path.basename(file))
            self.history.append(f"Zipped to: {output_file}")

    def _tar_files(self, output_file):
        with tarfile.open(output_file, 'w') as tarf:
            total_size = sum([os.path.getsize(f) for f in self.selected_files])
            tarred_size = 0
            for file in self.selected_files:
                tarred_size += os.path.getsize(file)
                self._update_progress(tarred_size, total_size)
                tarf.add(file, arcname=os.path.basename(file))
            self.history.append(f"Tarred to: {output_file}")

    def _update_progress(self, current, total):
        self.progress_bar.setValue(int((current / total) * 100))

    def openSettings(self):
        dialog = SettingsDialog(self)
        dialog.exec()

    def convertFile(self):
        if hasattr(self, 'selected_files'):
            for file in self.selected_files:
                if file.endswith('.mp4'):
                    output_gif = os.path.splitext(file)[0] + '.gif'
                    clip = VideoFileClip(file)
                    clip.write_gif(output_gif)
                    self.history.append(f"Converted {file} to {output_gif}")

stylesheet = """
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

if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setStyleSheet(stylesheet)
    ex = MyApp()
    sys.exit(app.exec())

import sys
import os
import psutil
from PyQt6.QtCore import QTimer

from pyunpack import Archive
from PyQt6.QtGui import QDragEnterEvent, QDropEvent
from PyQt6.QtCore import QMimeData
from PyQt6.QtWidgets import QInputDialog
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QDragEnterEvent, QDropEvent
import zipfile
import concurrent.futures
from PyQt6.QtWidgets import QLabel
from PyQt6.QtGui import QPixmap, QPainter, QColor
from PyQt6.QtGui import QIcon
from PyQt6.QtWidgets import QLabel, QWidget, QHBoxLayout
import tarfile
from moviepy.editor import VideoFileClip
from PyQt6.QtWidgets import (QApplication, QMainWindow, QPushButton, QVBoxLayout, 
                             QFileDialog, QWidget, QProgressBar, QTextEdit, 
                             QDialog, QLabel, QLineEdit, QComboBox, QSpinBox)

from zipfile import ZIP_STORED, ZIP_DEFLATED, ZIP_BZIP2, ZIP_LZMA
import webbrowser
import requests
import shutil

current_version = "1.0.0"  # Define the current version here

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
        self.version_label = QLabel(f"Version {current_version}", self)
        self.label_socials = QLabel("Socials: FaceBook Twitter Github", self)
        self.socials_layout = QHBoxLayout()
        self.socials_layout.addSpacing(100)  # Increase spacing as needed

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
        self.selected_files = []  # Initialize the attribute
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
        self.check_update_btn = QPushButton("Check for Updates", self)
        self.check_update_btn.clicked.connect(self.check_for_updates)
        self.download_update_btn = QPushButton("Update Now", self)
        self.download_update_btn.clicked.connect(self.download_latest_version)
        self.download_update_btn.setEnabled(False)  # Start with this button disabled
        self.setAcceptDrops(True)
        self.setWindowIcon(QIcon('Designer-14.png'))
        self.batch_convert_btn = QPushButton("Batch Convert Videos", self)
        self.batch_convert_btn.clicked.connect(self.batchConvertVideos)
        layout.addWidget(self.batch_convert_btn)
        # Create a glowing green dot
        green_dot = QLabel()
        pixmap = QPixmap(16, 16)  # You can adjust the size if necessary
        pixmap.fill(QColor(0, 0, 0, 0))  # Transparent background
        painter = QPainter(pixmap)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing, True)
        painter.setBrush(QColor(0, 255, 0))
        painter.drawEllipse(3, 3, 10, 10)
        painter.end()
        green_dot.setPixmap(pixmap)
        
        # Set a stylesheet to make it appear glowing
        green_dot.setStyleSheet("""
            QLabel {
                border-radius: 8px;  # half of the pixmap size
                background-color: transparent;
                box-shadow: 0 0 5px rgba(0, 255, 0, 0.9);
            }
        """)
        
        # Combine green dot and "Ready" message in a single widget
        status_widget = QWidget()
        status_layout = QHBoxLayout()
        status_layout.addWidget(green_dot)
        status_layout.addWidget(QLabel("Ready"))
        status_layout.setContentsMargins(0, 0, 0, 0)
        status_widget.setLayout(status_layout)
        
        # Create labels for CPU and memory usage
        self.cpu_label = QLabel()
        self.memory_label = QLabel()
        
        self.statusBar().addWidget(self.cpu_label)
        self.statusBar().addWidget(self.memory_label)

        # Timer to update CPU and Memory Usage
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.updateSystemMetrics)
        self.timer.start(1000)  # every second, adjust as needed
        
        # Add combined widget to the status bar
        self.statusBar().addWidget(status_widget)
        
        

        

        

        central_widget = QWidget(self)
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)
        

        layout.addWidget(self.check_update_btn)
        layout.addWidget(self.download_update_btn)

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
        self.setWindowTitle('UNZIPIT 🚀')
        self.show()

        self.settings = SettingsDialog(self)
        self.settings.theme_selector.currentTextChanged.connect(self.changeTheme)

    def check_for_updates(self):
        current_version = "1.0.0"  # This is your app's current version. Update this when releasing a new version.
        latest_version = self.get_latest_version_from_github()

        if latest_version and latest_version != current_version:
            # Notify the user about the update
            self.history.append(f"New update available! Current version: {current_version}, Latest version: {latest_version}")
            self.download_update_btn.setEnabled(True)  # Enable the "Update Now" button
        else:
            self.history.append(f"You are running the latest version: {current_version}")

    def get_latest_version_from_github(self):
        repo_url = "https://api.github.com/repos/wadder12/python-zipper/releases/latest"
        try:
            response = requests.get(repo_url)
            response.raise_for_status()  # Raise an exception for HTTP errors
            data = response.json()
            if "tag_name" in data:
                return data["tag_name"]  # Assumes you use tag names for version numbers.
            return None
        except requests.RequestException as e:
            self.history.append(f"Error checking for updates: {str(e)}")
            return None
        
    def updateSystemMetrics(self):
        cpu_usage = psutil.cpu_percent()
        memory_info = psutil.virtual_memory()
        self.cpu_label.setText(f"CPU: {cpu_usage}%")
        self.memory_label.setText(f"Memory: {memory_info.percent}%")
        
    def someOperationMethod(self):
        # For example, before starting an operation:
        self.statusBar().showMessage('Operation started...')
        
        # ... [operation code]
        
        # After finishing the operation:
        self.statusBar().showMessage('Operation completed successfully!')
        
    
        
    def dragEnterEvent(self, event: QDragEnterEvent):
        mime_data: QMimeData = event.mimeData()
        if mime_data.hasUrls():
            event.acceptProposedAction()
            self.highlightUI(True)
            self.statusBar().showMessage('Drop files to proceed...')  # Added a status message

    def dragLeaveEvent(self, event: QDragEnterEvent):
        self.highlightUI(False)
        self.setToolTip("")  
        self.statusBar().showMessage('Ready')  # Reset status message when user drags away

    def highlightUI(self, highlight: bool):
        if highlight:
            self.setStyleSheet("background-color: rgba(0, 128, 255, 0.1);")  # Light blue highlight
            self.setToolTip("Drop files here!")  # Set tooltip when files are dragged over the application
        else:
            self.setStyleSheet("")  # Reset to the default or current theme
            
    def batchConvertVideos(self):
        files, _ = QFileDialog.getOpenFileNames(self, "Select Multiple Videos", "", "Video Files (*.mp4)")
        if files:
            self.selected_files = files
            total_files = len(self.selected_files)
            self.progress_bar.setValue(0)
            
            with concurrent.futures.ThreadPoolExecutor() as executor:
                for idx, output_gif in enumerate(executor.map(self.convertToGif, self.selected_files)):
                    self.history.append(f"Converted to {output_gif}")
                    # Calculate the percentage and update progress bar
                    progress_percentage = int((idx + 1) / total_files * 100)
                    self.progress_bar.setValue(progress_percentage)
                    


    def convertToGif(self, file):
        if file.endswith('.mp4'):
            output_gif = os.path.splitext(file)[0] + '.gif'
            clip = VideoFileClip(file)
            clip.write_gif(output_gif)
            return output_gif

    def dropEvent(self, event: QDropEvent):
        self.selected_files = []  # Clear the list for each new drop
        urls = event.mimeData().urls()
        for url in urls:
            # convert QUrl to local path
            local_path = url.toLocalFile()
            if os.path.isfile(local_path):
                self.selected_files.append(local_path)
            elif os.path.isdir(local_path):
                for root, dirs, files in os.walk(local_path):
                    for file in files:
                        self.selected_files.append(os.path.join(root, file))
        self.history.append(f"Selected files: {', '.join(self.selected_files)}")

    def download_latest_version(self):
        download_url = "https://github.com/wadder12/python-zipper/releases/latest"
        webbrowser.open(download_url)  # This will open the user's default web browser and navigate to the latest release page.

    def browseFiles(self):
        files, _ = QFileDialog.getOpenFileNames(self, "Select Files")
        if files:
            self.selected_files = files
            self.history.append(f"Selected files: {', '.join(files)}")

    def unzipFile(self):
        password, ok = QInputDialog.getText(self, 'Password Input', 'Enter the password for extraction (leave empty for no password):', QLineEdit.EchoMode.Password)
        if ok:
            if hasattr(self, 'selected_files'):
                for file in self.selected_files:
                    try:
                        if file.endswith((".zip", ".rar", ".7z", ".tar", ".pbo")):
                            self._extract_file(file, password)
                    except Exception as e:
                        self.history.append(f"Error unzipping {file}: {str(e)}")

    def zipFile(self):
        if hasattr(self, 'selected_files'):
            output_file, _ = QFileDialog.getSaveFileName(self, "Save Archive File", filter="Zip Files (*.zip);;Tar Files (*.tar)")
            password, ok = QInputDialog.getText(self, 'Password Input', 'Enter a password for the archive (leave empty for no password):', QLineEdit.EchoMode.Password)
            if ok and output_file:
                try:
                    if output_file.endswith(".zip"):
                        self._zip_files(output_file, password)
                    elif output_file.endswith(".tar"):
                        self._tar_files(output_file)
                except Exception as e:
                    self.history.append(f"Error archiving files to {output_file}: {str(e)}")

    def _extract_file(self, file, password):
        if file.endswith(".zip"):
            with zipfile.ZipFile(file, 'r') as zip_ref:
                try:
                    zip_ref.extractall('.', pwd=password.encode() if password else None)
                    self.history.append(f"Successfully extracted {file}")
                except RuntimeError as e:
                    self.history.append(f"Error extracting {file}. Incorrect password or corrupted file.")
        else:
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

    def _zip_files(self, output_file, password, chunk_size=104857600): # 104857600 bytes = 100 MB
        with zipfile.ZipFile(output_file, 'w') as zip_ref:
            for file in self.selected_files:
                zip_ref.write(file, compress_type=zipfile.ZIP_DEFLATED, pwd=password.encode() if password else None) # type: ignore
            self.history.append(f"Successfully zipped files to {output_file}")
        
        # If the file size exceeds the chunk size, split it.
        if os.path.getsize(output_file) > chunk_size:
            self._split_file(output_file, chunk_size)

    def _split_file(self, file_path, chunk_size):
        with open(file_path, 'rb') as src_file:
            part_num = 0
            while True:
                chunk = src_file.read(chunk_size)
                if not chunk:
                    break

                part_num += 1
                part_filename = f"{file_path}.part{part_num}"
                
                with open(part_filename, 'wb') as part_file:
                    part_file.write(chunk)

                self.history.append(f"Saved part {part_num} as {part_filename}")

    # Optionally, delete the original file after splitting.
        os.remove(file_path)

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


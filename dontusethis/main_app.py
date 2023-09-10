import sys
import os
from pyunpack import Archive
from PyQt6.QtGui import QDragEnterEvent, QDropEvent
from PyQt6.QtCore import QMimeData
from PyQt6.QtWidgets import QInputDialog
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QDragEnterEvent, QDropEvent
import zipfile
import concurrent.futures

from PyQt6.QtGui import QIcon

import tarfile
from moviepy.editor import VideoFileClip
from PyQt6.QtWidgets import (QApplication, QMainWindow, QPushButton, QVBoxLayout, 
                             QFileDialog, QWidget, QProgressBar, QTextEdit, 
                             QDialog, QLabel, QLineEdit, QComboBox, QSpinBox)

from zipfile import ZIP_STORED, ZIP_DEFLATED, ZIP_BZIP2, ZIP_LZMA
import webbrowser
import requests
import shutil

from settings import SettingsDialog

from constants import dark_stylesheet, light_stylesheet



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
        self.setWindowTitle('UNZIPIT')
        self.show()

        self.settings = SettingsDialog(self)
        self.settings.theme_selector.currentTextChanged.connect(self.changeTheme)
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


from utilities import get_latest_version_from_github, _zip_files, _tar_files
from constants import dark_stylesheet, light_stylesheet



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
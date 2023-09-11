import concurrent.futures
import os
import shutil
import sys
import tarfile
import webbrowser
import zipfile
from zipfile import ZIP_BZIP2, ZIP_DEFLATED, ZIP_LZMA, ZIP_STORED

import psutil
import requests
from moviepy.editor import VideoFileClip
from PyQt6.QtCore import QMimeData, QTimer
from PyQt6.QtGui import (QColor, QDragEnterEvent, QDropEvent, QFont, QIcon,
                         QPainter, QPixmap)
from PyQt6.QtWidgets import (QApplication, QComboBox, QDialog, QFileDialog,
                             QHBoxLayout, QInputDialog, QLabel, QLineEdit,
                             QMainWindow, QProgressBar, QPushButton,
                             QScrollArea, QSpinBox, QTextEdit, QVBoxLayout,
                             QWidget)
from pyunpack import Archive


class ChangelogDialog(QDialog):

    def __init__(self, parent=None):
        super().__init__(parent)
        
        self.setWindowTitle("Changelog")
        
        scroll_area = QScrollArea(self)
        scroll_content = QWidget(self)
        scroll_layout = QVBoxLayout(scroll_content)
        
        self._populate_layout(scroll_layout)
        
        scroll_area.setWidget(scroll_content)
        
        main_layout = QVBoxLayout(self)
        main_layout.addWidget(scroll_area)
    
    def _populate_layout(self, layout):
        version = "1.0.0"
        
        version_label = QLabel(f"Version {version}")
        font = QFont("Arial", 14)
        font.setBold(True)
        version_label.setFont(font)

        changes = [
            "- Initial release."
        ]
        
        for change in changes:
            layout.addWidget(QLabel(change))
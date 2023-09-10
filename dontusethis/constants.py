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
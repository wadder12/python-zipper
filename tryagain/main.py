import sys
from PyQt6.QtWidgets import QApplication

from mainwindow import MyApp
from setter import SettingsDialog
from changelogdialog import ChangelogDialog

from styles import dark_stylesheet, light_stylesheet 

from utils import get_latest_version_from_github, convertToGif


def main():
    app = QApplication(sys.argv)

    window = MyApp()
    window.show()

    sys.exit(app.exec())


if __name__ == '__main__':
    main()
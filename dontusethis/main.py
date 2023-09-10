import sys
from PyQt6.QtWidgets import QApplication
from main_app import MyApp

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyApp()
    sys.exit(app.exec())

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
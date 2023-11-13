from openpyxl import load_workbook
from app.app import MyApp
import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QVBoxLayout, QWidget, QPushButton, QFileDialog, QTextEdit, QLineEdit
from PyQt5.QtCore import Qt, QThread, pyqtSignal
from PyQt5 import QtWidgets
import os
import locale

def load_stylesheet(qss_file_path: str) -> str:
    """Load the QSS file and return the stylesheet content."""
    with open(qss_file_path, "r") as f:
        return f.read()
    
def main():
    
    locale.setlocale(locale.LC_ALL, 'fr_FR.UTF-8')
    print("Loading...")
    app = QtWidgets.QApplication(sys.argv)
    # Chargez la feuille de style
    script_dir = os.path.dirname(os.path.abspath(__file__))
    qss_file_path = os.path.join(script_dir, "theme.qss")
    stylesheet = load_stylesheet(qss_file_path)
    app.setStyleSheet(stylesheet)
    myApp = MyApp()
    sys.exit(app.exec_())
    

if __name__ == "__main__":
    main()
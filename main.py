from openpyxl import load_workbook
from app.app import MyApp
import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QVBoxLayout, QWidget, QPushButton, QFileDialog, QTextEdit, QLineEdit
from PyQt5.QtCore import Qt, QThread, pyqtSignal
from PyQt5 import QtWidgets

def load_stylesheet(qss_file_path: str) -> str:
    """Load the QSS file and return the stylesheet content."""
    with open(qss_file_path, "r") as f:
        return f.read()

if __name__ == "__main__":
    print("Loading...")
    app = QtWidgets.QApplication(sys.argv)
    # Chargez la feuille de style
    stylesheet = load_stylesheet("./theme.qss")
    app.setStyleSheet(stylesheet)
    myApp = MyApp()
    sys.exit(app.exec_())
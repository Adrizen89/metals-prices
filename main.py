
from app.app import MyApp
import sys
from PyQt5.QtWidgets import QApplication, QMessageBox, QMainWindow, QLabel, QVBoxLayout, QWidget, QPushButton, QFileDialog, QTextEdit, QLineEdit
from PyQt5.QtCore import Qt, QThread, pyqtSignal
from PyQt5 import QtWidgets
import os
import locale
import winsparkle_wrapper
from generate_appcast import generate_appcast as appcast

def load_stylesheet(qss_file_path: str) -> str:
    """Load the QSS file and return the stylesheet content."""
    with open(qss_file_path, "r") as f:
        return f.read()
    
def main():
    # Initialise WinSparkle
    winsparkle_wrapper.initialize_winsparkle("https://adrizen89.github.io/metals-prices/appcast.xml")
    
    app = QtWidgets.QApplication(sys.argv)
    locale.setlocale(locale.LC_ALL, 'fr_FR.UTF-8')
    print("Loading...")
    # Chargez la feuille de style
    script_dir = os.path.dirname(os.path.abspath(__file__))
    qss_file_path = os.path.join(script_dir, "theme.qss")
    stylesheet = load_stylesheet(qss_file_path)
    app.setStyleSheet(stylesheet)
    myApp = MyApp()
    appcast()
    sys.exit(app.exec_())
    
    # Clean WinSparkle
    winsparkle_wrapper.cleanup_winsparkle()

if __name__ == "__main__":
    main()
    
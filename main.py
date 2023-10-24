
from app.app import MyApp
import sys
from PyQt5.QtWidgets import QApplication, QMessageBox, QMainWindow, QLabel, QVBoxLayout, QWidget, QPushButton, QFileDialog, QTextEdit, QLineEdit
from PyQt5.QtCore import Qt, QThread, pyqtSignal
from PyQt5 import QtWidgets
import os
import locale
import subprocess
import json
import requests
from pathlib import Path

def resource_path(relative_path):
    """ Obtenez le chemin absolu de la ressource, fonctionne pour le dev et pour le PyInstaller """
    base_path = getattr(sys, '_MEIPASS', Path(__file__).parent)
    return Path(base_path) / relative_path

# Fonction pour obtenir la version actuelle
def get_current_version():
    with open(resource_path('version.json'), 'r') as file:
        current_version_info = json.load(file)
    return current_version_info['version']

# Fonction pour vérifier la version la plus récente
def check_latest_version():
    response = requests.get('https://raw.githubusercontent.com/Adrizen89/metals-prices/main/version.json')
    latest_version_info = response.json()
    return latest_version_info

# Fonction pour télécharger la nouvelle version
def download_latest_version(url):
    response = requests.get(url)
    with open('main.exe', 'wb') as file:
        file.write(response.content)

# Fonction pour mettre à jour la version du fichier JSON
def update_local_version_file(latest_version_info):
    with open('version.json', 'w') as file:
        json.dump(latest_version_info, file, indent=4)

# Fonction pour lancer l'installateur
def launch_installer():
    subprocess.run(['main.exe'])


def load_stylesheet(qss_file_path: str) -> str:
    """Load the QSS file and return the stylesheet content."""
    with open(qss_file_path, "r") as f:
        return f.read()

def main():
    app = QApplication(sys.argv)
    
    # Version actuelle de Metals Prices
    current_version = get_current_version()

    # Véfifier la dernière version 
    latest_version_info = check_latest_version()
    latest_version = latest_version_info['version']
    
    
    if latest_version != current_version:
        user_response = QMessageBox.question(
            None, 
            "Mise à jour disponible",
            f"Une nouvelle version ({latest_version}) est disponible. Voulez-vous mettre à jour maintenant ?",
            QMessageBox.Yes | QMessageBox.No
        )
        if user_response == QMessageBox.Yes:
            # Téléchargez la dernière version
            download_url = latest_version_info['url']
            download_latest_version(download_url)
            update_local_version_file(latest_version_info)
            
            # Lancez l'installateur
            launch_installer()
    else:
        locale.setlocale(locale.LC_ALL, 'fr_FR.UTF-8')
        print("Loading...")
        # Chargez la feuille de style
        script_dir = os.path.dirname(os.path.abspath(__file__))
        qss_file_path = os.path.join(script_dir, "theme.qss")
        stylesheet = load_stylesheet(qss_file_path)
        app.setStyleSheet(stylesheet)
        myApp = MyApp()
        sys.exit(app.exec_())
        
if __name__ == "__main__":
    main()
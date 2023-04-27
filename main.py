import requests
import os
import re
import time
from bs4 import BeautifulSoup
from openpyxl import Workbook
import openpyxl
from PyPDF2 import PdfReader
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

import path_url
import reqs

import tkinter as tk
from tkinter import filedialog
import configparser
import sys
from io import StringIO
import datetime
import mailError


now = datetime.datetime.now().date()
date = now.strftime("%d/%m/%Y")

config = configparser.ConfigParser()
config.read('config.ini')

def get_config_value(section, variable):
    config = configparser.ConfigParser()
    config.read('config.ini')
    value = config.get(section, variable)
    return value

def set_config_value(section, variable, value):
    config = configparser.ConfigParser()
    config.read('config.ini')
    config.set(section, variable, value)
    with open('config.ini', 'w') as configfile:
              config.write(configfile)

# Téléchargement des PDFs
def download_pdf(response, name, folder):
    """Télécharger un fichier PDF et l'enregistrer localement"""
    if response.status_code == 200:
        print("Connexion réussie")
        path_download = os.path.join(folder, name)
        with open(path_download, "wb") as f:
            f.write(response.content)
        print(f"Téléchargement de {name} terminé avec succès à l'endroit {path_download}")
    else:
        print(f"Erreur lors du téléchargement de {name}")

# Récupérer les accès aux sites
def get_soup(response):
    """Récupérer le soup à partir de la réponse HTTP"""
    if response.status_code == 200:
        print("Connexion réussie")
        return BeautifulSoup(response.content, "html.parser")
    else:
        print("Erreur lors de la récupération du contenu HTML")


# Suppression des PDFs
def delete_pdfs(path_pdf, name_materion):
    """Supprimer deux fichiers PDF"""
    path_materion = f"{path_pdf}/{name_materion}"
    try:
        os.remove(path_materion)
        print("Suppression des fichiers PDF terminée avec succès")
    except FileNotFoundError:
        print("Erreur : au moins un des fichiers PDF n'existe pas")
    except Exception as e:
        print(f"Une erreur s'est produite : {e}")

# Ecran d'affichage liste des liens
class FileFrame(tk.Frame):
    def __init__(self, parent, file_path):
        tk.Frame.__init__(self, parent, width=300, height=200)
        self.pack_propagate(False)  # empêche la Frame de se redimensionner automatiquement
        self.canvas = tk.Canvas(self, width=300, height=200)
        self.scrollbar = tk.Scrollbar(self, orient="vertical", command=self.canvas.yview)
        self.scrollable_frame = tk.Frame(self.canvas)

        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(
                scrollregion=self.canvas.bbox("all")
            )
        )

        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")

        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        self.canvas.pack(side="left", fill="both", expand=True)
        self.scrollbar.pack(side="right", fill="y")

        with open(file_path, "r") as f:
            data = f.readlines()
        for line in data:
            if line.startswith("url_"):
                data_label = tk.Label(self.scrollable_frame, text=line)
                data_label.pack(side= tk.TOP, fill="x")


class MyApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.geometry("800x450")
        self.title("Cours des métaux")
        self.resizable(False, False)

        # Création frame pour chemins d'accès
        left_frame = tk.Frame(self)
        right_frame = tk.Frame(self)
        excel_frame = tk.Frame(left_frame)
        pdf_frame = tk.Frame(left_frame)

        self.output_text = tk.Text(right_frame, bg='white', state='disabled', width=50)
        self.output_text.pack(side='top', fill='both', expand=True)

        self.excel_path = get_config_value("main", "excel_path")
        self.pdf_path = get_config_value("main", "pdf_path")


        # Création des éléments de la fenêtre
        title_label = tk.Label(self, text="Diehl Augé Découpage", font=("Inter", 32))
        launch_button = tk.Button(left_frame, text="Lancer", command=lambda: self.lancer_script(), width=10, height=1, bg="grey", fg="white", font=('Inter', 16))

        excel_label = tk.Label(excel_frame, text="Fichier Excel :")
        self.excel_label = tk.Label(excel_frame, text=self.excel_path)
        excel_button = tk.Button(excel_frame, text="Parcourir...", command=self.choose_excelfile)

        pdf_label = tk.Label(pdf_frame, text="Fichier PDF :")
        self.pdf_label = tk.Label(pdf_frame, text=self.pdf_path)
        pdf_button = tk.Button(pdf_frame, text="Parcourir...", command=self.choose_pdffile)

        # file_frame = FileFrame(right_frame, "path_url.py")

        # Placement des éléments dans la fenêtre
        title_label.pack(side=tk.TOP, padx=10, pady=10)
        launch_button.pack(side=tk.BOTTOM, padx=10,pady=10)

        right_frame.pack(side=tk.RIGHT, padx=10, pady=10)
        excel_frame.pack(side=tk.TOP, padx=10, pady=10)
        pdf_frame.pack(side=tk.TOP, padx=10, pady=10)
        left_frame.pack(side=tk.LEFT, padx=10, pady=10)
        # file_frame.pack(side=tk.TOP, fill="both", expand=True)

        excel_label.pack(side=tk.TOP, padx=10, pady=10)
        self.excel_label.pack(side=tk.TOP, padx=10, pady=5)
        excel_button.pack(side=tk.BOTTOM, padx=10, pady=5)

        pdf_label.pack(side=tk.TOP, padx=10, pady=10)
        self.pdf_label.pack(side=tk.TOP, padx=10, pady=5)
        pdf_button.pack(side=tk.BOTTOM, padx=10, pady=5)

        # sauvegarde automatique du chemin d'accès lors de la fermeture de l'application
        self.protocol("WM_DELETE_WINDOW", self.save_config)

    def update_output(self, text):
        self.output_text.configure(state="normal")
        self.output_text.insert(tk.END, text + "\n")
        self.output_text.configure(state="disabled")

    def choose_excelfile(self):
        excel_path = filedialog.askopenfile()
        if excel_path:
            self.excel_path = excel_path
            self.excel_label.config(text=self.excel_path)
            set_config_value('main', 'excel_path', self.excel_path)
            self.save_config

    def choose_pdffile(self):
        pdf_path = filedialog.askdirectory()
        if pdf_path:
            self.pdf_path = pdf_path
            self.pdf_label.config(text=self.pdf_path)
            set_config_value('main', 'pdf_path', self.pdf_path)
            self.save_config

    def save_config(self):

        # Enregistrement des valeurs dans la configuration
        config.set('main', 'excel_path', self.excel_path)
        config.set('main', 'pdf_path', self.pdf_path)
        with open("config.ini", "w") as configfile:
            config.write(configfile)

        # Fermeture de l'application
        self.destroy()

    def lancer_script(self, sites):
        """Script du scrapping"""
        old_stdout = sys.stdout
        sys.stdout = mystdout = StringIO()
        print("Début du process !")
        download_pdf(reqs.response_2CUB, path_url.name_materion, self.pdf_path)
        for site in sites:
            response = requests.get(site['url'])
            soup = BeautifulSoup(response.content, "html.parser")
            data_extraction_function_name = f"extract_{site['name']}_data"
            if data_extraction_function_name in globals():
                data_extraction_function = globals()[data_extraction_function_name]
                data = data_extraction_function(soup)
                print (f"Données extraites pour le site {site['name']} : {data}")
            else:
                print(f'Aucune fonction d\'extraction de données trouvées')
        print('Fichier excel créé avec succès !')

        sys.stdout = old_stdout
        output = mystdout.getvalue()
        self.update_output(output)

# Lancement du process
if __name__ == '__main__':
    
    print("Début du process")
    app = MyApp()
    wb = openpyxl.load_workbook(app.excel_path)
    # Lancement de la boucle principale de la fenêtre
    app.mainloop()
    wb.save(app.excel_path)
    print('Fin du process')
    time.sleep(3)
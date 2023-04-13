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


# Extraction données lbma pour 1AG2 (EL)
def extract_1AG2_data(soup):
    # ws = wb['1AG2']
    ws = wb.create_sheet('1AG2')
    s=Service('C:/Users/adrie/OneDrive/Documents/chromedriver.exe')
    browser = webdriver.Chrome(service=s)
    url='https://www.lbma.org.uk/prices-and-data/precious-metal-prices#/table'
    browser.get(url)
    browser.maximize_window()
    time.sleep(5)
    table_path = "/html/body/div[1]/main/div[1]/div/div/div/div/div[2]/div/div[2]/div[4]/table"

    table = browser.find_elements(By.XPATH, "/html/body/div[1]/main/div[1]/div/div/div/div/div[2]/div/div[2]/div[4]/table")
    rows = browser.find_elements(By.XPATH, '/html/body/div[1]/main/div[1]/div/div/div/div/div[2]/div/div[2]/div[4]/table/tbody/tr[1]')
    drop = browser.find_elements(By.CLASS_NAME, 'dropdown-toggle')
    drop[0].click()
    a_drop = browser.find_elements(By.LINK_TEXT, 'Silver')
    a_drop[0].click()
    time.sleep(4)

    for row in rows:
        cells = row.find_elements(By.XPATH, '/html/body/div[1]/main/div[1]/div/div/div/div/div[2]/div/div[2]/div[4]/table/tbody/tr[1]/td[2]')
        for cell in (cells):
            row_number = ws.max_row +1
            ws.cell(row=row_number, column=1, value=date)
            ws.cell(row=row_number, column=2, value=cell.text.replace('.', ','))
            ws.cell(row=row_number, column=3, value='$')
            ws.cell(row=row_number, column=4, value='OZ')

    print(cell.text.replace('.', ','))

# Extraction données lbma pour 1AU2 (EL)
def extract_1AU2_data(soup):
    # ws = wb['1AU2']
    ws = wb.create_sheet('1AU2')
    s=Service('C:/Users/adrie/OneDrive/Documents/chromedriver.exe')
    browser = webdriver.Chrome(service=s)
    url='https://www.lbma.org.uk/prices-and-data/precious-metal-prices#/table'
    browser.get(url)
    browser.maximize_window()
    time.sleep(5)
    table_path = "/html/body/div[1]/main/div[1]/div/div/div/div/div[2]/div/div[2]/div[4]/table"

    table = browser.find_elements(By.XPATH, "/html/body/div[1]/main/div[1]/div/div/div/div/div[2]/div/div[2]/div[4]/table")
    rows = browser.find_elements(By.XPATH, '/html/body/div[1]/main/div[1]/div/div/div/div/div[2]/div/div[2]/div[4]/table/tbody/tr[1]')

    for row in rows:
        cells = row.find_elements(By.XPATH, '/html/body/div[1]/main/div[1]/div/div/div/div/div[2]/div/div[2]/div[4]/table/tbody/tr[1]/td[3]')
        for cell in (cells):
            row_number = ws.max_row +1
            ws.cell(row=row_number, column=1, value=date)
            ws.cell(row=row_number, column=2, value=cell.text.replace('.', ','))
            ws.cell(row=row_number, column=3, value='$')
            ws.cell(row=row_number, column=4, value='OZ')
    print(cell.text.replace('.', ','))
# Extraction données Cookson pour 1AG1 (EL)
def extract_1AG1_data(soup):
    """Extraire les données de la table Cookson et les ajouter au classeur Excel"""
    table = soup.find("table", {"class": "main"})
    # ws = wb['1AG1']
    ws = wb.create_sheet('1AG1')
    rows = soup.find_all("tr")
    second_row = rows[3]

    # Trouver la quatrième colonne de la table dans la deuxième ligne
    columns = second_row.find_all("td")
    fourth_column = columns[4]

    # Extraire le texte de la quatrième colonne
    data = fourth_column.text.strip()
    row_number = ws.max_row +1
    ws.cell(row=row_number, column=1, value=date)
    ws.cell(row=row_number, column=2, value=data.replace('.', ','))
    ws.cell(row=row_number, column=3, value='€')
    ws.cell(row=row_number, column=4, value='KG')
    print(data.replace('.', ','))

# Extraction données Cookson pour 1AU3 (EL)
def extract_1AU3_data(soup):
    """Extraire les données de la table Cookson et les ajouter au classeur Excel"""
    table = soup.find("table", {"class": "main"})
    # ws = wb['1AU3']
    ws = wb.create_sheet('1AU3')
    rows = soup.find_all("tr")
    second_row = rows[2]

    # Trouver la quatrième colonne de la table dans la deuxième ligne
    columns = second_row.find_all("td")
    last_column = columns[4]

    # Extraire le texte de la quatrième colonne
    data = last_column.text.strip()
    row_number = ws.max_row +1
    ws.cell(row=row_number, column=1, value=date)
    ws.cell(row=row_number, column=2, value=data.replace('.', ',').replace('€', ''))
    ws.cell(row=row_number, column=3, value='€')
    ws.cell(row=row_number, column=4, value='KG')
    print(data.replace('.', ',').replace('€', ''))

# Extraction données pour 1AG3 (EL)
def extract_1AG3_data(soup):
    """Extraire les données de la table Cookson et les ajouter au classeur Excel"""
    table = soup.find("table")
    # ws = wb['1AG3']
    ws = wb.create_sheet('1AG3')
    rows = soup.find_all("tr")
    second_row = rows[1]

    # Trouver la quatrième colonne de la table dans la deuxième ligne
    columns = second_row.find_all("td")
    fourth_column = columns[1]

    # Extraire le texte de la quatrième colonne
    data = fourth_column.text.strip()
    row_number = ws.max_row +1
    ws.cell(row=row_number, column=1, value=date)
    ws.cell(row=row_number, column=2, value=data.replace('.', ','))
    ws.cell(row=row_number, column=3, value='€')
    ws.cell(row=row_number, column=4, value='KG')
    print(data.replace('.', ','))

# Extraction données pour 2M37 (EL)
def extract_2M37_data(soup):
    """Extraire les données de la table Cookson et les ajouter au classeur Excel"""
    table = soup.find("table")
    # ws = wb['2M37']
    ws = wb.create_sheet('2M37')
    rows = soup.find_all("tr")
    second_row = rows[1]

    # Trouver la quatrième colonne de la table dans la deuxième ligne
    columns = second_row.find_all("td")
    fourth_column = columns[1]

    # Extraire le texte de la quatrième colonne
    data = fourth_column.text.strip()
    row_number = ws.max_row +1
    ws.cell(row=row_number, column=1, value=date)
    ws.cell(row=row_number, column=2, value=data.replace('.', ','))
    ws.cell(row=row_number, column=3, value='€')
    ws.cell(row=row_number, column=4, value='100 KG')
    print(data.replace('.', ','))

# Extraction données pour 3AL1 (EL)
def extract_3AL1_data(soup):
    """Extraire les données de la table Cookson et les ajouter au classeur Excel"""
    table = soup.find("table")
    # ws = wb['3AL1']
    ws = wb.create_sheet('3AL1')
    rows = soup.find_all("tr")
    second_row = rows[6]

    # Trouver la quatrième colonne de la table dans la deuxième ligne
    columns = second_row.find_all("td")
    fourth_column = columns[1]

    # Extraire le texte de la quatrième colonne
    data = fourth_column.text.strip()
    row_number = ws.max_row +1
    ws.cell(row=row_number, column=1, value=date)
    ws.cell(row=row_number, column=2, value=data.replace(',', '').replace('.', ','))
    ws.cell(row=row_number, column=3, value='$')
    ws.cell(row=row_number, column=4, value='TO')
    print(data.replace(',', '').replace('.', ','))
# Extraction données pour 3CU1 (EL)
def extract_3CU1_data(soup):
    """Extraire les données de la table Cookson et les ajouter au classeur Excel"""
    table = soup.find("table")
    # ws = wb['3CU1']
    ws = wb.create_sheet('3CU1')
    rows = soup.find_all("tr")
    second_row = rows[1]

    # Trouver la quatrième colonne de la table dans la deuxième ligne
    columns = second_row.find_all("td")
    fourth_column = columns[1]

    # Extraire le texte de la quatrième colonne
    data = fourth_column.text.strip()
    row_number = ws.max_row +1
    ws.cell(row=row_number, column=1, value=date)
    ws.cell(row=row_number, column=2, value=data.replace('.', '').replace('.', ','))
    ws.cell(row=row_number, column=3, value='$')
    ws.cell(row=row_number, column=4, value='TO')
    print(data.replace(',', '').replace('.', ','))
# Extraction données pour 3CU3 (EL)
def extract_3CU3_data(soup):
    """Extraire les données de la table Cookson et les ajouter au classeur Excel"""
    table = soup.find("table")
    # ws = wb['3CU3']
    ws = wb.create_sheet('3CU3')
    rows = soup.find_all("tr")
    second_row = rows[1]

    # Trouver la quatrième colonne de la table dans la deuxième ligne
    columns = second_row.find_all("td")
    fourth_column = columns[1]

    # Extraire le texte de la quatrième colonne
    data = fourth_column.text.strip()
    row_number = ws.max_row +1
    ws.cell(row=row_number, column=1, value=date)
    ws.cell(row=row_number, column=2, value=data.replace('.', ','))
    ws.cell(row=row_number, column=3, value='€')
    ws.cell(row=row_number, column=4, value='100 KG')
    print(data.replace('.', ','))

# Extraction données pour 2CUB (EL)
def extract_2CUB_data(path_materion, name_materion):
    """Extraire les données de la table Materion et les ajouter au classeur Excel"""
    # wm = wb['2CUB']
    wm = wb.create_sheet('2CUB')
    path = f"{path_materion}/{name_materion}"
    with open(path, 'rb') as pdf_materion:
        reader_materion = PdfReader(pdf_materion)
        page_materion = reader_materion.pages[0]
        text_materion = page_materion.extract_text()
        print('PDF lu')

        lines = text_materion.split('\n')

        alloy_line = None
        for line in lines:
            if line.startswith('Alloy 25'):
                alloy_line = line
                break

        if alloy_line is not None:
            # Récupérer la valeur de la 4ème colonne
            columns = alloy_line.split()
            if len(columns) >= 4:
                price_eur = columns[4]
            else:
                price_eur = None

            # Ajouter les nombres extraits dans le tableau Excel
            row_number = wm.max_row +1
            wm.cell(row=row_number, column=1, value=date)
            wm.cell(row=row_number, column=2, value=price_eur.replace('.', ','))
            wm.cell(row=row_number, column=3, value='€')
            wm.cell(row=row_number, column=4, value='KG')
            print(price_eur.replace('.', ','))

# Extraction données pour 3NI1 (EL)
def extract_3NI1_data(soup):
    """Extraction NICKEL Ligne 2, Valeur Colonne 3"""
    table = soup.find('table', class_='')
    # ws = wb['3NI1']
    ws = wb.create_sheet('3NI1')

    rows = soup.find_all('tr')
    second_row = rows[2]

    columns = second_row.find_all('td')
    fourth_column = columns[2]
    data = fourth_column.text.strip()
    row_number = ws.max_row +1
    ws.cell(row=row_number, column=1, value=date)
    ws.cell(row=row_number, column=2, value=data.replace('.', '').replace('¹', ''))
    ws.cell(row=row_number, column=3, value='$')
    ws.cell(row=row_number, column=4, value='TO')
    print(data.replace('.', '').replace('¹', ''))

# Extraction données pour 3SN1 (EL)
def extract_3SN1_data(soup):
    """Extraction ETAIN Ligne 3, Valeur Colonne 3"""
    table = soup.find('table', class_='')
    # ws =  wb['3SN1']
    ws = wb.create_sheet('3SN1')
    rows = soup.find_all('tr')
    second_row = rows[3]

    columns = second_row.find_all('td')
    fourth_column = columns[2]
    data = fourth_column.text.strip()
    row_number = ws.max_row +1
    ws.cell(row=row_number, column=1, value=date)
    ws.cell(row=row_number, column=2, value=data.replace('.', '').replace('¹', ''))
    ws.cell(row=row_number, column=3, value='$')
    ws.cell(row=row_number, column=4, value='TO')

    print(data.replace('.', '').replace('¹', ''))

################################################################

# Extraction données Materion Alloy 360(AC) EN ATTENTE
def extract_materion_alloy360_data(file_name):
    """Extraire les données de la table Materion et les ajouter au classeur Excel"""
    wb.create_sheet('Materion')
    wm = wb['Materion']
    wm.append(['Materion'])

    with open(path_url.folder_materion, 'rb') as pdf_materion:
        reader_materion = PdfReader(pdf_materion)
        page_materion = reader_materion.pages[0]
        text_materion = page_materion.extract_text()

        lines = text_materion.split('\n')

        alloy_line = None
        for line in lines:
            if line.startswith('Alloy 360'):
                alloy_line = line
                break

        if alloy_line is not None:
            # Récupérer la valeur de la 4ème colonne
            columns = alloy_line.split()
            if len(columns) >= 4:
                price_eur = columns[4]
            else:
                price_eur = None

            # Ajouter les nombres extraits dans le tableau Excel
            wm['A2'] = 'Alloy 360'
            wm['B2'] = price_eur.replace('.', ',')
            wm['C2'] = '€'


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
        excel_path = filedialog.askdirectory()
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

    def lancer_script(self):
        """Script du scrapping"""
        old_stdout = sys.stdout
        sys.stdout = mystdout = StringIO()
        print("Début du process !")
        download_pdf(reqs.response_2CUB, path_url.name_materion, self.pdf_path)
        extract_1AG2_data(get_soup(reqs.response_1AG2))
        extract_1AU2_data(get_soup(reqs.response_1AU2))
        extract_1AG1_data(get_soup(reqs.response_1AG1))
        extract_1AU3_data(get_soup(reqs.response_1AU3))
        extract_1AG3_data(get_soup(reqs.response_1AG3))
        extract_2M37_data(get_soup(reqs.response_2M37))
        extract_3AL1_data(get_soup(reqs.response_3AL1))
        extract_3CU1_data(get_soup(reqs.response_3CU1))
        extract_3CU3_data(get_soup(reqs.response_3CU3))
        extract_2CUB_data(self.pdf_path, path_url.name_materion)
        extract_3NI1_data(get_soup(reqs.response_3NI1))
        extract_3SN1_data(get_soup(reqs.response_3SN1))
        delete_pdfs(self.pdf_path, path_url.name_materion)
        file_path = os.path.join(self.excel_path, 'metals_prices.xlsx')
        wb.save(file_path)
        print('Fichier excel créé avec succès !')

        sys.stdout = old_stdout
        output = mystdout.getvalue()
        self.update_output(output)

# Lancement du process
if __name__ == '__main__':

    print("Début du process")
    wb = Workbook()
    app = MyApp()
    # wb = openpyxl.load_workbook(app.excel_path)
    # Lancement de la boucle principale de la fenêtre
    app.mainloop()
    # wb.save(app.excel_path)
    print('Fin du process')
    time.sleep(3)
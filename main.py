import requests
import os
import re
import time
from bs4 import BeautifulSoup
from openpyxl import Workbook
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



def choice_path():
    """Choisir le chemin pour déposer le fichier Excel"""
    chemin = filedialog.askdirectory()
    print(chemin)


# Téléchargement des PDFs
def download_pdf(response, name, folder):
    """Télécharger un fichier PDF et l'enregistrer localement"""
    if response.status_code == 200:
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
        print("Connexion réussi")
        return BeautifulSoup(response.content, "html.parser")
    else:
        print("Erreur lors de la récupération du contenu HTML")


# Extraction données lbma pour 1AG2 (EL)
def extract_1AG2_data(soup):
    ws = wb.create_sheet('1AG2')
    ws.append(['Ag LBMA' ])
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
            print(cell.text)
            ws['A2'] = 'AG'
            ws['B2'] = cell.text.replace('.', ',')
            ws['C2'] = '$'

# Extraction données lbma pour 1AU2 (EL)
def extract_1AU2_data(soup):
    ws = wb.create_sheet('1AU2')
    ws.append(['Au LBMA'])
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
            print(cell.text)
            ws['A2'] = 'AU'
            ws['B2'] = cell.text.replace('.', ',')
            ws['C2'] = '$'

# Extraction données Cookson pour 1AG1 (EL)
def extract_1AG1_data(soup):
    """Extraire les données de la table Cookson et les ajouter au classeur Excel"""
    table = soup.find("table", {"class": "main"})
    ws = wb.create_sheet('1AG1')
    ws.append(['Ag c3E'])

    rows = soup.find_all("tr")
    second_row = rows[3]

    # Trouver la quatrième colonne de la table dans la deuxième ligne
    columns = second_row.find_all("td")
    fourth_column = columns[4]

    # Extraire le texte de la quatrième colonne
    data = fourth_column.text.strip()

    ws['A2'] = 'AG'
    ws['B2'] = data.replace('.', ',')
    ws['C2'] = '€'

# Extraction données Cookson pour 1AU3 (EL)
def extract_1AU3_data(soup):
    """Extraire les données de la table Cookson et les ajouter au classeur Excel"""
    table = soup.find("table", {"class": "main"})
    ws = wb.create_sheet('1AU3')
    ws.append(['Au Industriel'])

    rows = soup.find_all("tr")
    second_row = rows[2]

    # Trouver la quatrième colonne de la table dans la deuxième ligne
    columns = second_row.find_all("td")
    last_column = columns[4]

    # Extraire le texte de la quatrième colonne
    data = last_column.text.strip()

    print(data)
    ws['A2'] = 'AU'
    ws['B2'] = data.replace('.', ',').replace('€', '')
    ws['C2'] = '€'


# Extraction données pour 1AG3 (EL)
def extract_1AG3_data(soup):
    """Extraire les données de la table Cookson et les ajouter au classeur Excel"""
    table = soup.find("table")
    ws = wb.create_sheet('1AG3')
    ws.append(['Ag Westmetall (Finesliber)'])

    rows = soup.find_all("tr")
    second_row = rows[1]

    # Trouver la quatrième colonne de la table dans la deuxième ligne
    columns = second_row.find_all("td")
    fourth_column = columns[1]

    # Extraire le texte de la quatrième colonne
    data = fourth_column.text.strip()
    print(data)

    ws['A2'] = 'AG'
    ws['B2'] = data.replace('.', ',')
    ws['C2'] = '€'

# Extraction données pour 2M37 (EL)
def extract_2M37_data(soup):
    """Extraire les données de la table Cookson et les ajouter au classeur Excel"""
    table = soup.find("table")
    ws = wb.create_sheet('2M37')
    ws.append(['Metalrate CuZn37/38'])

    rows = soup.find_all("tr")
    second_row = rows[1]

    # Trouver la quatrième colonne de la table dans la deuxième ligne
    columns = second_row.find_all("td")
    fourth_column = columns[1]

    # Extraire le texte de la quatrième colonne
    data = fourth_column.text.strip()
    print(data)

    ws['A2'] = 'CuZn37/38'
    ws['B2'] = data.replace('.', ',')
    ws['C2'] = '€'

# Extraction données pour 3AL1 (EL)
def extract_3AL1_data(soup):
    """Extraire les données de la table Cookson et les ajouter au classeur Excel"""
    table = soup.find("table")
    ws = wb.create_sheet('3AL1')
    ws.append(['LME Settlement Aluminium'])

    rows = soup.find_all("tr")
    second_row = rows[6]

    # Trouver la quatrième colonne de la table dans la deuxième ligne
    columns = second_row.find_all("td")
    fourth_column = columns[1]

    # Extraire le texte de la quatrième colonne
    data = fourth_column.text.strip()
    print(data)

    ws['A2'] = 'AL'
    ws['B2'] = data.replace(',', '').replace('.', ',')
    ws['C2'] = '$'

# Extraction données pour 3CU1 (EL)
def extract_3CU1_data(soup):
    """Extraire les données de la table Cookson et les ajouter au classeur Excel"""
    table = soup.find("table")
    ws = wb.create_sheet('3CU1')
    ws.append(['LME Settlement Copper'])

    rows = soup.find_all("tr")
    second_row = rows[1]

    # Trouver la quatrième colonne de la table dans la deuxième ligne
    columns = second_row.find_all("td")
    fourth_column = columns[1]

    # Extraire le texte de la quatrième colonne
    data = fourth_column.text.strip()
    print(data)

    ws['A2'] = 'CU'
    ws['B2'] = data.replace(',', '').replace('.', ',')
    ws['C2'] = '$'

# Extraction données pour 3CU3 (EL)
def extract_3CU3_data(soup):
    """Extraire les données de la table Cookson et les ajouter au classeur Excel"""
    table = soup.find("table")
    ws = wb.create_sheet('3CU3')
    ws.append(['Wieland Kopper'])

    rows = soup.find_all("tr")
    second_row = rows[1]

    # Trouver la quatrième colonne de la table dans la deuxième ligne
    columns = second_row.find_all("td")
    fourth_column = columns[1]

    # Extraire le texte de la quatrième colonne
    data = fourth_column.text.strip()
    print(data)

    ws['A2'] = 'CU'
    ws['B2'] = data.replace('.', ',')
    ws['C2'] = '€'

# Extraction données pour 2CUB (EL)
def extract_2CUB_data(path_materion, name_materion):
    """Extraire les données de la table Materion et les ajouter au classeur Excel"""
    wb.create_sheet("2CUB")
    wm = wb['2CUB']
    path = f"{path_materion}/{name_materion}"
    with open(path, 'rb') as pdf_materion:
        reader_materion = PdfReader(pdf_materion)
        page_materion = reader_materion.pages[0]
        text_materion = page_materion.extract_text()

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
            wm['A3'] = 'Alloy 25'
            wm['B3'] = price_eur.replace('.', ',')
            wm['C3'] = '€'

# Extraction données pour 3NI1 (EL)
def extract_3NI1_data(soup):
    """Extraction NICKEL Ligne 2, Valeur Colonne 3"""
    table = soup.find('table', class_='')
    ws = wb.create_sheet('3NI1')
    ws.append(['NICKEL'])

    rows = soup.find_all('tr')
    second_row = rows[2]

    columns = second_row.find_all('td')
    fourth_column = columns[2]
    data = fourth_column.text.strip()
    print (data)

    ws['A2'] = 'Ni'
    ws['B2'] = data.replace('.', '').replace('¹', '')
    ws['C2'] = '$'

# Extraction données pour 3SN1 (EL)
def extract_3SN1_data(soup):
    """Extraction ETAIN Ligne 3, Valeur Colonne 3"""
    table = soup.find('table', class_='')
    ws =  wb.create_sheet('3SN1')
    ws.append(['ETAIN'])
    rows = soup.find_all('tr')
    second_row = rows[3]

    columns = second_row.find_all('td')
    fourth_column = columns[2]
    data = fourth_column.text.strip()
    print (data)

    ws['A2'] = 'Sn'
    ws['B2'] = data.replace('.', '').replace('¹', '')
    ws['C2'] = '$'
################################################################

# Extraction données KME (AP)
def extract_kme_data(soup):
    """Extraire les données de la table KME et les ajouter au classeur Excel"""
    table = soup.find('table', class_='table table-condensed table-hover table-striped')
    ws = wb.create_sheet('KME')

    for row in table.find_all('tr'):
        data = []
        for cell in row.find_all('td')[:4]:
            data.append(cell.text.strip())
        if len(data) == 4:
            ws.append([data[3], data[1], data[2].replace('*', '').replace('.', '').replace(',', '.')])

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

        self.config = configparser.ConfigParser()
        self.config.read("config.ini")

        self.output_text = tk.Text(right_frame, bg='white', state='disabled', width=40)
        self.output_text.pack(side='top', fill='both', expand=True)

        self.excel_path = self.config.get("main", "excel_path", fallback="")
        self.pdf_path = self.config.get("main", "pdf_path", fallback="")


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

    def choose_pdffile(self):
        pdf_path = filedialog.askdirectory()
        if pdf_path:
            self.pdf_path = pdf_path
            self.pdf_label.config(text=self.pdf_path)

    def save_config(self):
        # sauvegarde du chemin d'accès dans le fichier de configuration
        self.config["main"] = {"excel_path": self.excel_path, "pdf_path": self.pdf_path}
        with open("config.ini", "w") as configfile:
            self.config.write(configfile)

        # fermeture de l'application
        self.destroy()

    def lancer_script(self):
        """Script du scrapping"""
        old_stdout = sys.stdout
        sys.stdout = mystdout = StringIO()
        print("Début du process !")
        download_pdf(reqs.response_2CUB, path_url.name_materion, self.pdf_path)
        print("Téléchargement du PDF...")
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
        print('Suppresion du PDF')

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
    # Lancement de la boucle principale de la fenêtre
    app.mainloop()

    print('Fin du process')
    time.sleep(3)
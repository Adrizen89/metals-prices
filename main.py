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

# Récupérer les responses
def get_soup(response):
    """Récupérer le soup à partir de la réponse HTTP"""
    if response.status_code == 200:
        print("Connexion réussi")
        return BeautifulSoup(response.content, "html.parser")
    else:
        print("Erreur lors de la récupération du contenu HTML")

# Extraction données lbma
def extract_lbma_data(soup):
    ws = wb.create_sheet('LBMA')
    ws.append(['Index', 'AM $', 'PM $', 'AM £', 'PM £', 'AM €', 'PM €' ])
    s=Service('C:/Users/adrie/OneDrive/Documents/chromedriver.exe')
    browser = webdriver.Chrome(service=s)
    url='https://www.lbma.org.uk/prices-and-data/precious-metal-prices#/table'
    browser.get(url)
    browser.maximize_window()
    time.sleep(5)
    table_path = "/html/body/div[1]/main/div[1]/div/div/div/div/div[2]/div/div[2]/div[4]/table"

    table = browser.find_elements(By.XPATH, "/html/body/div[1]/main/div[1]/div/div/div/div/div[2]/div/div[2]/div[4]/table")
    rows = browser.find_elements(By.XPATH, '/html/body/div[1]/main/div[1]/div/div/div/div/div[2]/div/div[2]/div[4]/table/tbody/tr[1]')

    current_date = ""
    row_count = 1
    for row in rows:
        cells = row.find_elements(By.TAG_NAME, 'td')
        if len(cells) == 1: # New date row
            current_date = cells[0].text
            row_count += 1
            ws.cell(row=row_count, column=1, value=current_date)
        else: # Data row
            row_count += 1
            for i, cell in enumerate(cells):
                if i == 0: # Date column
                    current_date = cell.text
                    ws.cell(row=row_count, column=1, value=current_date)
                else:
                    value = cell.text.replace(',', '')
                    ws.cell(row=row_count, column=i+1, value=value)



# Extraction données Cookson
def extract_cookson_data(soup):
    """Extraire les données de la table Cookson et les ajouter au classeur Excel"""
    table = soup.find("table", {"class": "main"})
    ws = wb.create_sheet('Cookson')
    ws.append(['Index', '1er fixing USD/oz', '1er fixing EUR/Kg', '2ème fixing EUR/Kg'])

    for row in table.find_all("tr"):
        columns = row.find_all("td")[1:]

        for i in range(1, 3):
            if any(c.isalpha() for c in columns[i].text):
                columns[i] = "-"
            column_2 = columns[0]
            if column_2.a:
                column_2.a.extract()
            columns[0] = column_2

        columns = [column.text.replace('€', '').replace('$', '').replace(',', '.') for column in columns]
        columns.reverse()
        ws.append(columns)

# Extraction données KME
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

# Extraction données Wieland
def extract_wieland_data(soup):
    """Extraire les données de la table Wieland et les ajouter au classeur Excel"""
    table = soup.find('table', class_='metalinfo-table table-lme-settlement')
    ws = wb.create_sheet('Wieland')
    ws.append(['Index', 'Prix', 'Devise'])

    for row in table.find_all('tr'):
        data = []
        for cell in row.find_all("td")[:3]:
            data.append(cell.text.strip())
        if len(data) == 3:
            ws.append([data[2], data[1].replace(',', '')])

# Extraction données Reynolds
def extract_reynolds_data(name_reynolds, wb):
    """Extraire les données du PDF Reynolds et les ajouter au classeur Excel"""
    wb.create_sheet('Reynolds')
    wr = wb['Reynolds']

    with open(path_url.folder_reynolds, 'rb') as pdf_reynolds:
        reader_reynolds = PdfReader(pdf_reynolds)
        page_reynolds = reader_reynolds.pages[0]
        text_reynolds = page_reynolds.extract_text()

        lines_reynolds = text_reynolds.split('\n')

        # Ajouter les données du PDF dans le fichier Excel
        for line in lines_reynolds:
            # Séparer les données en colonnes
            data = line.split()
            if "EUR/USD" in data:
                data[1] = data[1].replace(',', '.')
                # Si "EUR/USD" est trouvé, on a seulement 3 colonnes
                wr.append([data[0], data[1], data[2]])
            elif len(data) == 4:
                # Ajouter "1 TO" à la 4ème colonne
                if data[0] not in ["LME", "BASE", "METAL", "France"] and data[1] not in ["LME", "BASE", "METAL", "France"]:
                    if "," in data[1]:
                        data[1] = data[1].replace(',', '.')
                    else: data[1] = float(data[1])
                    # Ajouter "1 TO" à la 4ème colonne
                    wr.append([data[0], data[1], data[2], data[3]])
                else:
                    # Si la dernière colonne ne contient pas "1 TO", ajouter "1 TO" à la 4ème colonne
                    if data[0] not in ["LME", "BASE", "METAL", "France"]:
                        # Ajouter "1 TO" à la 4ème colonne
                        data.append("1 TO")
                        wr.append([data[0], data[1].replace(',', '.'), data[2], data[3]])

# Extraction données Materion
def extract_materion_data(file_name):
    """Extraire les données de la table Materion et les ajouter au classeur Excel"""
    wb.create_sheet('Materion')
    wm = wb['Materion']

    with open(path_url.folder_materion, 'rb') as pdf_materion:
        reader_materion = PdfReader(pdf_materion)
        page_materion = reader_materion.pages[0]
        text_materion = page_materion.extract_text()
        numbers = re.findall(r'\d+\.\d{2}', text_materion)

        # Ajouter des en-têtes de colonne
        wm['A1'] = 'USD/Lb'
        wm['B1'] = 'EUR/Kg'
        wm['C1'] = 'GBP/Kg'
        wm['D1'] = 'RMB/Kg'
        wm['E1'] = 'USD/Kg'

        # Ajouter les nombres extraits dans le tableau Excel
        for i, number in enumerate(numbers):
            row = (i // 5) + 2  # calculer le numéro de ligne en fonction de l'indice de la boucle
            col = (i % 5) + 1  # calculer le numéro de colonne en fonction de l'indice de la boucle
            wm.cell(row=row, column=col, value=number)

# Suppression des PDFs
def delete_pdfs():
    """Supprimer deux fichiers PDF"""
    try:
        os.remove(path_url.folder_materion)
        os.remove(path_url.folder_reynolds)
        print("Suppression des fichiers PDF terminée avec succès")
    except FileNotFoundError:
        print("Erreur : au moins un des fichiers PDF n'existe pas")
    except Exception as e:
        print(f"Une erreur s'est produite : {e}")

# Lancement du process
if __name__ == '__main__':
    print("Début du process")
    wb = Workbook()
    extract_lbma_data(get_soup(reqs.response_lbma))
    extract_cookson_data(get_soup(reqs.response_cookson))
    extract_kme_data(get_soup(reqs.response_kme))
    extract_wieland_data(get_soup(reqs.response_wieland))
    download_pdf(reqs.response_reynolds, path_url.name_reynolds, path_url.download_path)
    extract_reynolds_data(path_url.name_reynolds, wb)
    download_pdf(reqs.response_materion, path_url.name_materion, path_url.download_path)
    extract_materion_data(path_url.name_materion)
    delete_pdfs()

    file_path = os.path.join(path_url.excel_path, 'metals_prices.xlsx')
    wb.save(file_path)
    print('Fichier excel créé avec succès !')
    print('Fin du process')
    time.sleep(3)
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

# Extraction données lbma pour 1AG2
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

# Extraction données lbma pour 1AU2
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



# Extraction données Cookson pour 1AG1
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

# Extraction données Cookson pour 1AU3
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


# Extraction données pour 1AG3
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

# Extraction données pour 2M37
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

# Extraction données pour 3AL1
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

# Extraction données pour 3CU1
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

# Extraction données pour 3CU3
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

# Extraction AURUBIS CuSn0, 15
# Extraction AURUBIS Cu-ETP
# Extraction AURUBIS CuFe0, 1P
# Extraction AURUBIS Cu-DLP

# Extraction NOVAPROFIL CuZn30
# Extraction NOVAPROFIL CuZn33
# Extraction NOVAPROFIL CuZn36
# Extraction NOVAPROFIL CuZn37

# Extraction INOVAN Cu Invar Cu
# Extraction INOVAN Cu-OF

# Extraction PROFILTECH CuBe1,9
# Extraction PROFILTECH CuSn6P
# Extraction PROFILTECH Cu-PHC


# Extraction WIELAND CuSn6
# Extraction WIELAND Cu-ETP
# Extraction WIELAND Cu-OF
# Extraction WIELAND Cu-OFE
# Extraction WIELAND CuPHC
# Extraction WIELAND Cu-DLP
# Extraction WIELAND K55
# Extraction WIELAND Cu Fe0.1 P

# Extraction MATERION CuBe1,9
# Extraction MATERION Alloy 360

# Extraction R-METAL CuSn6P
# Extraction R-METAL CuSn8P
# Extraction R-METAL CuSn9P
# Extraction R-METAL CuZn30
# Extraction R-METAL Cu-ETP
# Extraction R-METAL Inox 1,4310

# Extraction SUNDWIGER CuSn0,15
# Extraction SUNDWIGER CuSn6P

# Extraction ARS CuSn6
# Extraction ARS CuZn37
# Extraction ARS ALU 1050A
# Extraction ARS ALU 5754

# Extraction THERMOCOMPACT Ni TOT
# Extraction THERMOCOMPACT AuCo TOT
# Extraction THERMOCOMPACT Au total sur s/c Ni total

# Extraction RICHARD STENZHORN CuFe2P
# Extraction RICHARD STENZHORN CuZn30
# Extraction RICHARD STENZHORN CuSn6P

# Extraction AD-PLATING Ni TOTAL 2 µm mini
# Extraction AD-PLATING Ni total 3 à 9µ

# Extraction KME STOL78
# Extraction KME Cu-OFE

# Extraction PEM CuSn6P
# Extraction PEM Cu-ETP
# Extraction PEM CuZn36
# Extraction PEM CuZn36 H12
# Extraction PEM Ni
# Extraction PEM NiP
# Extraction PEM Au
# Extraction PEM Sn V
# Extraction PEM Ag

# Extraction GRISET CuFe0,1P-FPG
# Extraction GRISET  FGP
# Extraction GRISET  Cu-ETP
# Extraction GRISET  CuSn0,15
# Extraction GRISET  Cu-DLP
# Extraction GRISET  CuFe0,1P
# Extraction GRISET  Cu-DHP
# Extraction GRISET  CuFe2P
# Extraction GRISET  CuSn6P

# Extraction LEGENI Ni TOT
# Extraction LEGENI Au TOT
# Extraction LEGENI Au total sur s/c Ni total

# Extraction DPE Sn
# Extraction DPE Ag
# Extraction DPE Ag20
# Extraction DPE Au b
# Extraction DPE Au b20
# Extraction DPE AuCo
# Extraction DPE Cu
# Extraction DPE Cu20
# Extraction DPE Ni
# Extraction DPE NiP

# Lancement du process
if __name__ == '__main__':
    print("Début du process")
    wb = Workbook()
    # Extraction pour Elisabeth
    extract_1AG2_data(get_soup(reqs.response_lbma))
    extract_1AU2_data(get_soup(reqs.response_lbma))
    extract_1AG1_data(get_soup(reqs.response_cookson))
    extract_1AU3_data(get_soup(reqs.response_cookson))
    extract_1AG3_data(get_soup(reqs.response_1AG3))
    extract_2M37_data(get_soup(reqs.response_2M37))
    extract_3AL1_data(get_soup(reqs.response_3AL1))
    extract_3CU1_data(get_soup(reqs.response_3CU1))
    extract_3CU3_data(get_soup(reqs.response_3CU3))

    # Extraction pour les Achats

    #extract_kme_data(get_soup(reqs.response_kme))
    #extract_wieland_data(get_soup(reqs.response_wieland))
    #download_pdf(reqs.response_reynolds, path_url.name_reynolds, path_url.download_path)
    #extract_reynolds_data(path_url.name_reynolds, wb)
    #download_pdf(reqs.response_materion, path_url.name_materion, path_url.download_path)
    #extract_materion_data(path_url.name_materion)
    #delete_pdfs()

    file_path = os.path.join(path_url.excel_path, 'metals_prices.xlsx')
    wb.save(file_path)
    print('Fichier excel créé avec succès !')
    print('Fin du process')
    time.sleep(3)

import configparser
from PyPDF2 import PdfReader
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager
from app.data_list import sites
import os
from selenium.common.exceptions import NoSuchElementException, TimeoutException

config = configparser.ConfigParser()
config.read('config.ini')


# Extraction données Cookson pour 1AG1 (EL)
def extract_1AG1(soup):
    """Extraire les données de la table Cookson et les ajouter au classeur Excel"""
    table = soup.find("table", {"class": "main"})
    rows = soup.find_all("tr")
    second_row = rows[3]

    # Trouver la quatrième colonne de la table dans la deuxième ligne
    columns = second_row.find_all("td")
    fourth_column = columns[4]

    # Extraire le texte de la quatrième colonne
    data = fourth_column.text.strip()
    formatted_data = data.replace('.', ',')
    return formatted_data
    print(formated_data)

# Extraction données Cookson pour 1AU3 (EL)
def extract_1AU3(soup):
    """Extraire les données de la table Cookson et les ajouter au classeur Excel"""
    table = soup.find("table", {"class": "main"})
    rows = soup.find_all("tr")
    second_row = rows[2]

    # Trouver la quatrième colonne de la table dans la deuxième ligne
    columns = second_row.find_all("td")
    last_column = columns[4]

    # Extraire le texte de la quatrième colonne
    data = last_column.text.strip()
    formatted_data = data.replace('.', ',').replace('€', '')
    return formatted_data

# Extraction données pour 1AG3 (EL)
def extract_1AG3(soup):
    """Extraire les données de la table Cookson et les ajouter au classeur Excel"""
    table = soup.find("table")
    rows = soup.find_all("tr")
    second_row = rows[1]

    # Trouver la quatrième colonne de la table dans la deuxième ligne
    columns = second_row.find_all("td")
    fourth_column = columns[1]

    # Extraire le texte de la quatrième colonne
    data = fourth_column.text.strip()
    formatted_data = data.replace('.', ',')
    return formatted_data

# Extraction données pour 2M37 (EL)
def extract_2M37(soup):
    """Extraire les données de la table Cookson et les ajouter au classeur Excel"""
    table = soup.find("table")
    rows = soup.find_all("tr")
    second_row = rows[1]

    # Trouver la quatrième colonne de la table dans la deuxième ligne
    columns = second_row.find_all("td")
    fourth_column = columns[1]

    # Extraire le texte de la quatrième colonne
    data = fourth_column.text.strip()
    formatted_data = data.replace('.', ',')
    return formatted_data

# Extraction données pour 3AL1 (EL)
def extract_3AL1(soup):
    """Extraire les données de la table Cookson et les ajouter au classeur Excel"""
    table = soup.find("table")
    rows = soup.find_all("tr")
    second_row = rows[6]

    # Trouver la quatrième colonne de la table dans la deuxième ligne
    columns = second_row.find_all("td")
    fourth_column = columns[1]

    # Extraire le texte de la quatrième colonne
    data = fourth_column.text.strip()
    formatted_data = data.replace(',', '').replace('.', ',')
    return formatted_data

# Extraction données pour 3CU1 (EL)
def extract_3CU1(soup):
    """Extraire les données de la table Cookson et les ajouter au classeur Excel"""
    table = soup.find("table")
    rows = soup.find_all("tr")
    second_row = rows[1]

    # Trouver la quatrième colonne de la table dans la deuxième ligne
    columns = second_row.find_all("td")
    fourth_column = columns[1]

    # Extraire le texte de la quatrième colonne
    data = fourth_column.text.strip()
    formatted_data = data.replace(',', '').replace('.', ',')
    return formatted_data

# Extraction données pour 3CU3 (EL)
def extract_3CU3(soup):
    """Extraire les données de la table Cookson et les ajouter au classeur Excel"""
    table = soup.find("table")
    rows = soup.find_all("tr")
    second_row = rows[1]

    # Trouver la quatrième colonne de la table dans la deuxième ligne
    columns = second_row.find_all("td")
    fourth_column = columns[1]

    # Extraire le texte de la quatrième colonne
    data = fourth_column.text.strip()
    formatted_data = data.replace('.', ',')
    return formatted_data

# Extraction données pour 3NI1 (EL)
def extract_3NI1(soup):
    """Extraction NICKEL Ligne 2, Valeur Colonne 3"""
    table = soup.find('table', class_='')

    rows = soup.find_all('tr')
    second_row = rows[2]

    columns = second_row.find_all('td')
    fourth_column = columns[2]
    data = fourth_column.text.strip()
    formatted_data = data.replace('.', '').replace('¹', '')
    return formatted_data

# Extraction données pour 3SN1 (EL)
def extract_3SN1(soup):
    """Extraction ETAIN Ligne 3, Valeur Colonne 3"""
    table = soup.find('table', class_='')
    rows = soup.find_all('tr')
    second_row = rows[3]

    columns = second_row.find_all('td')
    fourth_column = columns[2]
    data = fourth_column.text.strip()

    formatted_data = data.replace('.', '').replace('¹', '')
    return formatted_data

def extract_2CUB(soup):
    """Extraire les données de la table Materion et les ajouter au classeur Excel"""

    pdf_path = config.get('main', 'pdf_path')
    name_pdf = config.get('main', 'name_pdf')

    if not pdf_path:
        pdf_path = os.getcwd()

    path = f"{pdf_path}/{name_pdf}"
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

            formatted_data = price_eur.replace('.', ',')
            return formatted_data

# Extraction données lbma pour 1AG2 (EL)
def extract_1AG2(soup):
    try:
        path_driver_chrome = config.get('main', 'path_driver_chrome')
        s=Service(path_driver_chrome)
        browser = webdriver.Chrome(service=s)
        url= 'https://www.lbma.uk/prices-and-data/precious-metal-prices#/table'
        try:
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
                    formatted_data = cell.text.replace('.', ',')
        except Exception as e:
            print (f"Erreur : {e}")
            formatted_data = "err"
        finally:
            browser.quit()

    except NoSuchElementException:
        print("Erreur : élément non trouvé")
        formatted_data = None
    except TimeoutException:
        print("Erreur : délai d'attente dépassé")
        formatted_data = None
    finally:
        return formatted_data

# Extraction données lbma pour 1AU2 (EL)
def extract_1AU2(soup):

    
    try:
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
                formatted_data = cell.text.replace('.', ',')
    except NoSuchElementException:
        print("Erreur : élément non trouvé")
        formatted_data = None
    except TimeoutException:
        print("Erreur : délai d'attente dépassé")
        formatted_data = None


    finally:
        return formatted_data

# Extraction données 2M30
def extract_2M30(soup):
    table = soup.find('table', class_='metalinfo-table table-currency')

    rows = soup.find_all('tr')
    second_row = rows[22]

    columns = second_row.find_all('td')
    fourth_column = columns[1]
    data = fourth_column.text.strip()
    formatted_data = data.replace(',', '').replace('.', ',')

    return formatted_data

# Extraction données 2B16
def extract_2B16(soup):
    table = soup.find('table', class_='metalinfo-table table-currency')

    rows = soup.find_all('tr')
    second_row = rows[14]

    columns = second_row.find_all('td')
    fourth_column = columns[1]
    data = fourth_column.text.strip()
    formatted_data = data.replace(',', '').replace('.', ',')
    return formatted_data
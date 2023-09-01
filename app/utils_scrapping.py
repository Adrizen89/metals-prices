import configparser
from PyPDF2 import PdfReader
import time
from app.data_list import sites
import os
from .config import get_config_value, get_pdf_path, set_config_value
import json
from urllib.request import urlopen

config = configparser.ConfigParser()
config.read('config.ini')


# Extraction données Cookson pour 1AG1 (EL)
def extract_1AG1(soup):
    """Extraire les données de la table Cookson et les ajouter au classeur Excel"""
    table = soup.find("table")
    rows = soup.find_all("tr")
    second_row = rows[3]

    # Trouver la quatrième colonne de la table dans la deuxième ligne
    columns = second_row.find_all("td")
    last_column = columns[3]

    # Extraire le texte de la quatrième colonne
    data = last_column.text.strip()
    formatted_data = data.replace('€', '')
    return formatted_data

# Extraction données Cookson pour 1AU3 (EL)
def extract_1AU3(soup):
    """Extraire les données de la table Cookson et les ajouter au classeur Excel"""
    table = soup.find("table")
    rows = soup.find_all("tr")
    second_row = rows[2]

    # Trouver la quatrième colonne de la table dans la deuxième ligne
    columns = second_row.find_all("td")
    last_column = columns[3]

    # Extraire le texte de la quatrième colonne
    data = last_column.text.strip()
    formatted_data = data.replace('.', ',').replace('€', '').replace(' ','')
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
    table = soup.find('table', class_='table table-condensed table-hover table-striped')

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

    pdf_path = get_config_value('main', 'pdf_path')
    name_pdf = get_config_value('main', 'name_pdf')

    if not pdf_path:
        pdf_path = os.getcwd()

    path = f"{pdf_path}/{name_pdf}"
    try:
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
    except FileNotFoundError:
        print(f"Le fichier PDF '{name_pdf}' n'a pas été trouvé. Passage à autre chose.")
        formatted_data = 'err'
        return formatted_data

def extract_2360(soup):
    """Extraire les données de la table Materion et les ajouter au classeur Excel"""

    pdf_path = get_config_value('main', 'pdf_path')
    name_pdf = get_config_value('main', 'name_pdf')

    if not pdf_path:
        pdf_path = os.getcwd()

    path = f"{pdf_path}/{name_pdf}"
    try:
        with open(path, 'rb') as pdf_materion:
            reader_materion = PdfReader(pdf_materion)
            page_materion = reader_materion.pages[0]
            text_materion = page_materion.extract_text()
            print('PDF lu')

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

                formatted_data = price_eur.replace('.', ',')
                return formatted_data
    except FileNotFoundError:
        print(f"Le fichier PDF '{name_pdf}' n'a pas été trouvé. Passage à autre chose.")
        formatted_data = 'err'
        return formatted_data

# Extraction données lbma pour 1AG2 (EL)
def extract_1AG2(soup):
    url = "https://prices.lbma.org.uk/json/silver.json?r=211497526"
    response = urlopen(url).read()
    data = json.loads(response)
    latest_prices = data[-1]
    first_value = latest_prices['v'].pop(0)
    data = str(first_value)
    formatted_data = data.replace('.', ',')
    
    print(formatted_data)
    return formatted_data


# Extraction données lbma pour 1AU2 (EL)
def extract_1AU2(soup):

    url = "https://prices.lbma.org.uk/json/gold_pm.json?r=666323974"
    response = urlopen(url).read()
    data = json.loads(response)
    latest_prices = data[-1]
    first_value = latest_prices['v'].pop(0)
    data = str(first_value)
    formatted_data = data.replace('.', ',')
    
    print(formatted_data)
    return formatted_data

# Extraction données 2M30
def extract_2M30(soup):
    table = soup.find('table', class_='metalinfo-table table-metal-prices')

    rows = soup.find_all('tr')
    second_row = rows[23]

    columns = second_row.find_all('td')
    fourth_column = columns[1]
    data = fourth_column.text.strip()
    formatted_data = data.replace(',', '').replace('.', ',')

    return formatted_data

# Extraction données 2B16
def extract_2B16(soup):
    """Extraire les données de la table Cookson et les ajouter au classeur Excel"""
    table = soup.find("table")
    rows = soup.find_all("tr")
    second_row = rows[26]

    # Trouver la quatrième colonne de la table dans la deuxième ligne
    columns = second_row.find_all("td")
    fourth_column = columns[1]

    # Extraire le texte de la quatrième colonne
    data = fourth_column.text.strip()
    formatted_data = data.replace(',', '').replace('.', ',')
    return formatted_data

# Extraction données 3ZN1
def extract_3ZN1(soup):
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
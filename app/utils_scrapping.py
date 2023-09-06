import configparser
from PyPDF2 import PdfReader
import time
from datetime import datetime, timedelta
from app.data_list import sites
import os
from .config import get_config_value, get_pdf_path, set_config_value
import json
from urllib.request import urlopen

config = configparser.ConfigParser()
config.read('config.ini')

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
            date = None

            # Date d'aujourd'hui
            today = datetime.today()

            # Date de la veille
            yesterday = today - timedelta(days=1)

            # Numéro de la semaine
            week_number = yesterday.isocalendar()[1]

            for line in lines:
                print(line)
                if "As of" in line.lower():
                    date = line.split("As Of")[-1].strip()

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
                date = f"Semaine {week_number}"
                return date, formatted_data
    except FileNotFoundError:
        print(f"Le fichier PDF '{name_pdf}' n'a pas été trouvé. Passage à autre chose.")
        date = None
        formatted_data = 'err'
        return date, formatted_data

# Extraction données Cookson pour 1AG1 (EL)
def extract_1AG1(soup):
    """Extraire les données de la table Cookson et les ajouter au classeur Excel"""
    table = soup.find("table")
    rows = soup.find_all("tr")
    second_row = rows[3]

    # Trouver la quatrième colonne de la table dans la deuxième ligne
    columns = second_row.find_all("td")
    last_column = columns[3]

    # Extraire la date de la première colonne du tbody
    tbody = soup.find('tbody')
    first_td_in_tbody = soup.find('td')
    date_day = first_td_in_tbody.text.strip()


    # Extraire le texte de la quatrième colonne
    data = last_column.text.strip()
    formatted_data = data.replace('€', '')
    date = date_day.replace("Cours de Londres du ", " ")
    return date, formatted_data

# Extraction données lbma pour 1AG2 (EL)
def extract_1AG2(soup):
    url = "https://prices.lbma.org.uk/json/silver.json?r=211497526"
    response = urlopen(url).read()
    data = json.loads(response)
    latest_prices = data[-1]
    first_value = latest_prices['v'].pop(0)
    data_value = latest_prices['d']

    date_object = datetime.strptime(data_value, '%Y-%m-%d')
    formatted_date = date_object.strftime('%d/%m/%Y')

    data = str(first_value)
    formatted_data = data.replace('.', ',')
    
    print(formatted_data)
    return formatted_date, formatted_data

# Extraction données pour 3AL1 (EL)
def extract_3AL1(soup):
    """Extraire les données de la table Cookson et les ajouter au classeur Excel"""

    # Trouver la date dans le tag <th class="number">
    date_tag = soup.find("th", class_="number")
    date_data_raw = date_tag.text.strip() if date_tag else "Date not found"

    # Conversion de la date du format "05. September 2023" à "05/09/2023"
    months = {
        'January': '01', 'February': '02', 'March': '03', 'April': '04', 'May': '05', 
        'June': '06', 'July': '07', 'August': '08', 'September': '09', 'October': '10',
        'November': '11', 'December': '12'
    }

    day, month_name, year = date_data_raw.replace('.', '').split()
    month_num = months.get(month_name, '00')  # Si le mois n'est pas trouvé, '00' est utilisé par défaut
    date_data = f"{day}/{month_num}/{year}"

    # Continuer avec la logique existante pour obtenir la donnée de la quatrième colonne
    table = soup.find("table")
    rows = table.find_all("tr")
    second_row = rows[6]
    columns = second_row.find_all("td")
    fourth_column = columns[1]
    data = fourth_column.text.strip()
    formatted_data = data.replace(',', '').replace('.', ',')

    return date_data, formatted_data

# Extraction données lbma pour 1AU2 (EL)
def extract_1AU2(soup):

    url = "https://prices.lbma.org.uk/json/gold_pm.json?r=666323974"
    response = urlopen(url).read()
    data = json.loads(response)
    latest_prices = data[-1]
    first_value = latest_prices['v'].pop(0)
    data_value = latest_prices['d']

    date_object = datetime.strptime(data_value, '%Y-%m-%d')
    formatted_date = date_object.strftime('%d/%m/%Y')

    data = str(first_value)
    formatted_data = data.replace('.', ',').replace(" ", "")
    
    print(formatted_data)
    return formatted_date, formatted_data


# Extraction données Cookson pour 1AU3 (EL)
def extract_1AU3(soup):
    """Extraire les données de la table Cookson et les ajouter au classeur Excel"""
    table = soup.find("table")
    rows = soup.find_all("tr")
    second_row = rows[2]

    # Extraire la date de la première colonne du tbody
    tbody = soup.find('tbody')
    first_td_in_tbody = soup.find('td')
    date_day = first_td_in_tbody.text.strip()

    # Trouver la quatrième colonne de la table dans la deuxième ligne
    columns = second_row.find_all("td")
    last_column = columns[3]

    # Extraire le texte de la quatrième colonne
    data = last_column.text.strip()
    data = data.replace(" ", "")
    formatted_data = data.replace('.', ',').replace('€', '').replace(' ', '')
    date = date_day.replace("Cours de Londres du ", " ")
    return date, formatted_data

# Extraction données 2B16
def extract_2B16(soup):
    """Extraire les données de la table Cookson et les ajouter au classeur Excel"""

    # Trouver la date dans le tag <th class="number">
    date_tag = soup.find("th", class_="number")
    date_data_raw = date_tag.text.strip() if date_tag else "Date not found"

    # Conversion de la date du format "05. September 2023" à "05/09/2023"
    months = {
        'January': '01', 'February': '02', 'March': '03', 'April': '04', 'May': '05', 
        'June': '06', 'July': '07', 'August': '08', 'September': '09', 'October': '10',
        'November': '11', 'December': '12'
    }

    day, month_name, year = date_data_raw.replace('.', '').split()
    month_num = months.get(month_name, '00')  # Si le mois n'est pas trouvé, '00' est utilisé par défaut
    date_data = f"{day}/{month_num}/{year}"

    table = soup.find("table")
    rows = soup.find_all("tr")
    second_row = rows[26]
    # Trouver la quatrième colonne de la table dans la deuxième ligne
    columns = second_row.find_all("td")
    fourth_column = columns[1]

    # Extraire le texte de la quatrième colonne
    data = fourth_column.text.strip()
    formatted_data = data.replace(',', '').replace('.', ',')
    return date_data, formatted_data

# Extraction données pour 3CU1 (EL)
def extract_3CU1(soup):
    """Extraire les données de la table Cookson et les ajouter au classeur Excel"""
    table = soup.find("table")
    rows = soup.find_all("tr")
    second_row = rows[1]


    # Trouver la quatrième colonne de la table dans la deuxième ligne
    columns = second_row.find_all("td")
    fourth_column = columns[1]
    # Récupérer la date de la première colonne
    first_column = columns[0]
    date_data_raw = first_column.text.strip()

    # Conversion de la date du format "05. September 2023" à "05/09/2023"
    months = {
        'January': '01', 'February': '02', 'March': '03', 'April': '04', 'May': '05', 
        'June': '06', 'July': '07', 'August': '08', 'September': '09', 'October': '10',
        'November': '11', 'December': '12'
    }

    day, month_name, year = date_data_raw.replace('.', '').split()
    month_num = months.get(month_name, '00')  # Si le mois n'est pas trouvé, '00' est utilisé par défaut
    date_data = f"{day}/{month_num}/{year}"

    # Extraire le texte de la quatrième colonne
    data = fourth_column.text.strip()
    formatted_data = data.replace(',', '').replace('.', ',')
    return date_data, formatted_data

# Extraction données pour 3CU3 (EL)
def extract_3CU3(soup):
    """Extraire les données de la table Cookson et les ajouter au classeur Excel"""
    table = soup.find("table")
    rows = soup.find_all("tr")
    second_row = rows[1]

    
    # Trouver la quatrième colonne de la table dans la deuxième ligne
    columns = second_row.find_all("td")
    fourth_column = columns[1]
    # Récupérer la date de la première colonne
    first_column = columns[0]
    date_data_raw = first_column.text.strip()
    # Conversion de la date du format "05. September 2023" à "05/09/2023"
    months = {
        'January': '01', 'February': '02', 'March': '03', 'April': '04', 'May': '05', 
        'June': '06', 'July': '07', 'August': '08', 'September': '09', 'October': '10',
        'November': '11', 'December': '12'
    }

    day, month_name, year = date_data_raw.replace('.', '').split()
    month_num = months.get(month_name, '00')  # Si le mois n'est pas trouvé, '00' est utilisé par défaut
    date_data = f"{day}/{month_num}/{year}"


    # Extraire le texte de la quatrième colonne
    data = fourth_column.text.strip()
    formatted_data = data.replace('.', ',')
    return date_data ,formatted_data

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
            date = None
            # Date d'aujourd'hui
            today = datetime.today()

            # Date de la veille
            yesterday = today - timedelta(days=1)

            # Numéro de la semaine
            week_number = yesterday.isocalendar()[1]

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
                date = f" Semaine {week_number}"
                return date, formatted_data
    except FileNotFoundError:
        print(f"Le fichier PDF '{name_pdf}' n'a pas été trouvé. Passage à autre chose.")
        date = None
        formatted_data = 'err'
        return date, formatted_data

# Extraction données 2M30
def extract_2M30(soup):

    # Trouver la table spécifiée
    table = soup.find('table', class_='metalinfo-table table-metal-prices')

    # Trouver toutes les lignes (tr) à l'intérieur de cette table
    rows = soup.find_all('tr')
    second_row = rows[23]

    # Trouver toutes les colonnes (td) de la ligne spécifiée
    columns = second_row.find_all('td')
    fourth_column = columns[1]
    data = fourth_column.text.strip()
    formatted_data = data.replace(',', '').replace('.', ',')
    # Trouver la date dans le tag <p class="date small">
    date_tag = soup.find("p", class_="date small")
    raw_date_data = date_tag.text.strip() if date_tag else "Date not found"

    # Convertir la date au format souhaité
    try:
        # Supprimer "Value from " pour obtenir seulement la date
        clean_date_data = raw_date_data.replace("Value from ", "")
        # Convertir la chaîne de date au format souhaité
        datetime_obj = datetime.strptime(clean_date_data, '%b %d, %Y')
        formatted_date = datetime_obj.strftime('%d/%m/%Y')
    except ValueError:
        formatted_date = "Invalid date format"

    return formatted_date, formatted_data

# Extraction données pour 2M37 (EL)
def extract_2M37(soup):
    """Extraire les données de la table Cookson et les ajouter au classeur Excel"""
    table = soup.find("table")
    rows = soup.find_all("tr")
    second_row = rows[1]

    # Trouver la quatrième colonne de la table dans la deuxième ligne
    columns = second_row.find_all("td")
    fourth_column = columns[1]
    # Récupérer la date de la première colonne
    first_column = columns[0]
    date_data_raw = first_column.text.strip()

    # Conversion de la date du format "05. September 2023" à "05/09/2023"
    months = {
        'January': '01', 'February': '02', 'March': '03', 'April': '04', 'May': '05', 
        'June': '06', 'July': '07', 'August': '08', 'September': '09', 'October': '10',
        'November': '11', 'December': '12'
    }

    day, month_name, year = date_data_raw.replace('.', '').split()
    month_num = months.get(month_name, '00')  # Si le mois n'est pas trouvé, '00' est utilisé par défaut
    date_data = f"{day}/{month_num}/{year}"

    # Extraire le texte de la quatrième colonne
    data = fourth_column.text.strip()
    formatted_data = data.replace('.', ',')
    return date_data, formatted_data

# Extraction données pour 3NI1 (EL)
def extract_3NI1(soup):
    """Extraction NICKEL Ligne 2, Valeur Colonne 3"""
    def reformat_date(date_str):
        day, month, year = date_str.split(".")
        year = year[:4]
        return f"{day}/{month}/{year}"
    table = soup.find('table', class_='table table-condensed table-hover table-striped')

    rows = soup.find_all('tr')
    second_row = rows[2]


    columns = second_row.find_all('td')
    fourth_column = columns[2]
    # Récupérer la date de la première colonne
    first_column = columns[3]
    date_data = first_column.text.strip()

    data = fourth_column.text.strip()
    formatted_data = data.replace('.', '').replace('¹', '')
    date_data = reformat_date(date_data)
    return date_data, formatted_data

# Extraction données pour 3SN1 (EL)
def extract_3SN1(soup):
    """Extraction ETAIN Ligne 3, Valeur Colonne 3"""
    def reformat_date(date_str):
        day, month, year = date_str.split(".")
        year = year[:4]
        return f"{day}/{month}/{year}"
    
    table = soup.find('table', class_='')
    rows = soup.find_all('tr')
    second_row = rows[3]

    columns = second_row.find_all('td')
    fourth_column = columns[2]
    # Récupérer la date de la première colonne
    first_column = columns[3]
    date_data = first_column.text.strip()

    data = fourth_column.text.strip()

    formatted_data = data.replace('.', '').replace('¹', '')
    date_data = reformat_date(date_data)
    return date_data, formatted_data

# Extraction données 3ZN1
def extract_3ZN1(soup):
    """Extraire les données de la table Cookson et les ajouter au classeur Excel"""
    table = soup.find("table")
    rows = soup.find_all("tr")
    second_row = rows[1]

    # Trouver la quatrième colonne de la table dans la deuxième ligne
    columns = second_row.find_all("td")
    fourth_column = columns[1]
    # Récupérer la date de la première colonne
    first_column = columns[0]
    date_data_raw = first_column.text.strip()

    # Conversion de la date du format "05. September 2023" à "05/09/2023"
    months = {
        'January': '01', 'February': '02', 'March': '03', 'April': '04', 'May': '05', 
        'June': '06', 'July': '07', 'August': '08', 'September': '09', 'October': '10',
        'November': '11', 'December': '12'
    }

    day, month_name, year = date_data_raw.replace('.', '').split()
    month_num = months.get(month_name, '00')  # Si le mois n'est pas trouvé, '00' est utilisé par défaut
    date_data = f"{day}/{month_num}/{year}"

    # Extraire le texte de la quatrième colonne
    data = fourth_column.text.strip()
    formatted_data = data.replace(',', '').replace('.', ',')
    return date_data, formatted_data

# Extraction données pour 1AG3 (EL) Deja importé
# def extract_1AG3(soup):
#     """Extraire les données de la table Cookson et les ajouter au classeur Excel"""
#     table = soup.find("table")
#     rows = table.find_all("tr")
#     second_row = rows[1]

#     columns = second_row.find_all("td")
    
#     # Récupérer la date de la première colonne
#     first_column = columns[0]
#     date_data = first_column.text.strip()
    
#     # Récupérer la valeur de la quatrième colonne
#     fourth_column = columns[1]
#     data = fourth_column.text.strip()
#     formatted_data = data.replace('.', ',')

#     # Retourner la date et la valeur de la quatrième colonne
#     return date_data, formatted_data


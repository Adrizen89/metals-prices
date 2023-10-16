import configparser
from PyPDF2 import PdfReader
import time
from datetime import datetime, timedelta
from app.data_list import sites
import os
from .config import get_config_value, get_pdf_path, set_config_value
import json
from urllib.request import urlopen
import locale

config = configparser.ConfigParser()
config.read('../config.ini')

def extract_2360(soup, start_date=None, end_date=None):
    """Extraire les données de la table Materion et les ajouter au classeur Excel"""

    pdf_path = get_config_value('SETTINGS', 'pdf_path')
    name_pdf = get_config_value('SETTINGS', 'name_pdf')

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
def extract_1AG1(soup, start_date=None, end_date=None):
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
def extract_1AG2(soup, start_date=None, end_date=None):
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
def extract_3AL1(soup, start_date=None, end_date=None):
    """Extraire les données de la table AL et les ajouter au classeur Excel"""
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

# Extraction données lbma pour 1AU2 (EL)
def extract_1AU2(soup, start_date = None, end_date = None):

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
def extract_1AU3(soup, start_date=None, end_date=None):
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
def extract_2B16(soup, start_date=None, end_date=None):
    try:
        rows = soup.find_all("tr")[1:]
        months = {
            'January': '01', 'February': '02', 'March': '03', 'April': '04', 'May': '05', 
            'June': '06', 'July': '07', 'August': '08', 'September': '09', 'October': '10',
            'November': '11', 'December': '12'
        }

        data_list = []

        for row in rows:
            columns = row.find_all("td")

            if len(columns) < 2:
                continue

            # Récupérer et formater la date
            date_data_raw = columns[0].text.strip()
            day, month_name, year = date_data_raw.replace('.', '').split()
            month_num = months.get(month_name, '00')
            date_data_str = f"{day}/{month_num}/{year}"

            # Convertir la date en objet datetime pour la comparaison
            date_data = datetime.strptime(date_data_str, "%d/%m/%Y").date()

            # Récupérer et formater la valeur
            data = columns[1].text.strip()
            formatted_data = data.replace(',', '').replace('.', ',')

            # Vérifier si la date est dans la plage de dates spécifiée
            if (start_date and date_data < start_date) or (end_date and date_data > end_date):
                continue

            data_list.append((date_data_str, formatted_data))

        # Retourner la liste complète si start_date et end_date sont spécifiés, sinon retourner le premier élément
        return data_list if start_date and end_date else (data_list[0] if data_list else None)

    except Exception as e:
        return f"Erreur : {e}"


# Extraction données pour 3CU1 (EL)
def extract_3CU1(soup, start_date=None, end_date=None):
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
def extract_3CU3(soup, start_date=None, end_date=None):
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

def extract_2CUB(soup, start_date=None, end_date=None):
    """Extraire les données de la table Materion et les ajouter au classeur Excel"""

    pdf_path = get_config_value('SETTINGS', 'pdf_path')
    name_pdf = get_config_value('SETTINGS', 'name_pdf')

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
def extract_2M30(soup, start_date=None, end_date=None):

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
    locale.setlocale(locale.LC_TIME, "en_US.UTF-8")
    try:
        # Supprimer "Value from " pour obtenir seulement la date
        clean_date_data = raw_date_data.replace("Value from ", "").strip()
        print(f'clean data : "{clean_date_data}"')
        # Convertir la chaîne de date au format souhaité
        datetime_obj = datetime.strptime(clean_date_data, '%b %d, %Y')
        formatted_date = datetime_obj.strftime('%d/%m/%Y')
    except ValueError:
        formatted_date = "Invalid date format"

    return formatted_date, formatted_data

# Extraction données pour 2M37 (EL)
def extract_2M37(soup, start_date=None, end_date=None):
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
def extract_3NI1(soup, start_date=None, end_date=None):
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
def extract_3SN1(soup, start_date=None, end_date=None):
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
def extract_3ZN1(soup, checkbox_state=False, start_date=None, end_date=None):
    """Extraire les données de la table Cookson et les ajouter au classeur Excel"""

    months = {
        'January': '01', 'February': '02', 'March': '03', 'April': '04', 'May': '05', 
        'June': '06', 'July': '07', 'August': '08', 'September': '09', 'October': '10',
        'November': '11', 'December': '12'
    }

    table = soup.find("table")
    rows = soup.find_all("tr")
    
    if checkbox_state and start_date and end_date:

        extracted_values = []
        
        for row in rows[1:]:  # Ignorer l'en-tête
            columns = row.find_all("td")

            print(f"Processing row with {len(columns)} columns")
            if len(columns) < 2:  # Ajustez ce nombre en fonction de vos besoins
                continue
            
            date_data_raw = columns[0].text.strip()

            
            if len(columns) >= 1:
                date_data_raw = columns[0].text.strip()
                
            
                # Conversion de la date du format "05. September 2023" à "05/09/2023"
                day, month_name, year = date_data_raw.replace('.', '').split()
                month_num = months.get(month_name, '00')  # Si le mois n'est pas trouvé, '00' est utilisé par défaut
                date_data = f"{day}/{month_num}/{year}"
            
                date_data_obj = datetime.strptime(date_data, "%d/%m/%Y").date()
            
                if start_date <= date_data_obj <= end_date:
                    fourth_column = columns[1]
                    data = fourth_column.text.strip()
                    formatted_data = data.replace(',', '').replace('.', ',')
                    extracted_values.append((date_data, formatted_data))
        return extracted_values
                
    else:
        # Si la checkbox n'est pas cochée ou si les dates ne sont pas fournies, récupérer la première valeur
        second_row = rows[1]
        columns = second_row.find_all("td")
        fourth_column = columns[1]
        date_data_raw = columns[0].text.strip()
        
        # Conversion de la date et extraction des données comme dans votre code original
        # ...
        day, month_name, year = date_data_raw.replace('.', '').split()
        month_num = months.get(month_name, '00')
        date_data = f"{day}/{month_num}/{year}"
        
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


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
import re
import requests

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
def extract_1AG2(soup, checkbox_state = False, start_date=None, end_date=None):
    url = "https://prices.lbma.org.uk/json/silver.json?r=211497526"
    response = urlopen(url).read()
    data = json.loads(response)

    if checkbox_state and start_date and end_date:

        extracted_values = []


        for entry in data:
            entry_date_str = entry.get("d")
            entry_date = datetime.strptime(entry_date_str, "%Y-%m-%d")
            date_data_obj = entry_date.date()
            
            if start_date <= date_data_obj <= end_date:
                value = entry['v'].pop(0)
                if value:
                    extracted_values.append((date_data_obj.strftime('%d/%m/%Y'), value))
        extracted_values.reverse()
        return extracted_values
    else:
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
def extract_3AL1(soup, checkbox_state=False, start_date=None, end_date=None):
    """Extraire les données de la table AL et les ajouter au classeur Excel"""
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
            
            if len(columns) < 2:  # nombre de colonne pour ligne séparatrice
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
        
        # Conversion de la date et extraction des données
        day, month_name, year = date_data_raw.replace('.', '').split()
        month_num = months.get(month_name, '00')
        date_data = f"{day}/{month_num}/{year}"
        
        data = fourth_column.text.strip()
        formatted_data = data.replace(',', '').replace('.', ',')
        return date_data, formatted_data

# Extraction données lbma pour 1AU2 (EL)
def extract_1AU2(soup, checkbox_state = False, start_date = None, end_date = None):

    url = "https://prices.lbma.org.uk/json/gold_pm.json?r=666323974"
    response = urlopen(url).read()
    data = json.loads(response)

    if checkbox_state and start_date and end_date:

        extracted_values = []


        for entry in data:
            entry_date_str = entry.get("d")
            entry_date = datetime.strptime(entry_date_str, "%Y-%m-%d")
            date_data_obj = entry_date.date()
            
            if start_date <= date_data_obj <= end_date:
                value = entry['v'].pop(0)
                if value:
                    extracted_values.append((date_data_obj.strftime('%d/%m/%Y'), value))
        extracted_values.reverse()
        return extracted_values

    else:
        latest_prices = data[-1]
        first_value = latest_prices['v'].pop(0)
        date_value = latest_prices['d']

        date_object = datetime.strptime(date_value, '%Y-%m-%d')
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
def extract_2B16(soup, checkbox_state=False, start_date=None, end_date=None):
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

            if len(columns) < 2:  # nombre de colonne pour ligne séparatrice
                continue
            
            date_data_raw = columns[0].text.strip()

            
            if len(columns) >= 1: # On vérifie si le nombre de colonne est plus ou égal à 1
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
        
        # Conversion de la date et extraction des données
        day, month_name, year = date_data_raw.replace('.', '').split()
        month_num = months.get(month_name, '00')
        date_data = f"{day}/{month_num}/{year}"
        
        data = fourth_column.text.strip()
        formatted_data = data.replace(',', '').replace('.', ',')
        return date_data, formatted_data


# Extraction données pour 3CU1 (EL)
def extract_3CU1(soup, checkbox_state=False, start_date=None, end_date=None):
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

            if len(columns) < 2:  # nombre de colonne pour ligne séparatrice
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
        
        # Conversion de la date et extraction des données
        day, month_name, year = date_data_raw.replace('.', '').split()
        month_num = months.get(month_name, '00')
        date_data = f"{day}/{month_num}/{year}"
        
        data = fourth_column.text.strip()
        formatted_data = data.replace(',', '').replace('.', ',')
        return date_data, formatted_data

# Extraction données pour 3CU3 (EL)
def extract_3CU3(soup, checkbox_state = False, start_date=None, end_date=None):
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

            if len(columns) < 2:  # nombre de colonne pour ligne séparatrice
                continue
            
            date_data_raw = columns[0].text.strip()

            
            if len(columns) >= 1: # On vérifie si le nombre de colonne est plus ou égal à 1
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
        
        # Conversion de la date et extraction des données
        day, month_name, year = date_data_raw.replace('.', '').split()
        month_num = months.get(month_name, '00')
        date_data = f"{day}/{month_num}/{year}"
        
        data = fourth_column.text.strip()
        formatted_data = data.replace(',', '').replace('.', ',')
        return date_data, formatted_data

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
def extract_2M30(soup, checkbox_state = False, start_date=None, end_date=None):
    url = 'https://www.wieland.com/en/ajax/metal-prices/general'
    # Trouver la table spécifiée
    response = urlopen(url).read()
    dat = json.loads(response)


    if checkbox_state and start_date and end_date:
        response = requests.get(url)
        json_data = response.json()

        # Vérification de la présence des clés nécessaires
        if 'content' in json_data and 'chart' in json_data['content']:
            chart_data = json_data['content']['chart']

            if 'labels' in chart_data and 'data' in chart_data:

                # Date
                labels = chart_data['labels']
                # Valeurs
                data = chart_data['data']
                
                # Maintenant, vous pouvez itérer sur les labels et les données
                extracted_values = []
    
                for label, value in zip(labels, data):
                    # Convertir la date du label en objet datetime
                    label_date = datetime.strptime(label, '%m/%d/%Y')
                    label_date = label_date.date()
                    # Vérifier si la date du label est entre start_date et end_date
                    if start_date <= label_date <= end_date:
                        extracted_values.append((label, value))
                        
                return extracted_values
            else:
                print("Les clés 'labels' et/ou 'data' ne sont pas présentes dans les données.")
        else:
            print("Les clés 'content' et/ou 'chart' ne sont pas présentes dans les données.")
                        

    else:
        table = soup.find('table', class_='metalinfo-table')
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
def extract_2M37(soup, checkbox_state = False, start_date=None, end_date=None):
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

            if len(columns) < 2:  # nombre de colonne pour ligne séparatrice
                continue
            
            date_data_raw = columns[0].text.strip()

            
            if len(columns) >= 1: # On vérifie si le nombre de colonne est plus ou égal à 1
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
        
        # Conversion de la date et extraction des données
        day, month_name, year = date_data_raw.replace('.', '').split()
        month_num = months.get(month_name, '00')
        date_data = f"{day}/{month_num}/{year}"
        
        data = fourth_column.text.strip()
        formatted_data = data.replace(',', '').replace('.', ',')
        return date_data, formatted_data

# Extraction données pour 3NI1 (EL)
def extract_3NI1(soup, checkbox_state = False, start_date=None, end_date=None):
    """Extraction NICKEL Ligne 2, Valeur Colonne 3"""
    tables = soup.find_all('table', class_='table table-condensed table-hover table-striped')
    rows = tables[1].find_all("tr")

    if checkbox_state and start_date and end_date:
        extracted_values = []

        for row in rows[1:]:  # Ignorer l'en-tête
            columns = row.find_all("td")

            if len(columns) >= 1:
                date_data_raw = columns[0].text.strip()
                
                # Utiliser une expression régulière pour extraire une date valide
                date_match = re.search(r"(\d{2}\.\d{2}\.\d{4})", date_data_raw)
                if date_match:
                    date_data_raw = date_match.group(1)
                else:
                    continue  # Passer à la prochaine ligne si aucune date valide n'est trouvée

                try:
                    date_obj = datetime.strptime(date_data_raw, '%d.%m.%Y')
                    
                    date_data_obj = date_obj.date()
                    
                    if start_date <= date_data_obj <= end_date:
                        value_data = columns[1].text.strip().replace(',', '').replace('.', ',')
                        extracted_values.append((date_obj.strftime('%d/%m/%Y'), value_data))
                except ValueError as e:
                    print(f"Erreur lors de la conversion de la date: {e}")
        extracted_values.reverse()
        return extracted_values

    else:
    # S'assurer qu'il y a au moins deux tables et sélectionner la deuxième
        if len(tables) > 1:
            table = tables[1]
            
            # Obtenir la première ligne de la table (en excluant l'en-tête)
            last_row = table.find_all('tr')[42] if table else None
            print(last_row)
            if last_row:
                columns = last_row.find_all('td')
                print(columns)
                # S'assurer qu'il y a au moins deux colonnes
                if len(columns) >= 2:
                    # Extraire et nettoyer la date et la valeur
                    date_str = columns[0].text.strip()
                    print(f"DATE :", date_str)
                    value_str = columns[1].text.strip()
                    print(f"VALUE :", value_str)
                    
                    # Convertir la date au format d/m/Y
                    try:
                        date_obj = datetime.strptime(date_str, '%d.%m.%Y')
                        formatted_date = date_obj.strftime('%d/%m/%Y')
                    except ValueError:
                        print(f"Erreur de format de date : {date_str}")
                        formatted_date = date_str  # Garder la date telle quelle si la conversion échoue
                    print(formatted_date, value_str)
                    return formatted_date, value_str
                else:
                    print("Les colonnes de date et de valeur sont manquantes.")
                    return None, None
            else:
                print("Aucune ligne de données trouvée dans la table.")
                return None, None
        else:
            print("La deuxième table est introuvable.")
            return None, None


# Extraction données pour 3SN1 (EL)
def extract_3SN1(soup, checkbox_state = None, start_date=None, end_date=None):
    """Extraction ETAIN Ligne 3, Valeur Colonne 3"""
    tables = soup.find_all('table', class_='table table-condensed table-hover table-striped')
    rows = tables[1].find_all("tr")

    if checkbox_state and start_date and end_date:
        extracted_values = []

        for row in rows[1:]:  # Ignorer l'en-tête
            columns = row.find_all("td")

            if len(columns) >= 1:
                date_data_raw = columns[0].text.strip()
                
                # Utiliser une expression régulière pour extraire une date valide
                date_match = re.search(r"(\d{2}\.\d{2}\.\d{4})", date_data_raw)
                if date_match:
                    date_data_raw = date_match.group(1)
                else:
                    continue  # Passer à la prochaine ligne si aucune date valide n'est trouvée

                try:
                    date_obj = datetime.strptime(date_data_raw, '%d.%m.%Y')
                    
                    date_data_obj = date_obj.date()
                    
                    if start_date <= date_data_obj <= end_date:
                        value_data = columns[1].text.strip().replace(',', '').replace('.', ',')
                        extracted_values.append((date_obj.strftime('%d/%m/%Y'), value_data))
                except ValueError as e:
                    print(f"Erreur lors de la conversion de la date: {e}")
        extracted_values.reverse()
        return extracted_values

    else:
    # S'assurer qu'il y a au moins deux tables et sélectionner la deuxième
        if len(tables) > 1:
            table = tables[1]
            
            # Obtenir la première ligne de la table (en excluant l'en-tête)
            last_row = table.find_all('tr')[42] if table else None
            print(last_row)
            if last_row:
                columns = last_row.find_all('td')
                print(columns)
                # S'assurer qu'il y a au moins deux colonnes
                if len(columns) >= 2:
                    # Extraire et nettoyer la date et la valeur
                    date_str = columns[0].text.strip()
                    print(f"DATE :", date_str)
                    value_str = columns[1].text.strip()
                    print(f"VALUE :", value_str)
                    
                    # Convertir la date au format d/m/Y
                    try:
                        date_obj = datetime.strptime(date_str, '%d.%m.%Y')
                        formatted_date = date_obj.strftime('%d/%m/%Y')
                    except ValueError:
                        print(f"Erreur de format de date : {date_str}")
                        formatted_date = date_str  # Garder la date telle quelle si la conversion échoue
                    print(formatted_date, value_str)
                    return formatted_date, value_str
                else:
                    print("Les colonnes de date et de valeur sont manquantes.")
                    return None, None
            else:
                print("Aucune ligne de données trouvée dans la table.")
                return None, None
        else:
            print("La deuxième table est introuvable.")
            return None, None

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

            if len(columns) < 2:  # nombre de colonne pour ligne séparatrice
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
        print("3ZN1 :",extracted_values)
        return extracted_values
                
    else:
        # Si la checkbox n'est pas cochée ou si les dates ne sont pas fournies, récupérer la première valeur
        second_row = rows[1]
        columns = second_row.find_all("td")
        fourth_column = columns[1]
        date_data_raw = columns[0].text.strip()
        
        # Conversion de la date et extraction des données
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


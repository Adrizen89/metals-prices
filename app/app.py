import tkinter as tk
from tkinter import filedialog
import configparser
from bs4 import BeautifulSoup
import requests
from .config import get_config_value
from .config import set_config_value
from .data_list import sites as sites
import utils_scrapping as scrapping
from .utils_pdf import download_pdf
from .utils_pdf import delete_pdfs
import datetime
from openpyxl import load_workbook
import sys
from io import StringIO
from ressources.colors import bg_color, bg_color_light, bg_color, text_light, text_medium, text_dark


config = configparser.ConfigParser()
config.read('config.ini')

now = datetime.datetime.now().date()
date = now.strftime("%d/%m/%Y")

class MyApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.geometry("900x600")
        self.title("Cours des métaux")
        self.resizable(False, False)
        self.configure(bg="#0D1F26")

        # Création frame pour chemins d'accès
        left_frame = tk.Frame(self, bg=bg_color)
        right_frame = tk.Frame(self, bg=text_light)
        excel_frame = tk.Frame(left_frame, bg=bg_color, width=50)
        pdf_frame = tk.Frame(left_frame, bg=bg_color, width=50)
        driver_chrome_frame = tk.Frame(left_frame, bg=bg_color, width=50)
        name_pdf_frame = tk.Frame(left_frame, bg=bg_color, width=50)

        self.output_text = tk.Text(right_frame, bg='white', state='disabled', width=50)
        self.output_text.pack(side='top', fill='both', expand=True)

        self.excel_path = get_config_value("main", "excel_path")
        self.pdf_path = get_config_value("main", "pdf_path")
        self.driver_chrome_path = get_config_value("main", "path_driver_chrome")
        self.name_pdf_path = get_config_value("main", "name_pdf")


        # Création des éléments de la fenêtre
        title_label = tk.Label(self, text="Diehl Augé Découpage", font=("Inter", 32, 'bold'), fg=text_medium, bg=bg_color)
        launch_button = tk.Button(left_frame, text="Lancer", command=lambda: self.lancer_script(sites=sites), width=10, height=1, bg=text_medium, fg=bg_color, font=('Inter', 16))

        excel_label = tk.Label(excel_frame, text="Fichier Excel :", font=("Inter", 12, 'bold'), fg=text_medium, bg=bg_color)
        self.excel_label = tk.Label(excel_frame, text=self.excel_path, fg=bg_color, bg=text_medium, width=50)
        excel_button = tk.Button(excel_frame, text="Parcourir...", command=self.choose_excelfile, width=10, height=1, bg=text_dark, fg=text_light)

        driver_chrome_label = tk.Label(driver_chrome_frame, text="Fichier Driver Chrome :", font=("Inter", 12, 'bold'), fg=text_medium, bg=bg_color)
        self.driver_chrome_label = tk.Label(driver_chrome_frame, text=self.driver_chrome_path, fg=bg_color, bg=text_medium, width=50)
        driver_chrome_button = tk.Button(driver_chrome_frame, text="Parcourir...", command=self.choose_driver_chrome, width=10, height=1, bg=text_dark, fg=text_light)

        pdf_label = tk.Label(pdf_frame, text="Fichier PDF :", font=("Inter", 12, 'bold'), fg=text_medium, bg=bg_color)
        self.pdf_label = tk.Label(pdf_frame, text=self.pdf_path, fg=bg_color, bg=text_medium, width=50)
        pdf_button = tk.Button(pdf_frame, text="Parcourir...", command=self.choose_pdffile, width=10, height=1, bg=text_dark, fg=text_light)

        name_pdf_label = tk.Label(name_pdf_frame, text='Non du fichier PDF', font=("Inter", 12, 'bold'), fg=text_medium, bg=bg_color)
        self.name_pdf_label = tk.Entry(name_pdf_frame, width=50, bg=text_light, fg=bg_color)
        self.name_pdf_label.insert(0, self.name_pdf_path)
        self.name_pdf_label.config(state="readonly", bg=text_medium, fg=bg_color, width=60)
        modify_name_button = tk.Button(name_pdf_frame, text="Modifier", command=self.make_entry_editable, width=10, height=1, bg=text_dark, fg=text_light)
        save_name_button = tk.Button(name_pdf_frame, text="Sauvegarder", command=self.saves_changes_name_pdf, width=10, height=1, bg=text_dark, fg=text_light)

        # Placement des éléments dans la fenêtre
        title_label.pack(side=tk.TOP, padx=10, pady=10)
        launch_button.pack(side=tk.BOTTOM, padx=10,pady=10)

        right_frame.pack(side=tk.RIGHT, padx=10, pady=10)
        excel_frame.pack(side=tk.TOP, padx=10, pady=10)
        pdf_frame.pack(side=tk.TOP, padx=10, pady=10)
        driver_chrome_frame.pack(side=tk.TOP, padx=10, pady=10)
        name_pdf_frame.pack(side=tk.TOP, padx=10, pady=10)
        left_frame.pack(side=tk.LEFT, padx=10, pady=10)

        excel_label.pack(side=tk.TOP, padx=10, pady=5)
        self.excel_label.pack(side=tk.TOP, padx=10, pady=2)
        excel_button.pack(side=tk.BOTTOM, padx=10, pady=2)

        driver_chrome_label.pack(side=tk.TOP, padx=10, pady=5)
        self.driver_chrome_label.pack(side=tk.TOP, padx=10, pady=2)
        driver_chrome_button.pack(side=tk.BOTTOM, padx=10, pady=2)

        pdf_label.pack(side=tk.TOP, padx=10, pady=5)
        self.pdf_label.pack(side=tk.TOP, padx=10, pady=2)
        pdf_button.pack(side=tk.BOTTOM, padx=10, pady=2)

        name_pdf_label.pack(side=tk.TOP, padx=10, pady=5)
        self.name_pdf_label.pack(side=tk.TOP, padx=10, pady=2)
        modify_name_button.pack(side=tk.LEFT, padx=10, pady=2)
        save_name_button.pack(side=tk.RIGHT, padx=10, pady=2)

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
            self.excel_label.config(text=self.excel_path.name)
            set_config_value('main', 'excel_path', self.excel_path.name)
            self.save_config
    
    def choose_driver_chrome(self):
        driver_chrome_path = filedialog.askopenfile()
        if driver_chrome_path:
            self.driver_chrome_path = driver_chrome_path
            self.driver_chrome_label.config(text=self.driver_chrome_path.name)
            set_config_value('main', 'path_driver_chrome', self.driver_chrome_path.name)
            self.save_config

    def choose_pdffile(self):
        pdf_path = filedialog.askdirectory()
        if pdf_path:
            self.pdf_path = pdf_path
            self.pdf_label.config(text=self.pdf_path)
            set_config_value('main', 'pdf_path', self.pdf_path)
            self.save_config
    
    def make_entry_editable(self):
        self.name_pdf_label.config(state='normal')

    def saves_changes_name_pdf(self):
        new_text = self.name_pdf_label.get()
        if new_text != config.get('main', 'name_pdf'):
            set_config_value('main', 'name_pdf', new_text)
            self.name_pdf_label.config(state='readonly')

    def save_config(self):

        # Vérification des changements dans la configuration
        changes = False

        if self.excel_path != config.get('main', 'excel_path'):
            config.set('main', 'excel_path', self.excel_path.name)
            changes = True

        if self.driver_chrome_path != config.get('main', 'path_driver_chrome'):
            config.set('main', 'path_driver_chrome', self.driver_chrome_path.name)
            changes = True

        if self.pdf_path != config.get('main', 'pdf_path'):
            config.set('main', 'pdf_path', self.pdf_path)
            changes = True
        
        new_text = self.name_pdf_label.get()
        if new_text != config.get('main', 'name_pdf'):
            config.set('main', 'name_pdf', new_text)
            changes = True

        # Enregistrement des valeurs dans la configuration si des modifications ont été détectées
        if changes:
            with open("config.ini", "w") as configfile:
                config.write(configfile)

        # Fermeture de l'application
        self.destroy()

    def lancer_script(self, sites):
        old_stdout = sys.stdout
        sys.stdout = mystdout = StringIO()
        wb = load_workbook(self.excel_path)

        for site in sites:
            response = requests.get(site['url'])
            soup = BeautifulSoup(response.content, "html.parser")
            data_extraction_function_name = site['func']
            if hasattr(scrapping, data_extraction_function_name):
                if site['src'] == 'pdf':
                    download_pdf(response, site['name_pdf'], self.pdf_path)
                else:
                    print('')

                data_extraction_function = getattr(scrapping, data_extraction_function_name)
                data = data_extraction_function(soup)

                sheet = wb[site["name"]]
                row_number = sheet.max_row +1
                sheet.cell(row = row_number, column = 1, value = date)
                sheet.cell(row = row_number, column = 2, value = data)
                sheet.cell(row = row_number, column = 3, value = site['devise'])
                sheet.cell(row = row_number, column = 4, value = site['unit'])
                print (f"Valeur pour le site {site['name']} : {data}")
                sys.stdout = old_stdout
                output = mystdout.getvalue()
                self.update_output(output)

                wb.save(self.excel_path)
            else:
                print(f'Aucune fonction d\'extraction de données trouvées')
            
            
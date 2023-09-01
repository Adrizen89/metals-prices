import tkinter as tk
from tkinter import filedialog
import configparser
from bs4 import BeautifulSoup
import requests
from requests.exceptions import RequestException
from .config import get_config_value, get_pdf_path, set_config_value
from .data_list import sites as sites
import app.utils_scrapping as scrapping
from .utils_pdf import download_pdf, delete_pdfs
import datetime
from openpyxl import load_workbook, Workbook
import sys
import os
import subprocess
from io import StringIO
from ressources.colors import bg_color, bg_color_light, bg_color, text_light, text_medium, text_dark
import tkinter.messagebox as messagebox
from app.utils_format import check_and_return_value

config = configparser.ConfigParser()
config.read('config.ini')

now = datetime.datetime.now().date()
date = now.strftime("%d/%m/%Y")

class MyApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.geometry("900x620")
        self.title("Cours des métaux")
        self.resizable(False, False)
        self.configure(bg="#0D1F26")


        # Création frame pour chemins d'accès
        left_frame = tk.Frame(self, bg=bg_color)
        right_frame = tk.Frame(self, bg=text_light)
        excel_frame = tk.Frame(left_frame, bg=bg_color, width=50)
        pdf_frame = tk.Frame(left_frame, bg=bg_color, width=50)
        name_pdf_frame = tk.Frame(left_frame, bg=bg_color, width=50)

        # Modification: Ajout d'un Scrollbar pour le widget Text
        scrollbar = tk.Scrollbar(right_frame, orient="vertical")
        self.output_text = tk.Text(right_frame, bg='white', state='disabled', width=50, yscrollcommand=scrollbar.set)
        self.output_text.pack(side='left', fill='both', expand=True)
        scrollbar.config(command=self.output_text.yview)
        scrollbar.pack(side='right', fill='y')


        self.excel_path = get_config_value("main", "excel_path")
        self.pdf_path = get_config_value("main", "pdf_path")
        self.name_pdf_path = get_config_value("main", "name_pdf")

        self.excel_path_var = tk.StringVar()
        self.excel_path_var.set(self.excel_path)

        self.pdf_path = get_pdf_path()

        # Création des éléments de la fenêtre
        title_label = tk.Label(self, text="Diehl Augé Découpage", font=("Tahoma", 32, 'bold'), fg=text_medium, bg=bg_color)
        launch_button = tk.Button(left_frame, text="Lancer", command=lambda: self.lancer_script(sites=sites), width=10, height=1, bg=text_medium, fg=bg_color, font=('Tahoma', 16))

        excel_label = tk.Label(excel_frame, text="Fichier Excel :", font=("Tahoma", 12, 'bold'), fg=text_medium, bg=bg_color)
        self.excel_label = tk.Label(excel_frame, textvariable=self.excel_path_var, fg=bg_color, bg=text_medium, width=50)
        excel_button = tk.Button(excel_frame, text="Parcourir...", command=self.choose_excelfile, width=10, height=1, bg=text_dark, fg=text_light)
        open_excel_button = tk.Button(excel_frame, text="Ouvrir", command=self.open_excel, width=10, height=1, bg=text_dark, fg=text_light)

        pdf_label = tk.Label(pdf_frame, text="Fichier PDF :", font=("Tahoma", 12, 'bold'), fg=text_medium, bg=bg_color)
        self.pdf_label = tk.Label(pdf_frame, text=self.pdf_path, fg=bg_color, bg=text_medium, width=50)
        pdf_button = tk.Button(pdf_frame, text="Parcourir...", command=self.choose_pdffile, width=10, height=1, bg=text_dark, fg=text_light)

        name_pdf_label = tk.Label(name_pdf_frame, text='Nom du fichier PDF', font=("Tahoma", 12, 'bold'), fg=text_medium, bg=bg_color)
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
        name_pdf_frame.pack(side=tk.TOP, padx=10, pady=10)
        left_frame.pack(side=tk.LEFT, padx=10, pady=10)

        excel_label.pack(side=tk.TOP, padx=10, pady=5)
        self.excel_label.pack(side=tk.TOP, padx=10, pady=2)
        excel_button.pack(side=tk.LEFT, padx=10, pady=2)
        open_excel_button.pack(side=tk.RIGHT, padx=10, pady=10)


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

    def open_excel(self):
        try:
            subprocess.run(["start", self.excel_path], shell=True, check=True)
        except subprocess.CalledProcessError as e:
            messagebox.showerror("Erreur", f"Impossible d'ouvrir le fichier Excel: {e}")


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
        if new_text != get_config_value('main', 'name_pdf'):
            set_config_value('main', 'name_pdf', new_text)
            self.name_pdf_label.config(state='readonly')

    def save_config(self):

        # Vérification des changements dans la configuration
        changes = False

        if self.excel_path != get_config_value('main', 'excel_path'):
            set_config_value('main', 'excel_path', self.excel_path.name)
            changes = True

        if self.pdf_path != get_config_value('main', 'pdf_path'):
            set_config_value('main', 'pdf_path', self.pdf_path)
            changes = True
        
        new_text = self.name_pdf_label.get()
        if new_text != get_config_value('main', 'name_pdf'):
            set_config_value('main', 'name_pdf', new_text)
            changes = True

        # # Enregistrement des valeurs dans la configuration si des modifications ont été détectées
        # if changes:
        #     with open("config.ini", "w") as configfile:
        #         config.write(configfile)

        # Fermeture de l'application
        self.destroy()

    def lancer_script(self, sites):
        old_stdout = sys.stdout
        sys.stdout = mystdout = StringIO()

        replaced_values = {}
        replaced_value_count = 0

        config_excel_path = get_config_value("main", "excel_path")
        config_pdf_path = get_config_value("main", "pdf_path")

        # Vérifiez si l'une des valeurs a été modifiée
        if (self.excel_path != config_excel_path or
            self.pdf_path != config_pdf_path):
        
            messagebox.showerror("Attention !", "Un ou plusieurs a été modifié. Veuillez redémarrer l'application.\n Merci !")
            return

        if not self.excel_path or not os.path.exists(self.excel_path):
            self.excel_path = os.path.join(os.getcwd(), "metals_prices.xlsx")
            wb = Workbook()
            for site in sites:
                wb.create_sheet(site['name'])

            wb.save(self.excel_path)
            set_config_value("main", "excel_path", str(self.excel_path))

            self.excel_path_var.set(self.excel_path)
            
        else:
            wb = load_workbook(self.excel_path)

        rpa_sheet = wb['RPA'] if 'RPA' in wb.sheetnames else wb.create_sheet('RPA')
        # Clear existing data in "RPA" sheet
        if rpa_sheet.max_row > 1:
            rpa_sheet.delete_rows(2, rpa_sheet.max_row-1)

        txterr = ""
        for site in sites:
            try:
                response = requests.get(site['url'])
                response.raise_for_status()
            except RequestException as e:
                txterr = f"Erreur de connexion pour le site de {site['name']} : {e}"
                self.update_output(txterr)
                continue

            soup = BeautifulSoup(response.content, "html.parser")
            data_extraction_function_name = site['func']
            if hasattr(scrapping, data_extraction_function_name):
                if site['src'] == 'pdf':
                    download_pdf(response, site['name_pdf'], self.pdf_path)
                else:
                    print('')

                data_extraction_function = getattr(scrapping, data_extraction_function_name)
                sheet = wb[site["name"]]
                data = data_extraction_function(soup)
                data, txterr, replaced, replaced_values = check_and_return_value(data, sheet, site['format_func'], txterr, site, data, replaced_values)

                if replaced:
                     replaced_value_count += 1


                row_number = sheet.max_row +1
                sheet.cell(row = row_number, column = 1, value = date)
                sheet.cell(row = row_number, column = 2, value = data)
                sheet.cell(row = row_number, column = 3, value = site['devise'])
                sheet.cell(row = row_number, column = 4, value = site['unit'])
                print (f"Valeur pour le site {site['name']} : {data}")
                 # Write data to RPA sheet
                rpa_row_number = rpa_sheet.max_row + 1
                rpa_sheet.cell(row=rpa_row_number, column=1, value=site['metal'])
                rpa_sheet.cell(row=rpa_row_number, column=2, value=site['name'])
                rpa_sheet.cell(row=rpa_row_number, column=3, value=data)
                rpa_sheet.cell(row=rpa_row_number, column=4, value=site['devise'])
                rpa_sheet.cell(row=rpa_row_number, column=5, value=site['unit'])

                self.update_output(txterr)
                wb.save(self.excel_path)
            else:
                print(f'Aucune fonction d\'extraction de données trouvées')
        replaced_message = f"{replaced_value_count} valeurs remplacées : {', '.join(f'{k}: {v}' for k, v in replaced_values.items())}"
        self.update_output("Script terminé.")
        messagebox.showinfo("Information", f"Le script a terminé l'extraction des données et la mise à jour du fichier Excel.\n{replaced_message}")

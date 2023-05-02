import configparser
import os
import sys

def get_config_value(section, key):
    config = configparser.ConfigParser()

    if getattr(sys, 'frozen', False):
         exe_path = os.path.join(sys.executable)
         config_file_path = os.path.join(exe_path, 'config.ini')
    else:
         config_file_path = "config.ini"

    config.read(config_file_path)
    # Imprimer le contenu de config.ini pour le débogage
    with open(config_file_path, 'r') as f:
        content = f.read()
        print("Contenu de config.ini:")
        print(content)
    value = config.get(section, key)
    return value

def set_config_value(section, variable, value):
    config = configparser.ConfigParser()
    config.read('config.ini')
    config.set(section, variable, value)
    with open('config.ini', 'w') as configfile:
              config.write(configfile)

def get_pdf_path():
    pdf_path = get_config_value("main", "pdf_path")
    if not pdf_path:
        pdf_path = os.getcwd()
    return pdf_path

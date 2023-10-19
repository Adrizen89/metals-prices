import configparser
import os
import sys


def is_executable():
    return getattr(sys, 'frozen', False)

def get_config_path():
    if is_executable():
         application_path = os.path.dirname(sys.executable)
         os.chdir(application_path)
    else:
         application_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..')
    config_path = os.path.join(application_path,'config.ini')

    if not os.path.exists(config_path) and is_executable():
        # Si le fichier config.ini n'existe pas à côté de l'exécutable, recherchez-le dans le répertoire du script
        config_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..','config.ini')
    if not os.path.exists(config_path):
        print(f"Erreur : Le fichier 'config.ini' est introuvable au chemin : {config_path}")
        sys.exit(1)
    
    return os.path.abspath(config_path)

def get_code_config_path():
    if not is_executable():
        return os.path.join(os.path.dirname(os.path.abspath(__file__)), 'config.ini')
    return None

def get_config_value(section, key):
    config = configparser.ConfigParser()
    config_path = get_config_path()
    if config_path is None:
        config_path = get_code_config_path()
    config.read(config_path)
    # Imprimer le contenu de config.ini pour le débogage
    with open(config_path, 'r') as f:
        content = f.read()
        print("Contenu de config.ini:")
        print(content)
    value = config.get(section, key)
    return value

def set_config_value(section, variable, value):
    config = configparser.ConfigParser()
    config_path = get_config_path()
    if config_path is None:
        config_path = get_code_config_path()
    config.read(config_path)
    config.set(section, variable, value)
    with open(config_path, 'w') as configfile:
        config.write(configfile)

def get_pdf_path():
    pdf_path = get_config_value("SETTINGS", "pdf_path")
    if not pdf_path:
        pdf_path = os.getcwd()
    return pdf_path

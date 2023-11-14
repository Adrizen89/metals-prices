import unittest
import sys
sys.path.append('..')
from unittest.mock import patch, mock_open
from app_module.utils_scrapping import extract_2360
from bs4 import BeautifulSoup

class TestExtract2360(unittest.TestCase):
    
    @patch('app_module.utils_scrapping.get_config_value')
    @patch('builtins.open', new_callable=mock_open, read_data='data du PDF')
    @patch('app_module.utils_scrapping.PdfReader')  # Remplacez par le chemin correct de votre PdfReader
    def test_extract_2360_pdf_file_not_found(self, mock_pdf_reader, mock_file, mock_get_config):
        # Simuler un scénario où le fichier PDF n'est pas trouvé
        mock_get_config.return_value = '/chemin/vers/le/fichier/test.pdf'
        mock_file.side_effect = FileNotFoundError


        # Configurer un faux objet BeautifulSoup (soup)
        fake_html = "<html><body></body></html>"
        soup = BeautifulSoup(fake_html, 'html.parser')

        # Appeler extract_2360 et s'attendre à ce qu'elle gère l'erreur
        result = extract_2360(soup)

        # Assertions pour vérifier le résultat en cas d'erreur
        self.assertEqual(result, ('date none', 'value none'))

if __name__ == '__main__':
    unittest.main()

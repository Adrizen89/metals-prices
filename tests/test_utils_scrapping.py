import unittest
import sys
sys.path.append('..')
from bs4 import BeautifulSoup
from datetime import datetime
from app_module.utils_scrapping import extract_3ZN1

class TestExtract3ZN1(unittest.TestCase):

    def setUp(self):
        # HTML de test
        self.html_content = """
        <html>
        <body>
            <table>
                <tr>
                    <th>Date</th>
                    <th>Valeur</th>
                </tr>
                <tr>
                    <td>05. September 2023</td>
                    <td>100,00</td>
                </tr>
                <!-- Ajoutez plus de lignes si nécessaire pour les tests -->
            </table>
        </body>
        </html>
        """
        self.soup = BeautifulSoup(self.html_content, 'html.parser')

    def test_extract_single_value(self):
        # Test pour le cas où checkbox_state est False
        result = extract_3ZN1(self.soup, checkbox_state=False)
        expected_date = datetime.strptime("05/09/2023", "%d/%m/%Y").date()
        expected_date_formatted = expected_date.strftime("%d/%m/%Y") 
        self.assertEqual(result, (expected_date_formatted, '10000'))

    def test_extract_range_values(self):
        # Test pour le cas où checkbox_state est True avec des dates valides
        start_date = datetime.strptime("01/09/2023", "%d/%m/%Y").date()
        end_date = datetime.strptime("10/09/2023", "%d/%m/%Y").date()
        result = extract_3ZN1(self.soup, checkbox_state=True, start_date=start_date, end_date=end_date)
        self.assertIsInstance(result, list)
        self.assertTrue(len(result) > 0)


if __name__ == '__main__':
    unittest.main()

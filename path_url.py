from dotenv import load_dotenv
import os
load_dotenv()
url_cookson = "https://www.cookson-clal.com/cours/"
url_kme = 'https://www.kme.com/en/services/metal-prices'
url_wieland = 'https://www.wieland.com/en/resources/metal-information#metal-information'
url_reynolds = "https://reynolds-cuivre.fr/wp-content/uploads/2017/09/Cours_metaux_template.pdf"
url_lbma = "https://www.lbma.org.uk/prices-and-data/precious-metal-prices#"
url_1AG3 = "https://www.westmetall.com/en/markdaten.php?action=table&field=Ag"
url_2M37 = "https://www.westmetall.com/en/markdaten.php?action=table&field=MB_MS_63_37"
url_3AL1 = "https://www.westmetall.com/en/markdaten.php?action=average&field=LME_AI_cash"
url_3CU1 = "https://www.westmetall.com/en/markdaten.php?action=table&field=LME_Cu_cash"
url_3CU3 = "https://www.westmetall.com/en/markdaten.php?action=table&field=WI_Cu"

# url achat
url_aurubis = "www.kme.com/en/services/metal-prices"
url_novaprofil = "https://www.wieland.com/en/resources/metal-information#metal-information"
url_inovan = "https://www.wieland.com/de/ressourcen/metallinformation#tab-general"
url_profiltech = "https://www.kme.com/fr/services/cours-des-metaux"
url_wieland = "https://www.wieland.com/en/resources/metal-information#metal-information"
url_materion = "https://materion.de.com:443/-/media/files/german/metalvaluepostingfile.pdf"
url_rmetal = "https://www.kme.com/fr/services/cours-des-metaux"
url_sundwiger = "https://www.sundwiger-mw.com/en/"
url_ars = "www.kme.com/en/services/metal-prices"
url_thermocompact = "https://www.cookson-clal.com/cours/"
url_richard = "https://www.wieland.com/en/resources/metal-information"
url_adplating = "https://www.lbma.org.uk/prices-and-data/precious-metal-prices#"
url_kme = "https://www.kme.com/fr/services/cours-des-metaux"
url_pem = ""
url_griset = "https://www.kme.com/fr/services/cours-des-metaux"
url_legeni = "https://www.cookson-clal.com/cours/"
url_dpe = ""
url_k55 = "https://www.wieland.com/en/resources/metal-information#high-performance-alloys"


download_path = os.getenv("DOWNLOAD_PATH")
name_reynolds = "Cours_metaux_template.pdf"
folder_reynolds = f"{download_path}/{name_reynolds}"
name_materion = "metalvaluepostingfile.pdf"
folder_materion = f"{download_path}/{name_materion}"
excel_path = os.getenv("EXCEL_PATH")
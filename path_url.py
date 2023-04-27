from dotenv import load_dotenv
import os
load_dotenv()

# Liens des sites à Scrapper
sites = [
{"name" : "1AG1" , "url":"https://www.cookson-clal.com/cours/"},
{"name" : "1AG3" , "url": "https://www.westmetall.com/en/markdaten.php?action=table&field=Ag"},
{"name" : "1AG2" , "url" : "https://www.lbma.org.uk/prices-and-data/precious-metal-prices#"},
{"name" : "1AU2" , "url" : "https://www.lbma.org.uk/prices-and-data/precious-metal-prices#"},
{"name" : "1AU3" , "url" : "https://www.cookson-clal.com/cours/"},
{"name" : "2M37" , "url" : "https://www.westmetall.com/en/markdaten.php?action=table&field=MB_MS_63_37"},
{"name" : "3AL1" , "url" : "https://www.westmetall.com/en/markdaten.php?action=average&field=LME_AI_cash"},
{"name" : "3CU1" , "url" : "https://www.westmetall.com/en/markdaten.php?action=table&field=LME_Cu_cash"},
{"name" : "3CU3" , "url" : "https://www.westmetall.com/en/markdaten.php?action=table&field=WI_Cu"},
{"name" : "2CUB" , "url" : "https://materion.de.com:443/-/media/files/german/metalvaluepostingfile.pdf"},
{"name" : "3NI1" , "url" : "https://www.kme.com/fr/services/cours-des-metaux"},
{"name" : "3SN1" , "url" : "https://www.kme.com/fr/services/cours-des-metaux"},
]

name_materion ="metalvaluepostingfile.pdf"
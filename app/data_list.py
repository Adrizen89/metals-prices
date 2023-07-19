
import app.utils_format as func


sites = [
{"src": "site","name" : "1AG1" , "url":"https://www.cookson-clal.com/cours/", "func": "extract_1AG1", "unit" : "KG", "devise": "€", "format_func" : func.format_value_1AG1},
{"src": "site","name" : "1AG3" , "url": "https://www.westmetall.com/en/markdaten.php?action=table&field=Ag", "func": "extract_1AG3", "unit" : "KG", "devise": "€", "format_func" : func.format_value_1AG3},
{"src": "site","name" : "1AU3" , "url" : "https://www.cookson-clal.com/cours/", "func": "extract_1AU3", "unit" : "KG", "devise": "€", "format_func" : func.format_value_1AU3},
{"src": "site","name" : "2M37" , "url" : "https://www.westmetall.com/en/markdaten.php?action=table&field=MB_MS_63_37", "func": "extract_2M37", "unit" : "100KG", "devise": "€", "format_func" : func.format_value_2M37},
{"src": "site","name" : "3AL1" , "url" : "https://www.westmetall.com/en/markdaten.php?action=average&field=LME_AI_cash", "func": "extract_3AL1", "unit" : "TO", "devise": "$", "format_func" : func.format_value_3AL1},
{"src": "site","name" : "3CU1" , "url" : "https://www.westmetall.com/en/markdaten.php?action=table&field=LME_Cu_cash", "func": "extract_3CU1", "unit" : "TO", "devise": "$", "format_func" : func.format_value_3CU1},
{"src": "site","name" : "3CU3" , "url" : "https://www.westmetall.com/en/markdaten.php?action=table&field=WI_Cu", "func": "extract_3CU3", "unit" : "100KG", "devise": "€", "format_func" : func.format_value_3CU3},
{"src": "pdf" ,"name" : "2CUB" , "url" : "https://materion.de.com:443/-/media/files/german/metalvaluepostingfile.pdf", "func": "extract_2CUB", "unit" : "KG", "devise": "€", "name_pdf" : "metalvaluepostingfile.pdf", "format_func" : func.format_value_2CUB},
{"src": "site","name" : "3NI1" , "url" : "https://www.kme.com/fr/services/cours-des-metaux", "func": "extract_3NI1", "unit" : "TO", "devise": "$", "format_func" : func.format_value_3NI1},
{"src": "site","name" : "3SN1" , "url" : "https://www.kme.com/fr/services/cours-des-metaux", "func": "extract_3SN1", "unit" : "TO", "devise": "$", "format_func" : func.format_value_3SN1},
{"src": "ext" ,"name" : "1AG2" , "url" : "https://www.lbma.org.uk/prices-and-data/precious-metal-prices#", "func": "extract_1AG2", "unit": "OZ", "devise": "$", "format_func" : func.format_value_1AG2},
{"src": "ext" ,"name" : "1AU2" , "url" : "https://www.lbma.org.uk/prices-and-data/precious-metal-prices#", "func": "extract_1AU2", "unit": "OZ", "devise": "$", "format_func" : func.format_value_1AU2},
{"src": "site" ,"name" : "2B16" , "url" : "https://www.westmetall.com/en/markdaten.php?action=average&field=LME_AI_cash", "func": "extract_2B16", "unit": "100KG", "devise": "€", "format_func" : func.format_value_2B16},
{"src": "site" ,"name" : "2M30" , "url" : "https://www.wieland.com/en/resources/metal-information#metal-information", "func": "extract_2M30", "unit": "100KG", "devise": "€", "format_func" : func.format_value_2M30},
{"src": "ext" ,"name" : "3ZN1" , "url" : "https://www.westmetall.com/en/markdaten.php?action=table&field=LME_Zn_cash", "func": "extract_3ZN1", "unit": "TO", "devise": "$", "format_func" : func.format_value_3ZN1},
]
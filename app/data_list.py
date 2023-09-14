
import app.utils_format as func


sites = [
{"cal": "fr","src": "ext" ,"name" : "2360" , "metal" : "360" ,"url" : "https://www.westmetall.com/en/markdaten.php?action=table&field=LME_Zn_cash", "func": "extract_2360", "unit": "KG", "devise": "€","name_pdf" : "metalvaluepostingfile.pdf", "format_func" : func.format_value_2360},
{"cal": "fr","src": "site","name" : "1AG1", "metal" : "AG" , "url":"https://www.cookson-clal.com/cours/", "func": "extract_1AG1", "unit" : "KG", "devise": "€", "format_func" : func.format_value_1AG1},
{"cal": "fr","src": "ext" ,"name" : "1AG2" , "metal" : "AG" ,"url" : "https://prices.lbma.org.uk/json/silver.json?r=211497526", "func": "extract_1AG2", "unit": "OZ", "devise": "$", "format_func" : func.format_value_1AG2},
{"cal": "fr","src": "site","name" : "3AL1" , "metal" : "AL" ,"url" : "https://www.westmetall.com/en/markdaten.php?action=average&field=LME_AI_cash", "func": "extract_3AL1", "unit" : "TO", "devise": "$", "format_func" : func.format_value_3AL1},
{"cal": "fr","src": "ext" ,"name" : "1AU2" , "metal" : "AU" ,"url" : "https://prices.lbma.org.uk/json/gold_pm.json?r=666323974", "func": "extract_1AU2", "unit": "OZ", "devise": "$", "format_func" : func.format_value_1AU2},
{"cal": "fr","src": "site","name" : "1AU3" , "metal" : "AU" ,"url" : "https://www.cookson-clal.com/cours/", "func": "extract_1AU3", "unit" : "KG", "devise": "€", "format_func" : func.format_value_1AU3},
{"cal": "fr","src": "site" ,"name" : "2B16" , "metal" : "B16" ,"url" : "https://www.westmetall.com/en/markdaten.php?action=average&field=LME_AI_cash", "func": "extract_2B16", "unit": "100KG", "devise": "€", "format_func" : func.format_value_2B16},
{"cal": "fr","src": "site","name" : "3CU1" , "metal" : "CU" ,"url" : "https://www.westmetall.com/en/markdaten.php?action=table&field=LME_Cu_cash", "func": "extract_3CU1", "unit" : "TO", "devise": "$", "format_func" : func.format_value_3CU1},
{"cal": "fr","src": "site","name" : "3CU3" , "metal" : "CU" ,"url" : "https://www.westmetall.com/en/markdaten.php?action=table&field=WI_Cu", "func": "extract_3CU3", "unit" : "100KG", "devise": "€", "format_func" : func.format_value_3CU3},
{"cal": "fr","src": "pdf" ,"name" : "2CUB" , "metal" : "CUB" ,"url" : "https://materion.de.com:443/-/media/files/german/metalvaluepostingfile.pdf", "func": "extract_2CUB", "unit" : "KG", "devise": "€", "name_pdf" : "metalvaluepostingfile.pdf", "format_func" : func.format_value_2CUB},
{"cal": "fr","src": "site" ,"name" : "2M30" , "metal" : "M30" ,"url" : "https://www.wieland.com/en/resources/metal-information#metal-information", "func": "extract_2M30", "unit": "100KG", "devise": "€", "format_func" : func.format_value_2M30},
{"cal": "fr","src": "site","name" : "2M37" , "metal" : "M37" ,"url" : "https://www.westmetall.com/en/markdaten.php?action=table&field=MB_MS_63_37", "func": "extract_2M37", "unit" : "100KG", "devise": "€", "format_func" : func.format_value_2M37},
{"cal": "fr","src": "site","name" : "3NI1" , "metal" : "NI" ,"url" : "https://www.kme.com/fr/services/cours-des-metaux", "func": "extract_3NI1", "unit" : "TO", "devise": "$", "format_func" : func.format_value_3NI1},
{"cal": "fr","src": "site","name" : "3SN1" , "metal" : "SN" ,"url" : "https://www.kme.com/fr/services/cours-des-metaux", "func": "extract_3SN1", "unit" : "TO", "devise": "$", "format_func" : func.format_value_3SN1},
{"cal": "fr","src": "ext" ,"name" : "3ZN1" , "metal" : "ZN" ,"url" : "https://www.westmetall.com/en/markdaten.php?action=table&field=LME_Zn_cash", "func": "extract_3ZN1", "unit": "TO", "devise": "$", "format_func" : func.format_value_3ZN1},
# {"cal": "fr","src": "site","name" : "1AG3" , "metal" : "AG" , "url": "https://www.westmetall.com/en/markdaten.php?action=table&field=Ag", "func": "extract_1AG3", "unit" : "KG", "devise": "€", "format_func" : func.format_value_1AG3},
]


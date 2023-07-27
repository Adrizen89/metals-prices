import re
def check_and_return_value(value, sheet, format_func, txterr, site, data, replaced_values):
    replaced = False
    valueformat = data.replace('.', ',').replace(' ', '')
    pattern = r'^-|\d+(\s*\d{3})*(,\d+)?$'

    if re.match(pattern, valueformat) and valueformat != "-" and valueformat != "init":
        txterr = f"Valeur pour le site {site['name']} : {valueformat}"
    
    else: 
        last_row = sheet.max_row
        value = sheet.cell(row=last_row, column=2).value
        txterr = f"Remplacement pour {site['name']} : {value} , {valueformat}"
        replaced = True
        replaced_values[site['name']] = value
    
    return value, txterr, replaced, replaced_values

    


    # try:
        
    #     # valueformat = valueformat
    #     # valueformat = value.replace('.', ',')
    #     float(valueformat)
    #     txterr = f"Valeur pour le site {site['name']} : {data}, {valueformat}"


    # except ValueError:
    #     last_row = sheet.max_row
    #     value = sheet.cell(row=last_row, column=2).value
    #     txterr = f"Remplacement pour {site['name']} : {value} , {valueformat}"
    #     replaced = True
    #     replaced_values[site['name']] = value


    # return value, txterr, replaced, replaced_values


def format_value_1AG1(value):
    return value.replace('.', ',')

def format_value_1AU3(value):
    return value.replace('€', '')

def format_value_1AG3(value):
    return value.replace('.', ',')

def format_value_2M37(value):
    return value.replace('.', ',')

def format_value_3AL1(value):
    return value.replace(',', '').replace('.', ',')

def format_value_3CU1(value):
    return value.replace(',', '').replace('.', ',')

def format_value_3CU3(value):
    return value.replace('.', ',')

def format_value_3NI1(value):
    return value.replace('.', '').replace('¹', '')

def format_value_3SN1(value):
    return value.replace('.', '').replace('¹', '')

def format_value_2CUB(value):
    return value.replace('.', ',')

def format_value_2360(value):
    return value.replace('.', ',')

def format_value_1AG2(value):
    return value.replace('.', ',')

def format_value_1AU2(value):
    return value.replace('.', ',')

def format_value_2M30(value):
    return value.replace('.', '').replace('.', ',')

def format_value_2B16(value):
    return value.replace('.', '').replace('.', ',')

def format_value_3ZN1(value):
    return value.replace('.', '').replace('.', '')
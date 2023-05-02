def check_and_return_value(value, sheet, format_func, txterr, site, data):
    try:
        valueformat = format_func(value)
        float(valueformat.replace(',', '.'))
        txterr = f"Valeur pour le site {site['name']} : {data}"
    except ValueError:
        last_row = sheet.max_row
        value = sheet.cell(row=last_row, column=2).value
        txterr = f"Valeur remplacé pour le site {site['name']} : {value}"
    return value, txterr


def format_value_1AG1(value):
    return value.replace('.', ',')

def format_value_1AU3(value):
    return value.replace('.', ',').replace('€', '')

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

def format_value_1AG2(value):
    return value.replace('.', ',')

def format_value_1AU2(value):
    return value.replace('.', ',')

def format_value_2M30(value):
    return value.replace('.', '').replace('.', ',')

def format_value_2B16(value):
    return value.replace('.', '').replace('.', ',')
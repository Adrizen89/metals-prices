import configparser

def get_config_value(section, variable):
    config = configparser.ConfigParser()
    config.read('config.ini')
    value = config.get(section, variable)
    return value

def set_config_value(section, variable, value):
    config = configparser.ConfigParser()
    config.read('config.ini')
    config.set(section, variable, value)
    with open('config.ini', 'w') as configfile:
              config.write(configfile)
import requests
import path_url

response_cookson = requests.get(path_url.url_cookson)
response_kme = requests.get(path_url.url_kme)
response_wieland = requests.get(path_url.url_wieland)
response_reynolds = requests.get(path_url.url_reynolds)
response_materion = requests.get(path_url.url_materion)
response_lbma = requests.get(path_url.url_lbma)
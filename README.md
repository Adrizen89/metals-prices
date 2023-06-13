# Application Metals-Prices

Cette application a pour but de récupérer différents cours de métaux sur différents sites, les regrouper sur un fichier Excel et le déposer dans un dossier spécifique.

## Installation
```
$ git clone https://example.com
$ cd ../path/to/the/file
$ Créer un fichier ".env" avec les variables suivantes :
    DOWNLOAD_PATH = path/for/download/pdf
    EXCEL_PATH = path/for/download/excel

## Tableau pour Tarifs Clients

| Métal | Devise | Unité | Code SAP | Description | Lien |
|:--------------|:-------------:|--------------:|--------------:|--------------:|----------------------------------------------------------------------------------:|
| AG | € | X OZ | 1AG1 | Ag c3E | [Lien](https://www.cookson-clal.com/cours/cours.jsp?table=fins&datearch=) |
| AG | € | KG | 1AG3 | Ag Westmetall (Finesliber) | [Lien](https://www.westmetall.com/en/markdaten.php?action=table&field=Ag) |
| AG | $ | OZ | 1AG2 | Ag LBMA | [Lien](https://www.lbma.org.uk/prices-and-data/precious-metal-prices#/table) |
| AU | $ | OZ | 1AU2 | Au LBMA | [Lien](https://www.lbma.org.uk/prices-and-data/precious-metal-prices#/table) |
| AU | € | X OZ | 1AU3 | Au Industriel | [Lien](https://www.cookson-clal.com/cours/cours.jsp?table=fins&datearch=) |
| CuZn37/38 | € | 100 KG | 2M37 | Metalrate CuZn37/38 | [Lien](https://www.westmetall.com/en/markdaten.php?action=table&field=MB_MS_63_37) |
| AL | $ | TO | 3AL1 | LME Settlement Aluminium | [Lien](https://www.westmetall.com/en/markdaten.php?action=average&field=LME_AI_cash) |
| CU | $ | TO | 3CU1 | LME Settlement Copper | [Lien](https://www.westmetall.com/en/markdaten.php?action=table&field=LME_Cu_cash) |
| CU | € | 100 KG | 3CU3 | Wieland Kopper | [Lien](https://www.westmetall.com/en/markdaten.php?action=table&field=WI_Cu) |


| Test | Test | Test |
|:----:|:----:|:----:|
| OK | OK | OK |

## Tableau Fournisseurs pour les Achats

| Métal | Devise | Unité | Code SAP | Description | Lien |
|:--------------|:-------------:|--------------:|--------------:|--------------:|--------------:|
| STOL78 | € | KG | 2CUB | Alloy 25 | materion |
| Ni | $ | TO | 3NI1 |  | https://www.kme.com/fr/services/cours-des-metaux |
| Sn | $ | TO | 3SN1 |  | https://www.kme.com/fr/services/cours-des-metaux |
|  |  |  |  |  |  |
|  |  |  |  |  |  |
|  |  |  |  |  |  |
|  |  |  |  |  |  |
|  |  |  |  |  |  |
|  |  |  |  |  |  |

DAD - Adrien BERARD

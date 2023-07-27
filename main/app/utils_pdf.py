import os

# Téléchargement des PDFs
def download_pdf(response, name, folder):
    """Télécharger un fichier PDF et l'enregistrer localement"""
    if response.status_code == 200:
        print("Connexion réussie")
        path_download = os.path.join(folder, name)
        with open(path_download, "wb") as f:
            f.write(response.content)
        print(f"Téléchargement de {name} terminé avec succès à l'endroit {path_download}")
    else:
        print(f"Erreur lors du téléchargement de {name}")


# Suppression des PDFs
def delete_pdfs(path_pdf, name_materion):
    """Supprimer deux fichiers PDF"""
    path_materion = f"{path_pdf}/{name_materion}"
    print(path_materion)
    try:
        os.remove(path_materion)
        print("Suppression des fichiers PDF terminée avec succès")
    except FileNotFoundError:
        print("Erreur : au moins un des fichiers PDF n'existe pas")
    except Exception as e:
        print(f"Une erreur s'est produite : {e}")
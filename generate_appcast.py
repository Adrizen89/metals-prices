# Exemple simplifié
import json

def generate_appcast():
    # Lire le fichier version.json
    with open('version.json', 'r') as f:
        version_info = json.load(f)
        print('version lu')

    version = version_info['version']
    url = version_info['url']  # Assurez-vous que cette URL pointe vers l'exécutable dans les assets de release

    appcast_xml = f"""
    <item>
        <title>Version {version}</title>
        <sparkle:version>{version}</sparkle:version>
        <enclosure url="{url}" sparkle:version="{version}" type="application/octet-stream" />
    </item>
    """

    # Écrire le fichier Appcast XML
    with open('docs/appcast.xml', 'w') as f:
        f.write(appcast_xml)

if __name__ == "__main__":
    generate_appcast()

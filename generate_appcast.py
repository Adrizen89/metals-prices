# Exemple simplifié
import json

def generate_appcast():
    # Lire le fichier version.json
    with open('version.json', 'r') as f:
        version_info = json.load(f)
        print('version lu')

    version = version_info['version']
    url = version_info['url']  # Assurez-vous que cette URL pointe vers l'exécutable dans les assets de release

    appcast_xml = f"""<?xml version="1.0" encoding="utf-8"?>
<rss version="2.0" xmlns:sparkle="http://www.andymatuschak.org/xml-namespaces/sparkle" xmlns:dc="http://purl.org/dc/elements/1.1/">
    <channel>
        <title>Votre application Updates</title>
        <link>{url}</link>
        <description>Les mises à jour les plus récentes pour Votre application.</description>
        <language>fr</language>
        <item>
            <title>Version {version}</title>
            <enclosure url="{url}"
                       sparkle:version="{version}"
                       sparkle:shortVersionString="{version}"
                       type="application/octet-stream"/>
        </item>
    </channel>
</rss>"""

    # Écrire le fichier Appcast XML
    with open('docs/appcast.xml', 'w') as f:
        f.write(appcast_xml)

if __name__ == "__main__":
    generate_appcast()

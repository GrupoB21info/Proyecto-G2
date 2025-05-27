def export_path_to_kml(path, filename):
    with open(filename, 'w') as f:
        f.write("""<?xml version="1.0" encoding="UTF-8"?>
<kml xmlns="http://www.opengis.net/kml/2.2">
<Document>
<Placemark>
<name>Ruta más corta</name>
<LineString>
<coordinates>
""")
        for np in path.nodes:
            f.write(f"{np.x},{np.y},0\n")

        f.write("""
</coordinates>
</LineString>
</Placemark>
</Document>
</kml>""")
def export_path_to_kml(path, filename):
    with open(filename, 'w') as f:
        f.write("""<?xml version="1.0" encoding="UTF-8"?>
<kml xmlns="http://www.opengis.net/kml/2.2">
<Document>
<name>Ruta más corta</name>
""")

        # Añadir etiquetas para cada nodo
        for np in path.nodes:
            f.write(f"""
<Placemark>
    <name>{np.name}</name>
    <Point>
        <coordinates>{np.y},{np.x},0</coordinates>
    </Point>
</Placemark>
""")

        # Añadir la línea de ruta
        f.write("""
<Placemark>
    <name>Ruta completa</name>
    <Style>
      <LineStyle>
        <color>ff0000ff</color>  <!-- rojo en formato ABGR -->
        <width>3</width>
      </LineStyle>
    </Style>
    <LineString>
      <tessellate>1</tessellate>
      <coordinates>
""")

        for np in path.nodes:
            f.write(f"{np.y},{np.x},0\n")  # lon,lat,alt

        f.write("""
      </coordinates>
    </LineString>
</Placemark>
</Document>
</kml>""")

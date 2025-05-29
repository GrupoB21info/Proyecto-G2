def export_path_to_kml(path_or_graph, filename):
    def format_coords(node):
        return f"{node.y},{node.x},0"  # KML: lon,lat,alt

    with open(filename, 'w') as f:
        f.write("""<?xml version="1.0" encoding="UTF-8"?>
<kml xmlns="http://www.opengis.net/kml/2.2">
<Document>
<name>Exportación de Nodos</name>
""")

        # Detectar si es una ruta (camino más corto)
        if hasattr(path_or_graph, 'nodes') and isinstance(path_or_graph.nodes, list):
            nodes = path_or_graph.nodes

            # Dibujar cada nodo como punto
            for node in nodes:
                f.write(f"""
<Placemark>
    <name>{node.name}</name>
    <Point>
        <coordinates>{format_coords(node)}</coordinates>
    </Point>
</Placemark>
""")

            # Dibujar la línea de la ruta
            f.write("""
<Placemark>
    <name>Ruta completa</name>
    <Style>
      <LineStyle>
        <color>ff0000ff</color>  <!-- Rojo -->
        <width>3</width>
      </LineStyle>
    </Style>
    <LineString>
      <tessellate>1</tessellate>
      <coordinates>
""")
            for node in nodes:
                f.write(f"{format_coords(node)}\n")
            f.write("""
      </coordinates>
    </LineString>
</Placemark>
""")

        else:
            # Caso: grafo completo → solo los nodos como puntos
            for node in path_or_graph.nodes:
                f.write(f"""
<Placemark>
    <name>{node.name}</name>
    <Point>
        <coordinates>{format_coords(node)}</coordinates>
    </Point>
</Placemark>
""")

        f.write("</Document>\n</kml>")
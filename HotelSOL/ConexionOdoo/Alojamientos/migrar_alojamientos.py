﻿import pyodbc
import xml.etree.ElementTree as ET

# Conexion a SQL Server
conn = pyodbc.connect(
    "DRIVER={ODBC Driver 17 for SQL Server};SERVER=localhost;DATABASE=hotelsol;Trusted_Connection=yes;"
)
cursor = conn.cursor()

# JOIN entre Alojamiento y TipoAlojamiento
cursor.execute("""
    SELECT a.Id, a.TipoId, t.Nombre AS TipoNombre, a.Precio
    FROM Alojamientos a
    JOIN TipoAlojamientos t ON a.TipoId = t.Id
""")

alojamientos = cursor.fetchall()

# Crear raiz del XML
root = ET.Element("alojamientos")
ids_vistos = set()

for a in alojamientos:
    if a.Id in ids_vistos:
        continue
    ids_vistos.add(a.Id)

    aloj_elem = ET.SubElement(root, "alojamiento")
    ET.SubElement(aloj_elem, "id").text = str(a.Id)
    ET.SubElement(aloj_elem, "tipo_id").text = str(a.TipoId)
    ET.SubElement(aloj_elem, "tipo_nombre").text = str(a.TipoNombre)
    ET.SubElement(aloj_elem, "precio_base").text = str(a.Precio)

# Guardar el XML
tree = ET.ElementTree(root)
tree.write("alojamientos_intercambio.xml", encoding="utf-8", xml_declaration=True)

print("Archivo XML 'alojamientos_intercambio.xml' generado correctamente.")

conn.close()
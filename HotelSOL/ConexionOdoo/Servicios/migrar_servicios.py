"""
Script para generar un fichero XML con los servicios unicos del hotel desde SQL Server.
Se conecta a la base 'hotelsol', consulta la tabla 'Servicios' y genera un archivo XML
sin incluir servicios duplicados por nombre.
"""

import pyodbc
import xml.etree.ElementTree as ET

# Conexion a SQL Server
conn_sql = pyodbc.connect(
    "DRIVER={ODBC Driver 17 for SQL Server};SERVER=localhost;DATABASE=hotelsol;Trusted_Connection=yes;"
)
cursor = conn_sql.cursor()
cursor.execute("SELECT Id, Nombre, Precio, Descripcion FROM Servicios")
servicios = cursor.fetchall()

# Crear raiz del XML
root = ET.Element("servicios")

# Controlar duplicados por nombre
nombres_agregados = set()
duplicados_omitidos = 0

for servicio in servicios:
    nombre = str(servicio.Nombre)
    if nombre in nombres_agregados:
        duplicados_omitidos += 1
        continue  # Ya incluido en el XML

    nombres_agregados.add(nombre)

    s_elem = ET.SubElement(root, "servicio")
    ET.SubElement(s_elem, "id").text = str(servicio.Id)
    ET.SubElement(s_elem, "nombre").text = nombre
    ET.SubElement(s_elem, "precio").text = str(servicio.Precio)
    ET.SubElement(s_elem, "descripcion").text = str(servicio.Descripcion)

# Guardar el archivo XML
tree = ET.ElementTree(root)
tree.write("servicios_intercambio.xml", encoding="utf-8", xml_declaration=True)

print(f"Archivo XML 'servicios_intercambio.xml' generado correctamente.")
print(f"Servicios omitidos por estar duplicados en SQL: {duplicados_omitidos}")

conn_sql.close()

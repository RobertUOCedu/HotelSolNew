"""
Script para generar un fichero de intercambio XML con datos de clientes.

Objetivo:
Este script consulta los datos de clientes desde SQL Server (tablas 'Usuarios' y 'Clientes'),
y genera un archivo XML llamado 'clientes_intercambio.xml'. Este fichero representa el
intercambio de informacion entre la aplicacion del Producto 3 y Odoo, cumpliendo con el
formato estructurado requerido.

Cada cliente se exporta como una entrada <cliente> con los siguientes datos:
- id, nombre, apellido, email, movil, es_vip

Este fichero puede ser consumido por procesos de importacion o sincronizacion en Odoo.

"""


import pyodbc
import xml.etree.ElementTree as ET

# Conexion a SQL Server
conn = pyodbc.connect(
    "DRIVER={ODBC Driver 17 for SQL Server};SERVER=localhost;DATABASE=hotelsol;Trusted_Connection=yes;"
)
cursor = conn.cursor()

# Consulta con JOIN y correos validos
cursor.execute("""
    SELECT u.Id, u.Nombre, u.Apellido, u.Email, u.Movil, c.EsVIP
    FROM Clientes c
    JOIN Usuarios u ON c.Id = u.Id
    WHERE u.Email LIKE '%@%'
""")
clientes = cursor.fetchall()

# Crear raiz del XML
root = ET.Element("clientes")

# Agregar cada cliente como subelemento
for cliente in clientes:
    c_elem = ET.SubElement(root, "cliente")
    ET.SubElement(c_elem, "id").text = str(cliente.Id)
    ET.SubElement(c_elem, "nombre").text = str(cliente.Nombre)
    ET.SubElement(c_elem, "apellido").text = str(cliente.Apellido)
    ET.SubElement(c_elem, "email").text = str(cliente.Email)
    ET.SubElement(c_elem, "movil").text = str(cliente.Movil)
    ET.SubElement(c_elem, "es_vip").text = str(cliente.EsVIP)

# Crear arbol XML y guardarlo en archivo
tree = ET.ElementTree(root)
tree.write("clientes_intercambio.xml", encoding="utf-8", xml_declaration=True)

print("Archivo XML 'clientes_intercambio.xml' generado correctamente.")

conn.close()

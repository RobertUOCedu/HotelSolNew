import pyodbc
import xml.etree.ElementTree as ET

conn = pyodbc.connect(
    "DRIVER={ODBC Driver 17 for SQL Server};SERVER=localhost;DATABASE=hotelsol;Trusted_Connection=yes;"
)
cursor = conn.cursor()

root = ET.Element("empleados")

# Administradores
cursor.execute("""
    SELECT u.Id, u.Nombre, u.Apellido, u.Email, u.Movil
    FROM Administradores a
    JOIN Usuarios u ON a.Id = u.Id
""")
administradores = cursor.fetchall()

for a in administradores:
    e_elem = ET.SubElement(root, "empleado")
    ET.SubElement(e_elem, "id").text = str(a.Id)
    ET.SubElement(e_elem, "nombre").text = f"{a.Nombre} {a.Apellido}"
    ET.SubElement(e_elem, "email").text = a.Email
    ET.SubElement(e_elem, "movil").text = str(a.Movil)
    ET.SubElement(e_elem, "departamento").text = "Administradores"

# Recepcionistas
cursor.execute("""
    SELECT u.Id, u.Nombre, u.Apellido, u.Email, u.Movil
    FROM Recepcionistas r
    JOIN Usuarios u ON r.Id = u.Id
""")
recepcionistas = cursor.fetchall()

for r in recepcionistas:
    e_elem = ET.SubElement(root, "empleado")
    ET.SubElement(e_elem, "id").text = str(r.Id)
    ET.SubElement(e_elem, "nombre").text = f"{r.Nombre} {r.Apellido}"
    ET.SubElement(e_elem, "email").text = r.Email
    ET.SubElement(e_elem, "movil").text = str(r.Movil)
    ET.SubElement(e_elem, "departamento").text = "Recepcionistas"

tree = ET.ElementTree(root)
tree.write("empleados.xml", encoding="utf-8", xml_declaration=True)

print("Archivo 'empleados.xml' generado correctamente.")
conn.close()
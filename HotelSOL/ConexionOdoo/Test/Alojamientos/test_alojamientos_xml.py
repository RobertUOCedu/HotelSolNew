# test_alojamientos_xml.py
import xml.etree.ElementTree as ET

def test_alojamientos_xml():
    tree = ET.parse("alojamientos_intercambio.xml")
    root = tree.getroot()
    errores = 0

    for aloj in root.findall("alojamiento"):
        tipo_nombre = aloj.find("tipo_nombre").text or ""
        precio = aloj.find("precio_base").text or ""

        if not tipo_nombre.strip():
            print("Alojamiento sin tipo_nombre.")
            errores += 1
        try:
            float(precio)
        except:
            print(f"Alojamiento con precio inválido: {precio}")
            errores += 1

    if errores == 0:
        print("Todos los alojamientos del XML tienen tipo y precio válidos.")
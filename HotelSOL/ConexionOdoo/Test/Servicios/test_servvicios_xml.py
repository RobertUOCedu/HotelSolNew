# test_servicios_xml.py
import xml.etree.ElementTree as ET

def test_servicios_xml():
    tree = ET.parse("servicios_intercambio.xml")
    root = tree.getroot()
    nombres = set()
    errores = 0

    for s in root.findall("servicio"):
        nombre = s.find("nombre").text or ""
        precio = s.find("precio").text or ""
        descripcion = s.find("descripcion").text or ""

        if not nombre.strip():
            print("Servicio sin nombre.")
            errores += 1
        if nombre in nombres:
            print(f"Servicio duplicado en XML: {nombre}")
            errores += 1
        else:
            nombres.add(nombre)

        try:
            float(precio)
        except:
            print(f"Servicio '{nombre}' con precio inválido: {precio}")
            errores += 1

        if not descripcion.strip():
            print(f"Servicio '{nombre}' sin descripción.")
            errores += 1

    if errores == 0:
        print("Todos los servicios del XML son válidos y únicos.")

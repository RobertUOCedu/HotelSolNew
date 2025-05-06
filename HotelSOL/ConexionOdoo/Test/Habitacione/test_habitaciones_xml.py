# test_habitaciones_xml.py
import xml.etree.ElementTree as ET

def test_habitaciones_xml():
    tree = ET.parse("habitaciones.xml")
    root = tree.getroot()
    errores = 0

    for hab in root.findall("habitacion"):
        numero = hab.find("numero").text or ""
        tipo = hab.find("tipo").text or ""
        capacidad = hab.find("capacidad").text or ""
        precio = hab.find("precio").text or ""
        disponibilidad = hab.find("disponibilidad").text or ""

        if not numero.strip():
            print("Habitacion sin número.")
            errores += 1
        if not tipo.strip():
            print(f"Habitacion {numero} sin tipo.")
            errores += 1
        if not capacidad.strip().isdigit():
            print(f"Habitacion {numero} con capacidad inválida: {capacidad}")
            errores += 1
        try:
            float(precio)
        except:
            print(f"Habitacion {numero} con precio inválido: {precio}")
            errores += 1
        if disponibilidad not in ("0", "1"):
            print(f"Habitacion {numero} con disponibilidad inválida: {disponibilidad}")
            errores += 1

    if errores == 0:
        print("Todas las habitaciones del XML están correctamente formateadas.")

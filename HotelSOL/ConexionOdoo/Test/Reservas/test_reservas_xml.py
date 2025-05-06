# test_reservas_xml.py
import xml.etree.ElementTree as ET
from datetime import datetime

def test_reservas_xml():
    tree = ET.parse("reservas.xml")
    root = tree.getroot()
    errores = 0

    for r in root.findall("reserva"):
        cliente = r.find("cliente").text or ""
        email = r.find("email").text or ""
        habitacion = r.find("habitacion").text or ""
        entrada = r.find("fecha_entrada").text or ""
        salida = r.find("fecha_salida").text or ""
        precio = r.find("precio").text or ""

        if not cliente.strip() or not email.strip() or not habitacion.strip():
            print(f"Reserva incompleta: {cliente}, {email}, {habitacion}")
            errores += 1

        try:
            datetime.strptime(entrada, "%Y-%m-%d")
            datetime.strptime(salida, "%Y-%m-%d")
        except:
            print(f"Fechas inválidas: entrada={entrada}, salida={salida}")
            errores += 1

        try:
            float(precio)
        except:
            print(f"Precio inválido: {precio}")
            errores += 1

    if errores == 0:
        print("Todas las reservas del XML tienen campos válidos.")
# test_clientes_xml.py
import xml.etree.ElementTree as ET
import re

def es_email_valido(email):
    return re.match(r"[^@]+@[^@]+\.[^@]+", email)

def test_clientes_xml_valido():
    tree = ET.parse("clientes_intercambio.xml")
    root = tree.getroot()
    errores = 0

    for cliente in root.findall("cliente"):
        nombre = cliente.find("nombre").text or ""
        apellido = cliente.find("apellido").text or ""
        email = cliente.find("email").text or ""

        if not nombre.strip() or not apellido.strip():
            print(f"Cliente con nombre o apellido vacío: {ET.tostring(cliente, encoding='unicode')}")
            errores += 1
        elif not es_email_valido(email):
            print(f"Email inválido: {email}")
            errores += 1

    if errores == 0:
        print("Todos los clientes del XML son válidos.")
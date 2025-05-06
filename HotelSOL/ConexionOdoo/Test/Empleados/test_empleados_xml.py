# test_empleados_xml.py
import xml.etree.ElementTree as ET
import re

def es_email_valido(email):
    return re.match(r"[^@]+@[^@]+\.[^@]+", email)

def test_empleados_xml_valido():
    tree = ET.parse("empleados.xml")
    root = tree.getroot()
    errores = 0

    for emp in root.findall("empleado"):
        nombre = emp.find("nombre").text or ""
        email = emp.find("email").text or ""
        depto = emp.find("departamento").text or ""

        if not nombre.strip():
            print(f"Empleado sin nombre: {ET.tostring(emp, encoding='unicode')}")
            errores += 1
        elif not es_email_valido(email):
            print(f"Email inválido: {email}")
            errores += 1
        elif not depto.strip():
            print(f"Departamento vacío en: {nombre}")
            errores += 1

    if errores == 0:
        print("Todos los empleados del XML son válidos.")
# test_validacion_xmls.py
import os
import xml.etree.ElementTree as ET

def validar_archivo_xml(ruta):
    try:
        tree = ET.parse(ruta)
        tree.getroot()
        print(f"✅ XML válido: {ruta}")
    except Exception as e:
        print(f"❌ Error en XML '{ruta}': {e}")

def test_xmls_generados():
    rutas = [
        "clientes_intercambio.xml",
        "empleados.xml",
        "habitaciones.xml",
        "alojamientos_intercambio.xml",
        "facturas.xml",
        "reservas.xml",
        "servicios_intercambio.xml"
    ]
    for ruta in rutas:
        if os.path.exists(ruta):
            validar_archivo_xml(ruta)
        else:
            print(f"Archivo no encontrado: {ruta}")
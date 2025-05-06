# test_alojamientos_odoo.py
import xmlrpc.client
import xml.etree.ElementTree as ET

def test_alojamientos_odoo():
    # Cargar nombres desde el XML
    tree = ET.parse("alojamientos_intercambio.xml")
    root = tree.getroot()
    nombres_xml = set()

    for aloj in root.findall("alojamiento"):
        tipo_nombre = aloj.find("tipo_nombre").text.strip()
        nombres_xml.add(tipo_nombre)

    # Conexion a Odoo
    url = "http://127.0.0.1:8071"
    db = "hotelsol"
    username = "egamerolopez@uoc.edu"
    password = "HotelSol123"

    common = xmlrpc.client.ServerProxy(f"{url}/xmlrpc/2/common")
    uid = common.authenticate(db, username, password, {})
    models = xmlrpc.client.ServerProxy(f"{url}/xmlrpc/2/object")

    # Buscar productos tipo servicio
    productos = models.execute_kw(db, uid, password, 'product.template', 'search_read', [
        [('type', '=', 'service')]
    ], {'fields': ['name']})

    nombres_odoo = [p['name'].strip() for p in productos]

    errores = 0
    for nombre in nombres_xml:
        coincidencias = [n for n in nombres_odoo if nombre in n]
        if not coincidencias:
            print(f"Alojamiento '{nombre}' no encontrado en Odoo.")
            errores += 1
        elif len(coincidencias) > 1:
            print(f"Alojamiento '{nombre}' duplicado en Odoo: {coincidencias}")
            errores += 1
        else:
            print(f"Alojamiento '{nombre}' registrado correctamente.")

    if errores == 0:
        print("Todos los alojamientos del XML están correctamente insertados y sin duplicados.")

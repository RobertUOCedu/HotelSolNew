# test_servicios_odoo.py
import xml.etree.ElementTree as ET
import xmlrpc.client

def test_servicios_en_odoo():
    # Cargar nombres del XML
    tree = ET.parse("servicios_intercambio.xml")
    root = tree.getroot()
    nombres_xml = [s.find("nombre").text.strip() for s in root.findall("servicio")]

    # Conexion Odoo
    url = "http://127.0.0.1:8071"
    db = "hotelsol"
    username = "egamerolopez@uoc.edu"
    password = "HotelSol123"

    common = xmlrpc.client.ServerProxy(f"{url}/xmlrpc/2/common")
    uid = common.authenticate(db, username, password, {})
    models = xmlrpc.client.ServerProxy(f"{url}/xmlrpc/2/object")

    productos = models.execute_kw(db, uid, password, 'product.template', 'search_read', [
        [('type', '=', 'service')]
    ], {'fields': ['name', 'property_account_income_id']})

    nombres_odoo = [p['name'].strip() for p in productos]
    errores = 0

    for nombre in nombres_xml:
        coincidencias = [p for p in productos if p['name'].strip() == nombre]
        if not coincidencias:
            print(f"Servicio '{nombre}' no se encontró en Odoo.")
            errores += 1
        elif len(coincidencias) > 1:
            print(f"Servicio '{nombre}' duplicado en Odoo.")
            errores += 1
        elif not coincidencias[0]['property_account_income_id']:
            print(f"Servicio '{nombre}' sin cuenta contable asignada.")
            errores += 1
        else:
            print(f"Servicio '{nombre}' correctamente registrado en Odoo.")

    if errores == 0:
        print("Todos los servicios del XML están correctamente creados en Odoo con cuenta contable.")
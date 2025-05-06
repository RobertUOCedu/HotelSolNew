import xml.etree.ElementTree as ET
import xmlrpc.client

# Leer el archivo XML generado
tree = ET.parse("clientes_intercambio.xml")
root = tree.getroot()

# Conexion a Odoo
url = "http://127.0.0.1:8071"
db = "hotelsol"
username = "egamerolopez@uoc.edu"
password = "HotelSol123"

common = xmlrpc.client.ServerProxy(f"{url}/xmlrpc/2/common")
uid = common.authenticate(db, username, password, {})
models = xmlrpc.client.ServerProxy(f"{url}/xmlrpc/2/object")

# Asegurar que existe la categoria VIP
vip_category_id = models.execute_kw(
    db, uid, password, 'res.partner.category', 'search',
    [[['name', '=', 'VIP']]]
)
if not vip_category_id:
    vip_category_id = models.execute_kw(
        db, uid, password, 'res.partner.category', 'create',
        [{'name': 'VIP'}]
    )
else:
    vip_category_id = vip_category_id[0]

# Procesar cada cliente del XML
for cliente_elem in root.findall("cliente"):
    nombre = cliente_elem.find("nombre").text
    apellido = cliente_elem.find("apellido").text
    email = cliente_elem.find("email").text
    movil = cliente_elem.find("movil").text
    es_vip = cliente_elem.find("es_vip").text == "1"

    # Verificar si ya existe un contacto con el mismo movil
    existe = models.execute_kw(
        db, uid, password, 'res.partner', 'search',
        [[['phone', '=', movil]]]
    )
    if existe:
        print(f"Cliente con movil {movil} ya existe. Omitido.")
        continue

    valores = {
        'name': f"{nombre} {apellido}",
        'email': email,
        'phone': movil,
        'is_company': False,
        'type': 'contact',
    }

    if es_vip:
        valores['category_id'] = [(6, 0, [vip_category_id])]

    partner_id = models.execute_kw(db, uid, password, 'res.partner', 'create', [valores])
    print(f"Cliente {valores['name']} insertado en Odoo con ID: {partner_id}")

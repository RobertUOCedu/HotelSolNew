import xml.etree.ElementTree as ET
import xmlrpc.client

tree = ET.parse("habitaciones.xml")
root = tree.getroot()

# Conexion Odoo
url = "http://127.0.0.1:8071"
db = "hotelsol"
username = "egamerolopez@uoc.edu"
password = "HotelSol123"

common = xmlrpc.client.ServerProxy(f"{url}/xmlrpc/2/common")
uid = common.authenticate(db, username, password, {})
models = xmlrpc.client.ServerProxy(f"{url}/xmlrpc/2/object")

# Obtener cuenta contable de ingresos
cuentas = models.execute_kw(
    db, uid, password, 'account.account', 'search_read',
    [[['account_type', '=', 'income']]],
    {'fields': ['id', 'name'], 'limit': 1}
)

if not cuentas:
    raise Exception("No se encontró cuenta contable de ingresos")
cuenta_ingresos_id = cuentas[0]['id']

for h in root.findall("habitacion"):
    numero = h.find("numero").text
    tipo = h.find("tipo").text
    capacidad = h.find("capacidad").text
    precio = float(h.find("precio").text)
    disponible = h.find("disponibilidad").text == "1"

    nombre = f"{numero} - {tipo}"
    descripcion = f"Capacidad: {capacidad} personas. Disponible: {'Sí' if disponible else 'No'}"

    # Verificar duplicado
    existe = models.execute_kw(
        db, uid, password, 'product.template', 'search',
        [[['default_code', '=', numero]]]
    )
    if existe:
        print(f"Habitación '{nombre}' ya existe. Omitida.")
        continue

    valores = {
        'name': nombre,
        'type': 'service',
        'list_price': precio,
        'default_code': numero,
        'description': descripcion,
        'active': disponible,
        'property_account_income_id': cuenta_ingresos_id
    }

    product_id = models.execute_kw(db, uid, password, 'product.template', 'create', [valores])
    print(f"Habitación '{nombre}' insertada con ID: {product_id}")

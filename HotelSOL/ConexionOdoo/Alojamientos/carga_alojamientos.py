import xml.etree.ElementTree as ET
import xmlrpc.client

# Leer el archivo XML
tree = ET.parse("alojamientos_intercambio.xml")
root = tree.getroot()

# Conexion a Odoo
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

# Procesar cada alojamiento
for aloj_elem in root.findall("alojamiento"):
    aloj_id = aloj_elem.find("id").text
    tipo_nombre = aloj_elem.find("tipo_nombre").text
    precio = float(aloj_elem.find("precio_base").text)

    nombre_producto = f"{aloj_id} - {tipo_nombre}"

    # Verificar duplicado
    existe = models.execute_kw(
        db, uid, password, 'product.template', 'search',
        [[['name', '=', nombre_producto]]]
    )
    if existe:
        print(f"Alojamiento '{nombre_producto}' ya existe. Omitido.")
        continue

    valores = {
        'name': nombre_producto,
        'type': 'service',
        'list_price': precio,
        'default_code': aloj_id,
        'property_account_income_id': cuenta_ingresos_id
    }

    product_id = models.execute_kw(db, uid, password, 'product.template', 'create', [valores])
    print(f"Alojamiento '{nombre_producto}' insertado con ID: {product_id}")

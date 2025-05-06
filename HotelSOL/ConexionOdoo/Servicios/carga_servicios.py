import xml.etree.ElementTree as ET
import xmlrpc.client

# Leer el archivo XML
tree = ET.parse("servicios_intercambio.xml")
root = tree.getroot()

# Conexion a Odoo
url = "http://127.0.0.1:8071"
db = "hotelsol"
username = "egamerolopez@uoc.edu"
password = "HotelSol123"

common = xmlrpc.client.ServerProxy(f"{url}/xmlrpc/2/common")
uid = common.authenticate(db, username, password, {})
models = xmlrpc.client.ServerProxy(f"{url}/xmlrpc/2/object")

# Obtener cuenta de ingresos
cuentas_ingreso = models.execute_kw(
    db, uid, password, 'account.account', 'search_read',
    [[['account_type', '=', 'income']]],
    {'fields': ['id'], 'limit': 1}
)

if not cuentas_ingreso:
    raise Exception("No se encontró ninguna cuenta contable de ingresos.")
cuenta_ingresos_id = cuentas_ingreso[0]['id']

# Insertar servicios si no existen
for servicio in root.findall("servicio"):
    nombre = servicio.find("nombre").text
    precio = float(servicio.find("precio").text)
    descripcion = servicio.find("descripcion").text

    existe = models.execute_kw(
        db, uid, password,
        'product.template', 'search',
        [[['name', '=', nombre]]]
    )

    if existe:
        print(f"Servicio '{nombre}' ya existe. Omitido.")
        continue

    valores = {
        'name': nombre,
        'type': 'service',
        'list_price': precio,
        'description': descripcion,
        'property_account_income_id': cuenta_ingresos_id
    }

    template_id = models.execute_kw(db, uid, password, 'product.template', 'create', [valores])
    print(f"Servicio '{nombre}' insertado con template ID: {template_id}")

    # También actualizamos el product.product asociado
    product_ids = models.execute_kw(db, uid, password, 'product.product', 'search', [[['product_tmpl_id', '=', template_id]]])
    if product_ids:
        models.execute_kw(db, uid, password, 'product.product', 'write', [[product_ids[0]], {
            'property_account_income_id': cuenta_ingresos_id
        }])
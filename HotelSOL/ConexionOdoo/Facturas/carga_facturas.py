import xml.etree.ElementTree as ET
import xmlrpc.client

# Leer el XML
tree = ET.parse("facturas2.xml")
root = tree.getroot()

# Conexion a Odoo
url = "http://127.0.0.1:8071"
db = "hotelsol"
username = "egamerolopez@uoc.edu"
password = "HotelSol123"

common = xmlrpc.client.ServerProxy(f"{url}/xmlrpc/2/common")
uid = common.authenticate(db, username, password, {})
models = xmlrpc.client.ServerProxy(f"{url}/xmlrpc/2/object")

# Obtener el diario correcto (por código INV)
diarios = models.execute_kw(
    db, uid, password, 'account.journal', 'search_read',
    [[['code', '=', 'INV']]],
    {'fields': ['id'], 'limit': 1}
)
diario_id = diarios[0]['id']
print(f"Diario de ventas existente (INV): ID {diario_id}")

# Cuenta de ingresos (solo para mostrar)
cuentas_ingreso = models.execute_kw(
    db, uid, password, 'account.account', 'search_read',
    [[['account_type', '=', 'income']]],
    {'fields': ['id', 'name', 'code'], 'limit': 1}
)
cuenta_ingresos_id = cuentas_ingreso[0]['id']
cuenta_nombre = f"{cuentas_ingreso[0]['code']} {cuentas_ingreso[0]['name']}"
print(f"Cuenta de ingresos encontrada: {cuenta_ingresos_id} ({cuenta_nombre})")

# Crear facturas
for factura in root.findall("factura"):
    cliente = factura.find("cliente").text
    email = factura.find("email").text
    fecha = factura.find("fecha").text

    # Obtener o crear cliente
    partner_ids = models.execute_kw(
        db, uid, password, 'res.partner', 'search', [[['email', '=', email]]]
    )
    if not partner_ids:
        partner_id = models.execute_kw(
            db, uid, password, 'res.partner', 'create',
            [{'name': cliente, 'email': email}]
        )
    else:
        partner_id = partner_ids[0]

    # Verificar si ya existe una factura con ese cliente y esa fecha
    factura_existente = models.execute_kw(
        db, uid, password, 'account.move', 'search',
        [[
            ['move_type', '=', 'out_invoice'],
            ['partner_id', '=', partner_id],
            ['invoice_date', '=', fecha]
        ]]
    )
    if factura_existente:
        print(f"Factura para {cliente} del {fecha} ya existe. Omitida.")
        continue

    lineas = []
    for linea in factura.find("lineas").findall("linea"):
        servicio = linea.find("servicio").text
        cantidad = float(linea.find("cantidad").text)
        precio = float(linea.find("precio").text)

        product_ids = models.execute_kw(
            db, uid, password, 'product.product', 'search',
            [[['name', '=', servicio]]]
        )
        if not product_ids:
            raise Exception(f"Producto '{servicio}' no encontrado.")
        product_id = product_ids[0]

        product_data = models.execute_kw(
            db, uid, password, 'product.product', 'read', [product_id],
            {'fields': ['property_account_income_id', 'product_tmpl_id']}
        )[0]

        account_id = product_data.get('property_account_income_id')
        if not account_id:
            tmpl_id = product_data['product_tmpl_id'][0]
            tmpl_data = models.execute_kw(
                db, uid, password, 'product.template', 'read', [tmpl_id],
                {'fields': ['categ_id']}
            )[0]
            categ_id = tmpl_data['categ_id'][0]
            categ_data = models.execute_kw(
                db, uid, password, 'product.category', 'read', [categ_id],
                {'fields': ['property_account_income_categ_id']}
            )[0]
            account_id = categ_data['property_account_income_categ_id']
            if not account_id:
                raise Exception(f"El producto '{servicio}' no tiene cuenta contable ni su categoría.")
        if isinstance(account_id, (list, tuple)):
            account_id = account_id[0]

        lineas.append((0, 0, {
            'product_id': product_id,
            'quantity': cantidad,
            'price_unit': precio,
            'name': servicio,
            'account_id': account_id,
            'tax_ids': [(6, 0, [])]
        }))

    print(f"\nLíneas de factura para '{cliente}':")
    for l in lineas:
        print(l)

    factura_id = models.execute_kw(db, uid, password, 'account.move', 'create', [{
        'move_type': 'out_invoice',
        'partner_id': partner_id,
        'invoice_date': fecha,
        'journal_id': diario_id,
        'invoice_line_ids': lineas
    }])

    print(f"Factura creada con ID: {factura_id}")

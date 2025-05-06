import xmlrpc.client

# Conexion a Odoo
url = "http://127.0.0.1:8071"
db = "hotelsol"
username = "egamerolopez@uoc.edu"
password = "HotelSol123"

common = xmlrpc.client.ServerProxy(f"{url}/xmlrpc/2/common")
uid = common.authenticate(db, username, password, {})
models = xmlrpc.client.ServerProxy(f"{url}/xmlrpc/2/object")

# Buscar la cuenta 700000 (Ingresos)
cuenta_id = models.execute_kw(
    db, uid, password, 'account.account', 'search',
    [[['code', '=', '700000']]],
    {'limit': 1}
)
if not cuenta_id:
    raise Exception("No se encontro la cuenta 700000.")
cuenta_ingresos_id = cuenta_id[0]
print(f"Cuenta 700000 encontrada con ID: {cuenta_ingresos_id}")

# Buscar TODAS las categorias
categorias = models.execute_kw(
    db, uid, password, 'product.category', 'search_read',
    [[]],
    {'fields': ['id', 'name']}
)

print(f"Forzando la cuenta contable en {len(categorias)} categoría(s)...")

# Asignar la cuenta a cada una
for cat in categorias:
    models.execute_kw(
        db, uid, password, 'product.category', 'write',
        [[cat['id']], {'property_account_income_categ_id': cuenta_ingresos_id}]
    )
    print(f"Categoria '{cat['name']}' actualizada.")

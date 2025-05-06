# test_facturas_odoo.py
import xmlrpc.client

def test_facturas_en_odoo():
    url = "http://127.0.0.1:8071"
    db = "hotelsol"
    username = "egamerolopez@uoc.edu"
    password = "HotelSol123"

    common = xmlrpc.client.ServerProxy(f"{url}/xmlrpc/2/common")
    uid = common.authenticate(db, username, password, {})
    models = xmlrpc.client.ServerProxy(f"{url}/xmlrpc/2/object")

    facturas = models.execute_kw(db, uid, password, 'account.move', 'search_read', [
        [('move_type', '=', 'out_invoice')]
    ], {'fields': ['name', 'invoice_line_ids', 'partner_id']})

    if not facturas:
        print("No se encontraron facturas creadas en Odoo.")
        return

    errores = 0
    print(f"Facturas encontradas: {len(facturas)}")

    for f in facturas:
        if not f['invoice_line_ids']:
            print(f"Factura '{f['name']}' sin líneas.")
            errores += 1

        if not f['partner_id']:
            print(f"Factura '{f['name']}' sin cliente asociado.")
            errores += 1

    if errores == 0:
        print("Todas las facturas en Odoo tienen cliente y líneas asociadas.")

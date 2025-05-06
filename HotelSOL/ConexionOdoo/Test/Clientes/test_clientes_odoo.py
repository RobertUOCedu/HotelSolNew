# test_clientes_odoo.py
import xmlrpc.client

def test_clientes_en_odoo():
    url = "http://127.0.0.1:8071"
    db = "hotelsol"
    username = "egamerolopez@uoc.edu"
    password = "HotelSol123"

    common = xmlrpc.client.ServerProxy(f"{url}/xmlrpc/2/common")
    uid = common.authenticate(db, username, password, {})
    models = xmlrpc.client.ServerProxy(f"{url}/xmlrpc/2/object")

    # Buscar todos los partners tipo contacto
    partners = models.execute_kw(db, uid, password, 'res.partner', 'search_read',
        [[['type', '=', 'contact']]], {'fields': ['name', 'email', 'type', 'category_id']})

    if not partners:
        print("No se encontraron contactos creados en Odoo.")
        return

    print(f"Contactos encontrados: {len(partners)}")

    # Validar que los VIP tienen categoria asignada
    for p in partners:
        if "vip" in p['name'].lower() and not p['category_id']:
            print(f"Cliente con nombre '{p['name']}' parece VIP pero no tiene categoría asignada.")
        elif p['category_id']:
            print(f"Cliente '{p['name']}' tiene categoría asignada: {p['category_id']}")
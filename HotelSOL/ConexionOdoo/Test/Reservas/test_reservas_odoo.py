# test_reservas_odoo.py
import xmlrpc.client

def test_reservas_en_odoo():
    url = "http://127.0.0.1:8071"
    db = "hotelsol"
    username = "egamerolopez@uoc.edu"
    password = "HotelSol123"

    common = xmlrpc.client.ServerProxy(f"{url}/xmlrpc/2/common")
    uid = common.authenticate(db, username, password, {})
    models = xmlrpc.client.ServerProxy(f"{url}/xmlrpc/2/object")

    eventos = models.execute_kw(db, uid, password, 'calendar.event', 'search_read', [
        [['name', 'ilike', 'Reserva de']]
    ], {'fields': ['name', 'start', 'stop', 'description']})

    if not eventos:
        print("No se encontraron eventos de reserva en Odoo.")
        return

    print(f"Eventos de reserva encontrados: {len(eventos)}")
    errores = 0

    for e in eventos:
        if not e['start'] or not e['stop']:
            print(f"Evento sin fechas válidas: {e['name']}")
            errores += 1
        if "Habitación" not in e['description']:
            print(f"Descripción incompleta para: {e['name']}")
            errores += 1

    if errores == 0:
        print("Todos los eventos de reserva en Odoo están correctamente formateados.")
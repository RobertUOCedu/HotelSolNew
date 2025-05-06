import xml.etree.ElementTree as ET
import xmlrpc.client
from datetime import datetime

# Leer XML
tree = ET.parse("reservas.xml")
root = tree.getroot()

# Conexion a Odoo
url = "http://127.0.0.1:8071"
db = "hotelsol"
username = "egamerolopez@uoc.edu"
password = "HotelSol123"

common = xmlrpc.client.ServerProxy(f"{url}/xmlrpc/2/common")
uid = common.authenticate(db, username, password, {})
models = xmlrpc.client.ServerProxy(f"{url}/xmlrpc/2/object")

for r in root.findall("reserva"):
    cliente = r.find("cliente").text
    email = r.find("email").text
    habitacion = r.find("habitacion").text
    entrada = r.find("fecha_entrada").text
    salida = r.find("fecha_salida").text
    precio = r.find("precio").text

    name = f"Reserva de {habitacion} para {cliente}"
    description = f"Cliente: {cliente} ({email})\nHabitacion: {habitacion}\nPrecio por noche: {precio}"

    # Verificar si ya existe el evento exacto (opcional)
    eventos = models.execute_kw(
        db, uid, password, 'calendar.event', 'search',
        [[['name', '=', name], ['start', '=', entrada]]]
    )
    if eventos:
        print(f"Evento '{name}' ya existe. Omitido.")
        continue

    # Crear evento
    evento_id = models.execute_kw(
        db, uid, password, 'calendar.event', 'create',
        [{
            'name': name,
            'start': entrada,
            'stop': salida,
            'description': description,
        }]
    )
    print(f"Evento creado: {name} (ID: {evento_id})")

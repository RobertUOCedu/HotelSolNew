import pyodbc
import xmlrpc.client

# 1. Conexion a SQL Server
conn = pyodbc.connect(
    "DRIVER={ODBC Driver 17 for SQL Server};SERVER=localhost;DATABASE=hotelsol;Trusted_Connection=yes;"
)
cursor = conn.cursor()

# Traer habitaciones con su disponibilidad actual
cursor.execute("SELECT Numero, Disponibilidad FROM Habitaciones")
habitaciones = cursor.fetchall()

# 2. Conexion a Odoo
url = "http://127.0.0.1:8071"
db = "hotelsol"
username = "egamerolopez@uoc.edu"
password = "HotelSol123"

common = xmlrpc.client.ServerProxy(f"{url}/xmlrpc/2/common")
uid = common.authenticate(db, username, password, {})
models = xmlrpc.client.ServerProxy(f"{url}/xmlrpc/2/object")

actualizadas = 0

for habitacion in habitaciones:
    numero = habitacion.Numero
    disponible = habitacion.Disponibilidad == 1

    # Buscar variante por default_code
    product_variant_ids = models.execute_kw(
        db, uid, password, 'product.product', 'search',
        [[['default_code', '=', numero]]],
        {'context': {'active_test': False}}
    )


    if not product_variant_ids:
        print(f"Habitacion con cdigo '{numero}' no encontrada.")
        continue

    # Obtener plantilla relacionada
    plantilla_id = models.execute_kw(
        db, uid, password, 'product.product', 'read',
        [product_variant_ids], {'fields': ['product_tmpl_id']}
    )[0]['product_tmpl_id'][0]

    # Actualizar estado activo/inactivo en la plantilla
    models.execute_kw(
        db, uid, password, 'product.template', 'write',
        [[plantilla_id], {'active': disponible}]
    )

    print(f"Habitacion '{numero}' marcada como {'activa' if disponible else 'inactiva'}")
    actualizadas += 1

print(f"\n Sincronizacion completada. Habitaciones actualizadas: {actualizadas}")
conn.close()

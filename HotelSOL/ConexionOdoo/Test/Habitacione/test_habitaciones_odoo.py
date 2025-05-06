# test_habitaciones_odoo.py
import pyodbc
import xmlrpc.client

def test_habitaciones_odoo_vs_sql():
    # SQL Server
    conn = pyodbc.connect(
        "DRIVER={ODBC Driver 17 for SQL Server};SERVER=localhost;DATABASE=hotelsol;Trusted_Connection=yes;"
    )
    cursor = conn.cursor()
    cursor.execute("SELECT Numero, Disponibilidad FROM Habitaciones")
    habitaciones_sql = {row.Numero: row.Disponibilidad == 1 for row in cursor.fetchall()}
    conn.close()

    # Odoo
    url = "http://127.0.0.1:8071"
    db = "hotelsol"
    username = "egamerolopez@uoc.edu"
    password = "HotelSol123"

    common = xmlrpc.client.ServerProxy(f"{url}/xmlrpc/2/common")
    uid = common.authenticate(db, username, password, {})
    models = xmlrpc.client.ServerProxy(f"{url}/xmlrpc/2/object")

    productos = models.execute_kw(db, uid, password, 'product.template', 'search_read', [
        [('default_code', '!=', False), ('type', '=', 'service')]
    ], {'fields': ['name', 'default_code', 'active', 'property_account_income_id']})

    errores = 0
    for p in productos:
        codigo = p['default_code']
        activo = p['active']
        cuenta = p['property_account_income_id']

        if codigo not in habitaciones_sql:
            print(f"Codigo '{codigo}' no encontrado en SQL Server.")
            errores += 1
            continue

        disponible_sql = habitaciones_sql[codigo]
        if disponible_sql != activo:
            print(f"Mismatch disponibilidad para '{codigo}': SQL={disponible_sql}, Odoo={activo}")
            errores += 1

        if not cuenta:
            print(f"Habitacion '{codigo}' sin cuenta contable en Odoo.")
            errores += 1

    if errores == 0:
        print("Disponibilidad y cuenta contable de habitaciones sincronizadas correctamente.")

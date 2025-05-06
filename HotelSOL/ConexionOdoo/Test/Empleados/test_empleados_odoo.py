# test_empleados_odoo.py
import xmlrpc.client

def test_empleados_en_odoo():
    url = "http://127.0.0.1:8071"
    db = "hotelsol"
    username = "egamerolopez@uoc.edu"
    password = "HotelSol123"

    common = xmlrpc.client.ServerProxy(f"{url}/xmlrpc/2/common")
    uid = common.authenticate(db, username, password, {})
    models = xmlrpc.client.ServerProxy(f"{url}/xmlrpc/2/object")

    empleados = models.execute_kw(db, uid, password, 'hr.employee', 'search_read',
        [[]], {'fields': ['name', 'work_email', 'department_id']})

    if not empleados:
        print("No se encontraron empleados en Odoo.")
        return

    print(f"Empleados registrados: {len(empleados)}")
    for emp in empleados:
        if not emp['department_id']:
            print(f"Empleado '{emp['name']}' sin departamento asignado.")
        else:
            print(f"Empleado '{emp['name']}' asignado a: {emp['department_id'][1]}")

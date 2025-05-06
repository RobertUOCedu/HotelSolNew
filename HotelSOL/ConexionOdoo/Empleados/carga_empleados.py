import xml.etree.ElementTree as ET
import xmlrpc.client

tree = ET.parse("empleados.xml")
root = tree.getroot()

# Conexion Odoo
url = "http://127.0.0.1:8071"
db = "hotelsol"
username = "egamerolopez@uoc.edu"
password = "HotelSol123"

common = xmlrpc.client.ServerProxy(f"{url}/xmlrpc/2/common")
uid = common.authenticate(db, username, password, {})
models = xmlrpc.client.ServerProxy(f"{url}/xmlrpc/2/object")

# Cache de departamentos
departamentos_ids = {}

for emp in root.findall("empleado"):
    nombre = emp.find("nombre").text
    email = emp.find("email").text
    movil = emp.find("movil").text
    depto = emp.find("departamento").text

    # Verificar o crear departamento
    if depto not in departamentos_ids:
        resultado = models.execute_kw(
            db, uid, password, 'hr.department', 'search',
            [[['name', '=', depto]]]
        )
        if not resultado:
            dept_id = models.execute_kw(
                db, uid, password, 'hr.department', 'create',
                [{'name': depto}]
            )
            print(f"Departamento '{depto}' creado con ID: {dept_id}")
        else:
            dept_id = resultado[0]

        departamentos_ids[depto] = dept_id
    else:
        dept_id = departamentos_ids[depto]

    # Evitar duplicados
    existe = models.execute_kw(
        db, uid, password, 'hr.employee', 'search',
        [[['name', '=', nombre]]]
    )
    if existe:
        print(f"Empleado '{nombre}' ya existe. Omitido.")
        continue

    # Crear empleado
    emp_id = models.execute_kw(
        db, uid, password, 'hr.employee', 'create',
        [{
            'name': nombre,
            'work_email': email,
            'mobile_phone': movil,
            'department_id': dept_id
        }]
    )
    print(f"Empleado '{nombre}' insertado en Odoo con ID: {emp_id}")

# test_conexion_odoo.py
import xmlrpc.client

def test_odoo_connection():
    try:
        url = "http://127.0.0.1:8071"
        db = "hotelsol"
        username = "egamerolopez@uoc.edu"
        password = "HotelSol123"

        common = xmlrpc.client.ServerProxy(f"{url}/xmlrpc/2/common")
        uid = common.authenticate(db, username, password, {})
        assert uid is not None
        print(" Conexión a Odoo correcta.")
    except Exception as e:
        print(f" Error de conexión a Odoo: {e}")
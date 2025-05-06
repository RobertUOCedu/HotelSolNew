import pyodbc
import re

# Conexion a SQL Server
conn = pyodbc.connect(
    "DRIVER={ODBC Driver 17 for SQL Server};SERVER=localhost;DATABASE=hotelsol;Trusted_Connection=yes;"
)
cursor = conn.cursor()

# Consulta con JOIN entre Clientes y Usuarios
cursor.execute("""
    SELECT u.Id, u.Nombre, u.Apellido, u.Email, u.Movil, c.EsVIP
    FROM Clientes c
    JOIN Usuarios u ON c.Id = u.Id
""")

clientes = cursor.fetchall()

# Expresion regular simple para validar emails
def es_email_valido(email):
    return re.match(r"[^@]+@[^@]+\.[^@]+", email)

print("Clientes válidos encontrados:")
for cliente in clientes:
    if not es_email_valido(cliente.Email):
        print(f"Email inválido, se omite: {cliente.Email}")
        continue

    if not cliente.Nombre or not cliente.Apellido:
        print(f"Nombre o apellido incompletos, se omite ID {cliente.Id}")
        continue

    print({
        "id": cliente.Id,
        "nombre": cliente.Nombre,
        "apellido": cliente.Apellido,
        "email": cliente.Email,
        "movil": cliente.Movil,
        "es_vip": cliente.EsVIP
    })

conn.close()

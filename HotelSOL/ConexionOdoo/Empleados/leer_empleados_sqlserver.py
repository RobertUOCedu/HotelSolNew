import pyodbc

# Conexion a SQL Server
conn = pyodbc.connect(
    "DRIVER={ODBC Driver 17 for SQL Server};SERVER=localhost;DATABASE=hotelsol;Trusted_Connection=yes;"
)
cursor = conn.cursor()

# Administradores
cursor.execute("""
    SELECT u.Id, u.Nombre, u.Apellido, u.Email, u.Movil
    FROM Administradores a
    JOIN Usuarios u ON a.Id = u.Id
""")
administradores = cursor.fetchall()

print("Administradores encontrados:")
for a in administradores:
    print({
        "id": a.Id,
        "nombre": a.Nombre,
        "apellido": a.Apellido,
        "email": a.Email,
        "movil": a.Movil,
        "departamento": "Administradores"
    })

# Recepcionistas
cursor.execute("""
    SELECT u.Id, u.Nombre, u.Apellido, u.Email, u.Movil
    FROM Recepcionistas r
    JOIN Usuarios u ON r.Id = u.Id
""")
recepcionistas = cursor.fetchall()

print("\nRecepcionistas encontrados:")
for r in recepcionistas:
    print({
        "id": r.Id,
        "nombre": r.Nombre,
        "apellido": r.Apellido,
        "email": r.Email,
        "movil": r.Movil,
        "departamento": "Recepcionistas"
    })

conn.close()

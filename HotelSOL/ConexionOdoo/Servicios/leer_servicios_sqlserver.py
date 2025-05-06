import pyodbc

# Conexion a SQL Server
conn = pyodbc.connect(
    "DRIVER={ODBC Driver 17 for SQL Server};SERVER=localhost;DATABASE=hotelsol;Trusted_Connection=yes;"
)
cursor = conn.cursor()

# Consulta a la tabla Servicios
cursor.execute("""
    SELECT Id, Nombre, Precio, Descripcion
    FROM Servicios
""")

servicios = cursor.fetchall()

print("Servicios encontrados:")
for servicio in servicios:
    print({
        "id": servicio.Id,
        "nombre": servicio.Nombre,
        "precio": servicio.Precio,
        "descripcion": servicio.Descripcion
    })

conn.close()

import pyodbc

# Conexion a SQL Server
conn = pyodbc.connect(
    "DRIVER={ODBC Driver 17 for SQL Server};SERVER=localhost;DATABASE=hotelsol;Trusted_Connection=yes;"
)
cursor = conn.cursor()

# Consulta con JOIN a TipoAlojamiento
cursor.execute("""
    SELECT a.Id, a.TipoId, t.Nombre AS TipoNombre, a.Precio
    FROM Alojamientos a
    JOIN TipoAlojamientos t ON a.TipoId = t.Id
""")

alojamientos = cursor.fetchall()

print("Alojamientos encontrados:")
for a in alojamientos:
    print({
        "id": a.Id,
        "tipo_id": a.TipoId,
        "tipo_nombre": a.TipoNombre,
        "precio_base": a.Precio
    })

conn.close()
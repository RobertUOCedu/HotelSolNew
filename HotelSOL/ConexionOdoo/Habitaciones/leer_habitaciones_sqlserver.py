import pyodbc

# Conexion a SQL Server
conn = pyodbc.connect(
    "DRIVER={ODBC Driver 17 for SQL Server};SERVER=localhost;DATABASE=hotelsol;Trusted_Connection=yes;"
)
cursor = conn.cursor()

# JOIN con TipoHabitacion sin filtrar por disponibilidad
cursor.execute("""
    SELECT h.Id, h.Numero, th.Nombre AS Tipo, h.Capacidad, h.Precio, h.Disponibilidad
    FROM Habitaciones h
    JOIN TipoHabitaciones th ON h.TipoHabitacionId = th.Id
""")

habitaciones = cursor.fetchall()

print("Habitaciones registradas en el sistema:")
for h in habitaciones:
    print({
        "id": h.Id,
        "numero": h.Numero,
        "tipo": h.Tipo,
        "capacidad": h.Capacidad,
        "precio": h.Precio,
        "disponibilidad": "Si" if h.Disponibilidad else "No"
    })

conn.close()

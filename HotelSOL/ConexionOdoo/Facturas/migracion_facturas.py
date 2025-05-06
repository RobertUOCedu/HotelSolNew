import pyodbc
import xml.etree.ElementTree as ET

conn = pyodbc.connect(
    "DRIVER={ODBC Driver 17 for SQL Server};SERVER=localhost;DATABASE=hotelsol;Trusted_Connection=yes;"
)
cursor = conn.cursor()

# Usamos LEFT JOIN por si no hay servicios vinculados
cursor.execute("""
    SELECT 
        f.Id AS FacturaId, 
        f.FechaEmision, 
        f.Total,
        f.MetodoPago,
        f.Pagada,
        u.Nombre,
        u.Apellido,
        u.Email,
        s.Nombre AS Servicio,
        dfs.Cantidad,
        dfs.PrecioUnitario
    FROM Facturas f
    JOIN Reservas r ON f.ReservaId = r.Id
    JOIN Usuarios u ON r.ClienteId = u.Id
    LEFT JOIN DetalleFacturaServicios dfs ON dfs.FacturaId = f.Id
    LEFT JOIN Servicios s ON s.Id = dfs.ServicioId
    ORDER BY f.Id
""")

facturas = {}

for row in cursor.fetchall():
    fid = row.FacturaId
    if fid not in facturas:
        facturas[fid] = {
            "fecha": str(row.FechaEmision.date()),
            "cliente": f"{row.Nombre or ''} {row.Apellido or ''}".strip(),
            "email": row.Email or '',
            "total": row.Total or 0,
            "lineas": []
        }

    servicio = row.Servicio
    cantidad = row.Cantidad
    precio = row.PrecioUnitario

    if servicio:  # Solo si el nombre del servicio es valido
        facturas[fid]["lineas"].append({
            "servicio": servicio,
            "cantidad": cantidad or 1,
            "precio": precio or 0
        })

# XML
root = ET.Element("facturas")
facturas_generadas = 0

for fid, datos in facturas.items():
    f_elem = ET.SubElement(root, "factura")
    ET.SubElement(f_elem, "id").text = str(fid)
    ET.SubElement(f_elem, "fecha").text = datos["fecha"]
    ET.SubElement(f_elem, "cliente").text = datos["cliente"]
    ET.SubElement(f_elem, "email").text = datos["email"]
    lineas_elem = ET.SubElement(f_elem, "lineas")

    if not datos["lineas"]:
        # Si no hay servicios validos, se añade linea generica
        print(f"Factura {fid} sin líneas válidas. Se añade 'Alojamiento base'.")
        l_elem = ET.SubElement(lineas_elem, "linea")
        ET.SubElement(l_elem, "servicio").text = "Alojamiento base"
        ET.SubElement(l_elem, "cantidad").text = "1"
        ET.SubElement(l_elem, "precio").text = str(datos["total"])
    else:
        for l in datos["lineas"]:
            l_elem = ET.SubElement(lineas_elem, "linea")
            ET.SubElement(l_elem, "servicio").text = l["servicio"]
            ET.SubElement(l_elem, "cantidad").text = str(l["cantidad"])
            ET.SubElement(l_elem, "precio").text = str(l["precio"])

    facturas_generadas += 1

# Guardar XML si hay algo
if facturas_generadas > 0:
    ET.ElementTree(root).write("facturas2.xml", encoding="utf-8", xml_declaration=True)
    print(f"Archivo 'facturas2.xml' generado con {facturas_generadas} factura(s).")
else:
    print("No se generó ninguna factura. Verifica los datos.")

conn.close()

# test_facturas_xml.py
import xml.etree.ElementTree as ET

def test_facturas_xml():
    tree = ET.parse("facturas.xml")
    root = tree.getroot()
    errores = 0

    for f in root.findall("factura"):
        cliente = f.find("cliente").text or ""
        email = f.find("email").text or ""
        fecha = f.find("fecha").text or ""
        lineas = f.find("lineas").findall("linea")

        if not cliente.strip() or not email.strip() or not fecha.strip():
            print(f"Factura incompleta: cliente={cliente}, email={email}, fecha={fecha}")
            errores += 1

        if not lineas:
            print(f"Factura {f.find('id').text} sin líneas (esperamos línea genérica)")
        else:
            for l in lineas:
                servicio = l.find("servicio").text or ""
                cantidad = l.find("cantidad").text or ""
                precio = l.find("precio").text or ""

                if not servicio.strip():
                    print("Línea sin nombre de servicio")
                    errores += 1
                try:
                    float(cantidad)
                    float(precio)
                except:
                    print(f"Línea con cantidad o precio inválido: {cantidad}, {precio}")
                    errores += 1

    if errores == 0:
        print("Todas las facturas y líneas del XML son válidas.")

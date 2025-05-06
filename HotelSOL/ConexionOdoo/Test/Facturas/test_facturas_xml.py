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
            print(f"Factura {f.find('id').text} sin l�neas (esperamos l�nea gen�rica)")
        else:
            for l in lineas:
                servicio = l.find("servicio").text or ""
                cantidad = l.find("cantidad").text or ""
                precio = l.find("precio").text or ""

                if not servicio.strip():
                    print("L�nea sin nombre de servicio")
                    errores += 1
                try:
                    float(cantidad)
                    float(precio)
                except:
                    print(f"L�nea con cantidad o precio inv�lido: {cantidad}, {precio}")
                    errores += 1

    if errores == 0:
        print("Todas las facturas y l�neas del XML son v�lidas.")

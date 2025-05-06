# test_conexion_sqlserver.py
import pyodbc

def test_sqlserver_connection():
    try:
        conn = pyodbc.connect(
            "DRIVER={ODBC Driver 17 for SQL Server};SERVER=localhost;DATABASE=hotelsol;Trusted_Connection=yes;"
        )
        cursor = conn.cursor()
        cursor.execute("SELECT 1")
        result = cursor.fetchone()
        assert result[0] == 1
        print("Conexión a SQL Server correcta.")
        conn.close()
    except Exception as e:
        print(f"Error de conexión a SQL Server: {e}")
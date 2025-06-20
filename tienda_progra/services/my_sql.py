# sql.py
import mysql.connector

def conectar(consulta_sql):
    # Credenciales para la conexión
    config = {
        'user': 'u0mpxrljxh9li3i2',
        'password': 'ElcAh83krxavLWk44FL4',
        'host': 'bdtfzwhm8vhxrkdbh4k1-mysql.services.clever-cloud.com',
        'database': 'bdtfzwhm8vhxrkdbh4k1',
        'raise_on_warnings': True
    }

    try:
        conexion = mysql.connector.connect(**config)
        print("✅ Conexión exitosa a la base de datos.")

        consulta = conexion.cursor()
        consulta.execute(consulta_sql)
        resultado = consulta.fetchall()

        conexion.close()
        return resultado

    except mysql.connector.Error as err:
        print(f"❌ Error al conectar a la base de datos: {err}")
        return []  # <- IMPORTANTE: retorna lista vacía para evitar errores

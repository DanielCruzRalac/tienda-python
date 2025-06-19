import mysql.connector


def manipular(consulta_sql, parametros=None):
    config = {
        'user': 'u0mpxrljxh9li3i2',
        'password': 'ElcAh83krxavLWk44FL4',
        'host': 'bdtfzwhm8vhxrkdbh4k1-mysql.services.clever-cloud.com',
        'database': 'bdtfzwhm8vhxrkdbh4k1',
        'raise_on_warnings': True
    }

    try:
        conexion = mysql.connector.connect(**config)
        cursor = conexion.cursor()

        # Ejecutar con o sin parámetros
        if parametros:
            cursor.execute(consulta_sql, parametros)
        else:
            cursor.execute(consulta_sql)

        # Si es una consulta SELECT, obtener resultados
        if consulta_sql.strip().lower().startswith("select"):
            resultado = cursor.fetchall()
        else:
            # Para INSERT, UPDATE, DELETE: confirmar cambios
            conexion.commit()
            resultado = cursor.rowcount  # Devuelve cantidad de filas afectadas

        cursor.close()
        conexion.close()
        return resultado

    except mysql.connector.Error as err:
        print(f"Error al conectar a la base de datos: {err}")
        return None


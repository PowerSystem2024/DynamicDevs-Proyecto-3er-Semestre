# app.py
import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT

def run_sql_file(filename, connection):
    with open(filename, 'r') as f:
        sql_commands = f.read()

    # Divide los comandos por punto y coma (excepto los que están entre comillas)
    commands = sql_commands.split(';')

    with connection.cursor() as cursor:
        for command in commands:
            if command.strip():
                cursor.execute(command)
        connection.commit()


def setup_database():
    # Conexión inicial (sin base de datos específica)
    admin_conn = psycopg2.connect(
        host="localhost",
        user="root",
        password="root",
        port="5432"
    )
    admin_conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)

    # Crear la base de datos si no existe
    run_sql_file('database/create_database.sql', admin_conn)
    admin_conn.close()

    # Conexión a la base de datos específica
    db_conn = psycopg2.connect(
        host="localhost",
        user="postgres",
        password="tu_contraseña",
        port="5432",
        database="mantenimiento_db"
    )

    # Ejecutar scripts SQL
    run_sql_file('database/create_tables.sql', db_conn)
    run_sql_file('database/create_indexes.sql', db_conn)

    db_conn.close()
    print("Base de datos y tablas creadas exitosamente!")


if __name__ == "__main__":
    setup_database()

import logging
from logging.handlers import RotatingFileHandler

import psycopg2
from psycopg2 import sql
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
import os
import re


# Configuración básica del logger
def setup_logger():
    """Configura el sistema de logging"""
    logger = logging.getLogger('enertech_db')
    logger.setLevel(logging.DEBUG)

    # Formato de los mensajes
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

    # Handler para consola
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    console_handler.setFormatter(formatter)

    # Handler para archivo (con rotación)
    file_handler = RotatingFileHandler(
        'enertech_db.log',
        maxBytes=1024 * 1024,  # 1MB
        backupCount=5,
        encoding='utf-8'
    )
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(formatter)

    # Añadir handlers al logger
    logger.addHandler(console_handler)
    logger.addHandler(file_handler)

    return logger


# Obtener el logger configurado
log = setup_logger()


def read_sql_file(file_path):
    """Lee el contenido de un archivo SQL"""
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            return file.read()
    except IOError as e:
        log.error(f"Error al leer el archivo {file_path}: {e}")
        raise


def execute_sql_commands(conn, sql_commands):
    """Ejecuta comandos SQL en la conexión proporcionada"""
    with conn.cursor() as cursor:
        try:
            commands = [cmd.strip() for cmd in sql_commands.split(';') if cmd.strip()]
            for command in commands:
                log.debug(f"Executando comando: {command[:100]}...")
                cursor.execute(command)
            conn.commit()
            log.info("Comandos SQL ejecutados exitosamente.")
        except psycopg2.Error as e:
            conn.rollback()
            log.error(f"Error al ejecutar comandos SQL: {e}", exc_info=True)
            raise


def database_exists(conn, db_name):
    """Verifica si la base de datos existe"""
    with conn.cursor() as cursor:
        cursor.execute("SELECT 1 FROM pg_database WHERE datname = %s", (db_name,))
        return cursor.fetchone() is not None


def table_exists(conn, table_name):
    """Verifica si una tabla ya existe en la base de datos"""
    with conn.cursor() as cursor:
        cursor.execute("""
                       SELECT EXISTS (SELECT
                                      FROM information_schema.tables
                                      WHERE table_schema = 'public'
                                        AND table_name = %s);
                       """, (table_name.lower(),))
        return cursor.fetchone()[0]


def index_exists(conn, index_name):
    """Verifica si un índice ya existe en la base de datos"""
    with conn.cursor() as cursor:
        cursor.execute("""
                       SELECT EXISTS (SELECT
                                      FROM pg_indexes
                                      WHERE schemaname = 'public'
                                        AND indexname = %s);
                       """, (index_name.lower(),))
        return cursor.fetchone()[0]


def extract_index_names(sql_content):
    """Extrae los nombres de los índices del contenido SQL"""
    pattern = r'CREATE\s+(?:UNIQUE\s+)?INDEX\s+(?:IF\s+NOT\s+EXISTS\s+)?([^\s(]+)'
    return set(re.findall(pattern, sql_content, re.IGNORECASE))


def main():
    script_dir = os.path.dirname(os.path.abspath(__file__))

    db_config = {
        'host': 'localhost',
        'user': 'postgres',  # Cambia esto si tu usuario es diferente
        'password': 'root',  # Cambia esto si tu contraseña es diferente
        'port': '5432'
    }

    db_name = 'enertech'
    required_tables = ['admins', 'supervisors', 'technicians', "industrial_assets", "work_orders"]

    # Conexión inicial al servidor PostgreSQL
    log.info("Conectando al servidor PostgreSQL...")
    conn = psycopg2.connect(**db_config)
    conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)

    try:
        log.info("Iniciando el proceso de creación de base de datos y tablas...")
        # Crear base de datos si no existe
        if not database_exists(conn, db_name):
            log.info(f"Creando base de datos {db_name}...")
            conn.cursor().execute(sql.SQL("CREATE DATABASE {}").format(sql.Identifier(db_name)))
            log.info("Base de datos creada exitosamente")
        else:
            log.info(f"La base de datos {db_name} ya existe.")

        conn.close()

        # Conexión a la base de datos específica
        db_config['dbname'] = db_name
        log.info(f"Conectando a la base de datos {db_name}...")
        conn = psycopg2.connect(**db_config)

        # Verificar y crear tablas si es necesario
        tables_file = os.path.join(script_dir, 'create_tables.sql')
        if os.path.exists(tables_file):
            missing_tables = [t for t in required_tables if not table_exists(conn, t)]

            if missing_tables:
                log.info(f"Faltan tablas: {', '.join(missing_tables)}. Creando tablas...")
                sql_commands = read_sql_file(tables_file)
                execute_sql_commands(conn, sql_commands)
            else:
                log.info("Todas las tablas ya existen.")
        else:
            log.error("Error: Archivo create_tables.sql no encontrado")

        # Verificar y crear índices si es necesario
        indexes_file = os.path.join(script_dir, 'create_indexes.sql')
        if os.path.exists(indexes_file):
            indexes_content = read_sql_file(indexes_file)
            required_indexes = extract_index_names(indexes_content)

            missing_indexes = [i for i in required_indexes if not index_exists(conn, i)]

            if missing_indexes:
                log.info(f"Faltan índices: {', '.join(missing_indexes)}. Creando índices...")
                execute_sql_commands(conn, indexes_content)
            else:
                log.info("Todos los índices ya existen.")
        else:
            log.error("Advertencia: Archivo create_indexes.sql no encontrado")

        log.info("Proceso completado exitosamente!")

    except psycopg2.OperationalError as e:
        log.critical(f"Error de conexión: {e}", exc_info=True)
    except psycopg2.Error as e:
        log.error(f"Error de PostgreSQL: {e}", exc_info=True)
    except Exception as e:
        log.exception(f"Error inesperado: {e}")
    finally:
        if 'conn' in locals() and conn is not None:
            conn.close()
            log.info("Conexión a la base de datos cerrada.")


if __name__ == '__main__':
    main()

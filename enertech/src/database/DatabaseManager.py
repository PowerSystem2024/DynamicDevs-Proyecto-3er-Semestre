import os
from contextlib import contextmanager

import psycopg2
from enertech.src.AppLogger import AppLogger


class DatabaseManager:
    _log = AppLogger.setup_logger('enertech_db')

    def __init__(self, db_config: dict):
        self._db_config = db_config
        self._conn = None  # se establece con initialize()

    def _stablish_connection(self):
        """Establece la conexión a la base de datos usando la conexion global"""
        try:
            self._conn = psycopg2.connect(**self._db_config)
            self._log.info(f"Conexión establecida a la base de datos {self._db_config['dbname']}.")
        except psycopg2.OperationalError as e:
            self._log.error(f"Error al conectar a la base de datos: {e}", exc_info=True)
            raise
        except Exception as e:
            self._log.exception(f"Error inesperado al establecer conexión: {e}", exc_info=True)
            raise

    def get_connection(self) -> psycopg2.extensions.connection:
        """Devuelve la conexión a la base de datos, estableciéndola si no está activa"""
        if self._conn is None or self._conn.closed:
            self._stablish_connection()
        return self._conn

    @contextmanager
    def transaction(self):
        """Context manager que maneja commit/rollback automático"""
        if self._conn.closed:
            raise RuntimeError("Conexión cerrada")

        try:
            yield
            self._conn.commit()
        except Exception as e:
            self._conn.rollback()
            raise RuntimeError(f"Error en transacción: {str(e)}")

    def close_connection(self):
        """Cierra la conexión a la base de datos"""
        if self._conn is not None:
            self._conn.close()
            self._log.info("Conexión a la base de datos cerrada.")
        else:
            self._log.info("No hay conexión activa para cerrar.")

    def _read_sql_file(self, file_path) -> str:
        """Lee el contenido de un archivo SQL y devuelve su contenido como una cadena"""
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                return file.read()
        except IOError as e:
            self._log.exception(f"Error al leer el archivo {file_path}: {e}")
            raise

    def _execute_sql_commands(self, sql_commands):
        """Ejecuta comandos SQL"""
        try:
            # Dividir los comandos eliminando espacios y líneas vacías
            commands = [cmd.strip() for cmd in sql_commands.split(';') if cmd.strip()]
            with self._conn.cursor() as cursor:
                for command in commands:
                    if command:
                        try:
                            # muestra los primeros 100 caracteres
                            self._log.debug(f"Ejecutando comando: {command[:100]}...")
                            cursor.execute(command)
                            self._log.debug("Comando SQL ejecutado exitosamente.")
                        except psycopg2.Error as e:
                            self._conn.rollback()
                            self._log.error(f"Error al ejecutar comando SQL: {command[:100]}...")
                            self._log.exception(f"Detalle del error: {e}", exc_info=True)
                            raise

                self._conn.commit()
                self._log.debug("Todos los comandos SQL se ejecutaron correctamente.")
        except Exception as e:
            self._log.exception(f"Error inesperado: {e}", exc_info=True)
            raise

    def _database_exists(self) -> bool:
        """Verifica si la DB existe (usa conexión temporal con autocommit)"""
        query = "SELECT 1 FROM pg_database WHERE datname = %s"
        # Se crea una conexión temporal sin la base de datos para verificar su existencia
        connetion_params = {k: v for k, v in self._db_config.items() if
                            k != 'dbname'}  # Excluye 'dbname' para evitar errores de conexión
        temp_conn = psycopg2.connect(**connetion_params)
        temp_conn.autocommit = True  # Necesario en este caso para evitar problemas de transacciones
        exist = False
        try:
            with temp_conn.cursor() as cursor:
                cursor.execute(query, (self._db_config['dbname'],))
                exist = cursor.fetchone() is not None
        finally:
            temp_conn.close()
        return exist

    def _create_database(self):
        """Crea la DB (usa conexión temporal con autocommit)"""
        # Se crea una conexión temporal sin la base de datos para verificar su existencia
        connetion_params = {k: v for k, v in self._db_config.items() if
                            k != 'dbname'}  # Excluye 'dbname' para evitar errores de conexión
        temp_conn = psycopg2.connect(**connetion_params)
        temp_conn.autocommit = True  # Necesario para crear la base de datos

        try:
            with temp_conn.cursor() as cursor:
                self._log.info(f"Creando base de datos {self._db_config['dbname']}...")
                cursor.execute(f"CREATE DATABASE {self._db_config['dbname']}")
                self._log.info("Base de datos creada exitosamente")
        finally:
            temp_conn.close()

    def _create_schema(self):
        """Crea las tablas e índices (usa transacciones explícitas)"""
        try:
            # obtener la ruta del archivo create_tables.sql
            create_tables_file = os.path.join(os.path.dirname(__file__), 'create_tables.sql')
            if os.path.exists(create_tables_file):  # verificar si el archivo existe
                sql_commands = self._read_sql_file(create_tables_file)  # Leer el contenido del archivo
                self._execute_sql_commands(sql_commands)  # Ejecutar los comandos SQL extraídos del archivo
                self._log.info("tablas creadas exitosamente.")

            # obtener la ruta del archivo create_indexes.sql
            create_indexes_file = os.path.join(os.path.dirname(__file__), 'create_indexes.sql')
            if os.path.exists(create_indexes_file):  # verificar si el archivo existe
                sql_commands = self._read_sql_file(create_indexes_file)  # Leer el contenido del archivo
                self._execute_sql_commands(sql_commands)  # Ejecutar los comandos SQL extraídos del archivo
                self._log.info("índices creadas exitosamente.")
        except IOError as e:
            self._log.exception(f"Error al leer el archivo: {e}", exc_info=True)
            raise

    def initialize(self):
        try:
            if not self._database_exists():
                self._create_database()  # Crear la base de datos (usa conexión temporal)
                self._stablish_connection()  # Establecer conexión después de crear la base de datos
                self._create_schema()
                self._log.info(f"Base de datos {self._db_config['dbname']} inicializada correctamente.")
            else:
                self._log.info(f"La base de datos {self._db_config['dbname']} ya existe.")
        except psycopg2.OperationalError as e:
            self._log.critical(f"Error de conexión: {e}", exc_info=True)
        except psycopg2.Error as e:
            self._log.error(f"Error de PostgresSQL: {e}", exc_info=True)
        except Exception as e:
            self._log.exception(f"Error inesperado: {e}")

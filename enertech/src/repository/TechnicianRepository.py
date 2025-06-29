from typing import Optional, List
from enertech.src.database.DatabaseManager import DatabaseManager
from enertech.src.domain.Technician import Technician
from src.domain.UserRole import UserRole
from src.repository.BaseUserRepository import BaseUserRepository
from src.repository.Criteria import Criteria


# Repositorio para manejar operaciones de base de datos para técnicos (Technician)
class TechnicianRepository(BaseUserRepository):
    def __init__(self, db_manager: DatabaseManager):
        """
        Constructor que inicializa el repositorio con un gestor de base de datos.
        :param db_manager: Instancia de DatabaseManager para manejar conexiones a la base de datos.
        """
        super().__init__(db_manager)

    def save(self, technician: Technician) -> Technician:
        """
        Inserta un nuevo técnico en la base de datos y devuelve la entidad creada con el ID asignado.
        :param technician: Instancia de Technician con los datos a insertar.
        :return: Technician con los datos insertados, incluyendo el ID generado.
        """
        query = """
                INSERT INTO technicians (first_name, last_name, email, password, rol, active, max_active_orders)
                VALUES (%s, %s, %s, %s, %s, %s,
                        %s) RETURNING id, first_name, last_name, email, password, rol, active, max_active_orders; \
                """
        with self._db_manager.get_connection().cursor() as cursor:
            cursor.execute(query, (
                technician.first_name,
                technician.last_name,
                technician.email,
                technician.password,
                technician.role.value,
                technician.is_active,
                technician.max_active_orders
            ))
            self._db_manager.commit_transaction()
            result = cursor.fetchone()
            self._db_manager.close_connection()

        return self._row_to_entity(result) if result else None

    def update(self, technician: Technician) -> Optional[Technician]:
        """
        Actualiza un técnico existente en la base de datos y devuelve la entidad actualizada.
        :param technician: Instancia de Technician con los datos actualizados.
        :return: Technician con los datos actualizados, o None si no se encontró el registro.
        """
        query = """
                UPDATE technicians
                SET first_name        = %s,
                    last_name         = %s,
                    email             = %s,
                    password          = %s,
                    rol               = %s,
                    active            = %s,
                    max_active_orders = %s
                WHERE id = %s RETURNING id, first_name, last_name, email, password, rol, active, max_active_orders; \
                """
        with self._db_manager.get_connection().cursor() as cursor:
            cursor.execute(query, (
                technician.first_name,
                technician.last_name,
                technician.email,
                technician.password,
                technician.role.value,
                technician.is_active,
                technician.max_active_orders,
                technician.id
            ))
            self._db_manager.commit_transaction()
            result = cursor.fetchone()
            self._db_manager.close_connection()
        return self._row_to_entity(result) if result else None

    def get_by_id(self, technician_id: int) -> Optional[Technician]:
        """
        Busca y devuelve un técnico por su ID.
        :param technician_id: ID del técnico a buscar.
        :return: Technician si se encuentra, None si no existe.
        """
        query = "SELECT * FROM technicians WHERE id = %s"
        with self._db_manager.get_connection().cursor() as cursor:
            cursor.execute(query, (technician_id,))
            row = cursor.fetchone()

        return self._row_to_entity(row) if row else None

    def get_by_email(self, email: str) -> Optional[Technician]:
        """
        Busca y devuelve un técnico por su correo electrónico.
        :param email: Correo electrónico del técnico a buscar.
        :return: Technician si se encuentra, None si no existe.
        """
        query = "SELECT * FROM technicians WHERE email = %s"
        with self._db_manager.get_connection().cursor() as cursor:
            cursor.execute(query, (email,))
            row = cursor.fetchone()

        return self._row_to_entity(row) if row else None

    def list_by_criteria(self, criteria: dict) -> List[Technician]:
        """
        Lista técnicos que cumplan con ciertos criterios de búsqueda.
        :param criteria: Diccionario con los criterios de búsqueda (ejemplo: {'active': True}).
        :return: Lista de Technician que cumplen con los criterios, o None si no hay resultados.
        """
        _TABLE_NAME = 'TECHNICIANS'
        results = Criteria.list_by_criteria(_TABLE_NAME, self._db_manager, criteria)
        return [self._row_to_entity(result) for result in results]

    def delete(self, technician_id: int) -> bool:
        """
        Elimina un técnico por ID.
        :param technician_id: ID del técnico a eliminar.
        :return: True si se eliminó correctamente, False si no se encontró el registro.
        """
        query = "DELETE FROM technicians WHERE id = %s"
        with self._db_manager.get_connection().cursor() as cursor:
            cursor.execute(query, (technician_id,))
            return cursor.rowcount > 0

    @staticmethod
    def _row_to_entity(row) -> Technician:
        # Metodo auxiliar que convierte una fila de la BD a un objeto Technician
        technician = Technician(
            first_name=row[1],
            last_name=row[2],
            email=row[3],
            password=row[4],
            max_active_orders=row[7])
        technician.id = row[0]
        technician.role = UserRole(row[5])
        technician.is_active = row[6]
        return technician

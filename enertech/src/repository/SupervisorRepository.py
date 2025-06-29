from typing import Optional, List
from enertech.src.database.DatabaseManager import DatabaseManager
from enertech.src.domain.Supervisor import Supervisor
from enertech.src.domain.UserRole import UserRole
from enertech.src.repository.Criteria import Criteria

from enertech.src.repository.BaseUserRepository import BaseUserRepository


# Repositorio para manejar operaciones de base de datos para supervisores
class SupervisorRepository(BaseUserRepository):
    def __init__(self, db_manager: DatabaseManager):
        """
        Constructor que inicializa el repositorio con un gestor de base de datos.
        :param db_manager: Instancia de DatabaseManager para manejar conexiones a la base de datos.
        """
        super().__init__(db_manager)

    def save(self, supervisor: Supervisor) -> Supervisor:
        """
        Inserta un nuevo supervisor en la base de datos y devuelve la entidad creada con el ID asignado.
        :param supervisor: Instancia de Supervisor con los datos a insertar.
        :return: Supervisor con los datos insertados, incluyendo el ID generado.
        """
        query = """
                INSERT INTO supervisors (first_name, last_name, email, password, rol, active, assigned_area)
                VALUES (%s, %s, %s, %s, %s, %s,
                        %s) RETURNING id, first_name, last_name, email, password, rol, active, assigned_area; \
                """
        with self._db_manager.get_connection().cursor() as cursor:
            cursor.execute(query, (
                supervisor.first_name,
                supervisor.last_name,
                supervisor.email,
                supervisor.password,
                supervisor.role.value,
                supervisor.is_active,
                supervisor.assigned_area
            ))
            self._db_manager.commit_transaction()
            result = cursor.fetchone()
            self._db_manager.close_connection()
        return self._map_to_supervisor(result)

    def update(self, supervisor: Supervisor) -> Supervisor:
        """
        Actualiza un supervisor existente en la base de datos y devuelve la entidad actualizada.
        :param supervisor: Instancia de Supervisor con los datos actualizados.
        :return: Supervisor con los datos actualizados.
        """
        query = """
                UPDATE supervisors
                SET first_name    = %s,
                    last_name     = %s,
                    email         = %s,
                    password      = %s,
                    rol           = %s,
                    active        = %s,
                    assigned_area = %s
                WHERE id = %s RETURNING id, first_name, last_name, email, password, rol, active, assigned_area; \
                """
        with self._db_manager.get_connection().cursor() as cursor:
            cursor.execute(query, (
                supervisor.first_name,
                supervisor.last_name,
                supervisor.email,
                supervisor.password,
                supervisor.role.value,
                supervisor.is_active,
                supervisor.assigned_area,
                supervisor.id
            ))
            self._db_manager.commit_transaction()
            result = cursor.fetchone()
            self._db_manager.close_connection()
        return self._map_to_supervisor(result)

    def get_by_id(self, supervisor_id: int) -> Optional[Supervisor]:
        """
        Busca y devuelve un supervisor por su ID.
        :param supervisor_id: ID del supervisor a buscar.
        :return: Supervisor si se encuentra, None si no existe.
        """
        query = """
                SELECT id,
                       first_name,
                       last_name,
                       email,
                       password,
                       rol,
                       active,
                       assigned_area
                FROM supervisors
                WHERE id = %s; \
                """
        with self._db_manager.get_connection().cursor() as cursor:
            cursor.execute(query, (supervisor_id,))
            result = cursor.fetchone()
            self._db_manager.close_connection()
        if result:
            return self._map_to_supervisor(result)
        return None

    def email_exist(self, email: str) -> bool:
        """
        Verifica si un correo electrónico ya existe en la base de datos.
        :param email: Correo electrónico a verificar.
        :return: True si el correo electrónico ya existe, False en caso contrario.
        """
        query = "SELECT COUNT(*) FROM supervisors WHERE email = %s;"
        with self._db_manager.get_connection().cursor() as cursor:
            cursor.execute(query, (email,))
            count = cursor.fetchone()[0]
            self._db_manager.close_connection()
        return count > 0

    def get_by_email(self, email: str) -> Optional[Supervisor]:
        """
        Busca y devuelve un supervisor por su correo electrónico.
        :param email: Correo electrónico del supervisor a buscar.
        :return: Supervisor si se encuentra, None si no existe.
        """
        query = """
                SELECT id,
                       first_name,
                       last_name,
                       email,
                       password,
                       rol,
                       active,
                       assigned_area
                FROM supervisors
                WHERE email = %s; \
                """
        with self._db_manager.get_connection().cursor() as cursor:
            cursor.execute(query, (email,))
            result = cursor.fetchone()
            self._db_manager.close_connection()

        if result:
            return self._map_to_supervisor(result)
        return None

    def list_by_criteria(self, criteria: dict) -> List[Supervisor]:
        """
        Lista supervisores que cumplan con ciertos criterios de búsqueda.
        :param criteria: Diccionario con los criterios de búsqueda (ejemplo: {'active': True, 'assigned_area': 'Zona Norte'}).
        :return: Lista de supervisores que cumplen con los criterios.
        """
        _TABLE_NAME = "SUPERVISORS"
        results = Criteria.list_by_criteria(_TABLE_NAME, self._db_manager, criteria)
        return [self._map_to_supervisor(row) for row in results]

    def delete(self, supervisor_id: int) -> bool:
        """
        Elimina un supervisor por su ID.
        :param supervisor_id: ID del supervisor a eliminar.
        :return: True si se eliminó correctamente, False si no se encontró el registro.
        """
        query = "DELETE FROM supervisors WHERE id = %s;"
        with self._db_manager.get_connection().cursor() as cursor:
            cursor.execute(query, (supervisor_id,))
            self._db_manager.commit_transaction()
            result = cursor.rowcount
            self._db_manager.close_connection()
            return result > 0

    @staticmethod
    def _map_to_supervisor(db_result: tuple[any, ...]) -> Supervisor:
        supervisor = Supervisor(
            first_name=db_result[1],
            last_name=db_result[2],
            email=db_result[3],
            password=db_result[4],
            assigned_area=db_result[7])
        supervisor.id = db_result[0]
        supervisor.role = UserRole(db_result[5])
        supervisor.is_active = db_result[6]

        return supervisor

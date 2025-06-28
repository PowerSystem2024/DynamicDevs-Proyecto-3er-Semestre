from typing import Optional, List
from src.database.DatabaseManager import DatabaseManager
from src.domain.Supervisor import Supervisor

# Repositorio para manejar operaciones de base de datos para supervisores
class SupervisorRepository:
    def __init__(self, db_manager: DatabaseManager):
        """
        Constructor que inicializa el repositorio con un gestor de base de datos.
        :param db_manager: Instancia de DatabaseManager para manejar conexiones a la base de datos.
        """
        self._db_manager = db_manager

    def save(self, supervisor: Supervisor) -> Supervisor:
        """
        Inserta un nuevo supervisor en la base de datos y devuelve la entidad creada con el ID asignado.
        :param supervisor: Instancia de Supervisor con los datos a insertar.
        :return: Supervisor con los datos insertados, incluyendo el ID generado.
        """
        query = """
            INSERT INTO supervisors (
                first_name, last_name, email, password, rol, active, assigned_area
            ) VALUES (%s, %s, %s, %s, %s, %s, %s)
            RETURNING id, first_name, last_name, email, password, rol, active, assigned_area;
        """
        with self._db_manager.get_connection().cursor() as cursor:
            cursor.execute(query, (
                supervisor.first_name,
                supervisor.last_name,
                supervisor.email,
                supervisor.password,
                supervisor.rol,
                supervisor.active,
                supervisor.assigned_area
            ))
            result = cursor.fetchone()

        return Supervisor(
            id=result[0],
            first_name=result[1],
            last_name=result[2],
            email=result[3],
            password=result[4],
            rol=result[5],
            active=result[6],
            assigned_area=result[7]
        )

    def update(self, supervisor: Supervisor) -> Supervisor:
        """
        Actualiza un supervisor existente en la base de datos y devuelve la entidad actualizada.
        :param supervisor: Instancia de Supervisor con los datos actualizados.
        :return: Supervisor con los datos actualizados.
        """
        query = """
            UPDATE supervisors
            SET first_name = %s, last_name = %s, email = %s, password = %s, rol = %s, active = %s, assigned_area = %s
            WHERE id = %s
            RETURNING id, first_name, last_name, email, password, rol, active, assigned_area;
        """
        with self._db_manager.get_connection().cursor() as cursor:
            cursor.execute(query, (
                supervisor.first_name,
                supervisor.last_name,
                supervisor.email,
                supervisor.password,
                supervisor.rol,
                supervisor.active,
                supervisor.assigned_area,
                supervisor.id
            ))
            result = cursor.fetchone()

        return Supervisor(
            id=result[0],
            first_name=result[1],
            last_name=result[2],
            email=result[3],
            password=result[4],
            rol=result[5],
            active=result[6],
            assigned_area=result[7]
        )

    def get_by_id(self, supervisor_id: int) -> Optional[Supervisor]:
        """
        Busca y devuelve un supervisor por su ID.
        :param supervisor_id: ID del supervisor a buscar.
        :return: Supervisor si se encuentra, None si no existe.
        """
        query = """
            SELECT id, first_name, last_name, email, password, rol, active, assigned_area
            FROM supervisors
            WHERE id = %s;
        """
        with self._db_manager.get_connection().cursor() as cursor:
            cursor.execute(query, (supervisor_id,))
            result = cursor.fetchone()

        if result:
            return Supervisor(
                id=result[0],
                first_name=result[1],
                last_name=result[2],
                email=result[3],
                password=result[4],
                rol=result[5],
                active=result[6],
                assigned_area=result[7]
            )
        return None

    def get_by_email(self, email: str) -> Optional[Supervisor]:
        """
        Busca y devuelve un supervisor por su correo electrónico.
        :param email: Correo electrónico del supervisor a buscar.
        :return: Supervisor si se encuentra, None si no existe.
        """
        query = """
            SELECT id, first_name, last_name, email, password, rol, active, assigned_area
            FROM supervisors
            WHERE email = %s;
        """
        with self._db_manager.get_connection().cursor() as cursor:
            cursor.execute(query, (email,))
            result = cursor.fetchone()

        if result:
            return Supervisor(
                id=result[0],
                first_name=result[1],
                last_name=result[2],
                email=result[3],
                password=result[4],
                rol=result[5],
                active=result[6],
                assigned_area=result[7]
            )
        return None

    def list_by_criteria(self, criteria: dict) -> List[Supervisor]:
        """
        Lista supervisores que cumplan con ciertos criterios de búsqueda.
        :param criteria: Diccionario con los criterios de búsqueda (ejemplo: {'active': True, 'assigned_area': 'Zona Norte'}).
        :return: Lista de supervisores que cumplen con los criterios.
        """
        query = "SELECT id, first_name, last_name, email, password, rol, active, assigned_area FROM supervisors WHERE 1=1"
        params = []

        if 'active' in criteria:
            query += " AND active = %s"
            params.append(criteria['active'])

        if 'assigned_area' in criteria:
            query += " AND assigned_area = %s"
            params.append(criteria['assigned_area'])

        with self._db_manager.get_connection().cursor() as cursor:
            cursor.execute(query, tuple(params))
            results = cursor.fetchall()

        return [
            Supervisor(
                id=row[0],
                first_name=row[1],
                last_name=row[2],
                email=row[3],
                password=row[4],
                rol=row[5],
                active=row[6],
                assigned_area=row[7]
            )
            for row in results
        ]

    def delete(self, supervisor_id: int) -> bool:
        """
        Elimina un supervisor por su ID.
        :param supervisor_id: ID del supervisor a eliminar.
        :return: True si se eliminó correctamente, False si no se encontró el registro.
        """
        query = "DELETE FROM supervisors WHERE id = %s;"
        with self._db_manager.get_connection().cursor() as cursor:
            cursor.execute(query, (supervisor_id,))
            return cursor.rowcount > 0
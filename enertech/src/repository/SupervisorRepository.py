from typing import Optional, List
from src.database.DatabaseManager import DatabaseManager
from src.domain.Supervisor import Supervisor

# Repositorio para manejar operaciones de base de datos para supervisores
class SupervisorRepository:
    def __init__(self, db_manager: DatabaseManager):
        self._db_manager = db_manager

    def save(self, supervisor: Supervisor) -> Supervisor:
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
        query = "DELETE FROM supervisors WHERE id = %s;"
        with self._db_manager.get_connection().cursor() as cursor:
            cursor.execute(query, (supervisor_id,))
            return cursor.rowcount > 0
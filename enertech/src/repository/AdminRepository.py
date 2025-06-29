from typing import Optional, List, Dict
from src.database.DatabaseManager import DatabaseManager
from src.domain.Admin import Admin

# Repositorio para manejar operaciones de base de datos para administradores (Admin)
class AdminRepository:
    def __init__(self, db_manager: DatabaseManager):
        """
        Constructor que inicializa el repositorio con un gestor de base de datos.
        :param db_manager: Instancia de DatabaseManager para manejar conexiones a la base de datos.
        """
        self._db_manager = db_manager

    def save(self, admin: Admin) -> Admin:
        """
        Inserta un nuevo administrador en la base de datos y devuelve la entidad creada con el ID asignado.
        :param admin: Instancia de Admin con los datos a insertar.
        :return: Admin con los datos insertados, incluyendo el ID generado.
        """
        query = """
            INSERT INTO admins (
                first_name, last_name, email, password, rol, active, department
            ) VALUES (%s, %s, %s, %s, %s, %s, %s)
            RETURNING id, first_name, last_name, email, password, rol, active, department;
        """
        with self._db_manager.get_connection().cursor() as cursor:
            cursor.execute(query, (
                admin.first_name,
                admin.last_name,
                admin.email,
                admin.password,
                admin.rol,
                admin.active,
                admin.department
            ))
            result = cursor.fetchone()

        return self._row_to_entity(result) if result else None

    def update(self, admin: Admin) -> Optional[Admin]:
        """
        Actualiza un administrador existente en la base de datos y devuelve la entidad actualizada.
        :param admin: Instancia de Admin con los datos actualizados.
        :return: Admin con los datos actualizados, o None si no se encontró el registro.
        """
        query = """
            UPDATE admins
            SET first_name = %s, last_name = %s, email = %s, password = %s, rol = %s,
                active = %s, department = %s
            WHERE id = %s
            RETURNING id, first_name, last_name, email, password, rol, active, department;
        """
        with self._db_manager.get_connection().cursor() as cursor:
            cursor.execute(query, (
                admin.first_name,
                admin.last_name,
                admin.email,
                admin.password,
                admin.rol,
                admin.active,
                admin.department,
                admin.id
            ))
            result = cursor.fetchone()

        return self._row_to_entity(result) if result else None

    def get_by_id(self, admin_id: int) -> Optional[Admin]:
        """
        Busca y devuelve un administrador por su ID.
        :param admin_id: ID del administrador a buscar.
        :return: Admin si se encuentra, None si no existe.
        """
        query = "SELECT * FROM admins WHERE id = %s"
        with self._db_manager.get_connection().cursor() as cursor:
            cursor.execute(query, (admin_id,))
            row = cursor.fetchone()

        return self._row_to_entity(row) if row else None

    def get_by_email(self, email: str) -> Optional[Admin]:
        """
        Busca y devuelve un administrador por su correo electrónico.
        :param email: Correo electrónico del administrador a buscar.
        :return: Admin si se encuentra, None si no existe.
        """
        query = "SELECT * FROM admins WHERE email = %s"
        with self._db_manager.get_connection().cursor() as cursor:
            cursor.execute(query, (email,))
            row = cursor.fetchone()

        return self._row_to_entity(row) if row else None

    def list_by_criteria(self, criteria: Optional[Dict[str, any]] = None, sort: str = "id") -> Optional[List[Admin]]:
        """
        Lista administradores que cumplan con ciertos criterios de búsqueda.
        :param criteria: Diccionario con los criterios de búsqueda (ejemplo: {'active': True}).
        :param sort: Campo por el cual ordenar los resultados (por defecto: 'id').
        :return: Lista de Admin que cumplen con los criterios, o None si no hay resultados.
        """
        query = "SELECT * FROM admins"
        filters = []
        params = []

        if criteria:
            for field, value in criteria.items():
                if value is not None:
                    filters.append(f"{field} ILIKE %s")
                    params.append(f"%{value}%")

        if filters:
            query += " WHERE " + " AND ".join(filters)

        query += f" ORDER BY {sort}"

        with self._db_manager.get_connection().cursor() as cursor:
            cursor.execute(query, params)
            rows = cursor.fetchall()

        return [self._row_to_entity(row) for row in rows] if rows else None

    def delete(self, admin_id: int) -> bool:
        """
        Elimina un administrador por ID.
        :param admin_id: ID del administrador a eliminar.
        :return: True si se eliminó correctamente, False si no se encontró el registro.
        """
        query = "DELETE FROM admins WHERE id = %s"
        with self._db_manager.get_connection().cursor() as cursor:
            cursor.execute(query, (admin_id,))
            return cursor.rowcount > 0

    @staticmethod
    def _row_to_entity(row) -> Admin:
        """
        Convierte una fila de la base de datos en una instancia de Admin.
        :param row: Fila obtenida de la base de datos.
        :return: Instancia de Admin con los datos de la fila.
        """
        return Admin(
            id=row[0],
            first_name=row[1],
            last_name=row[2],
            email=row[3],
            password=row[4],
            rol=row[5],
            active=row[6],
            department=row[7]
        )
from typing import Optional, List, Dict
from enertech.src.database.DatabaseManager import DatabaseManager
from enertech.src.domain.Admin import Admin
from enertech.src.domain.UserRole import UserRole
from enertech.src.repository.BaseUserRepository import BaseUserRepository


# Repositorio para manejar operaciones de base de datos para administradores (Admin)
class AdminRepository(BaseUserRepository):
    def __init__(self, db_manager: DatabaseManager):
        """
        Constructor que inicializa el repositorio con un gestor de base de datos.
        :param db_manager: Instancia de DatabaseManager para manejar conexiones a la base de datos.
        """
        super().__init__(db_manager)

    def save(self, admin: Admin) -> Admin:
        """
        Inserta un nuevo administrador en la base de datos y devuelve la entidad creada con el ID asignado.
        :param admin: Instancia de Admin con los datos a insertar.
        :return: Admin con los datos insertados, incluyendo el ID generado.
        """
        query = """
                INSERT INTO admins (first_name, last_name, email, password, rol, active, department)
                VALUES (%s, %s, %s, %s, %s, %s,
                        %s) RETURNING id, first_name, last_name, email, password, rol, active, department; \
                """
        with self._db_manager.get_connection().cursor() as cursor:
            cursor.execute(query, (
                admin.first_name,
                admin.last_name,
                admin.email,
                admin.password,
                admin.role,
                admin.is_active,
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
                SET first_name = %s,
                    last_name  = %s,
                    email      = %s,
                    password   = %s,
                    rol        = %s,
                    active     = %s,
                    department = %s
                WHERE id = %s RETURNING id, first_name, last_name, email, password, rol, active, department; \
                """
        with self._db_manager.get_connection().cursor() as cursor:
            cursor.execute(query, (
                admin.first_name,
                admin.last_name,
                admin.email,
                admin.password,
                admin.role,
                admin.is_active,
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

    def email_exist(self, email: str) -> bool:
        """
        Verifica si un correo electrónico ya está registrado en la base de datos.
        :param email: Correo electrónico a verificar.
        :return: True si el correo existe, False en caso contrario.
        """
        query = "SELECT 1 FROM admins WHERE email = %s"
        with self._db_manager.get_connection().cursor() as cursor:
            cursor.execute(query, (email,))
            return cursor.fetchone() is not None

    def list_by_criteria(self, criteria: Optional[Dict[str, any]] = None, sort: str = "id") -> Optional[List[Admin]]:
        """
        Se obtiene una lista de administradores que cumplan con ciertos criterios de búsqueda.
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
    def _row_to_entity(db_result: tuple[any, ...]) -> Admin:
        """
        Convierte una fila de la base de datos en una instancia de Admin.
        :param db_result: Resultados obtenidos de la la consulta.
        :return: Instancia de Admin con los datos de la fila.
        """
        admin = Admin(
            first_name=db_result[1],
            last_name=db_result[2],
            email=db_result[3],
            password=db_result[4],
            department=db_result[7])
        admin.id = db_result[0]
        admin.role = UserRole(db_result[5])
        admin.is_active = db_result[6]
        return admin

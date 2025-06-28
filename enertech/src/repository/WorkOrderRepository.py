from typing import Optional, List, Dict
from enertech.src.database.DatabaseManager import DatabaseManager
from enertech.src.domain.WorkOrder import WorkOrder
from enertech.src.domain.MaintenanceType import MaintenanceType
from enertech.src.domain.PriorityLevel import PriorityLevel
from enertech.src.domain.TimeUnit import TimeUnit
from enertech.src.domain.Status import Status


# Repositorio para manejar operaciones de base de datos para órdenes de trabajo (WorkOrder)
class WorkOrderRepository:
    def __init__(self, db_manager: DatabaseManager):
        # Constructor que recibe un gestor de base de datos para manejar conexiones 
        self._db_manager = db_manager

    def save(self, order: WorkOrder) -> WorkOrder:
        # Inserta una nueva orden de trabajo en la base de datos y devuelve la entidad creada con el ID asignado
        query = """
                INSERT INTO WORK_ORDERS (title, assigned_to, created_by, asset_id, maintenance_type, priority, status,
                                         opened_at, estimated_time, estimated_time_unit, description)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s) 
                RETURNING id, title, assigned_to, created_by, asset_id, maintenance_type, priority, status, opened_at, 
                resolved_at, estimated_time, estimated_time_unit, resolved_on_time, description, closure_comments; \
                """
        # Abre cursor para ejecutar la consulta
        with self._db_manager.get_connection().cursor() as cursor:
            # Ejecuta la consulta con los valores del objeto order, usando el atributo value para los enums
            cursor.execute(query, (order.title, order.assigned_to, order.created_by, order.asset_id,
                                   order.maintenance_type.value, order.priority.value, order.status.value,
                                   order.opened_at, order.estimated_time,
                                   order.estimated_time_unit.value, order.description))
            # Confirma la transacción para guardar los cambios en la base de datos
            self._db_manager.commit_transaction()
            # Obtiene la fila retornada con los datos del registro insertado
            row = cursor.fetchone()
            # Cierra la conexión a la base de datos
            self._db_manager.close_connection()
            # Convierte la fila obtenida en un objeto WorkOrder y lo retorna
            return self._row_to_entity(row)

    def update(self, order: WorkOrder) -> Optional[WorkOrder]:
        # Actualiza una orden de trabajo existente en la base de datos y devuelve la entidad actualizada
        query = """
                UPDATE WORK_ORDERS
                SET title               = %s,
                    created_by          = %s,
                    asset_id            = %s,
                    maintenance_type    = %s,
                    priority            = %s,
                    estimated_time      = %s,
                    estimated_time_unit = %s,
                    description         = %s,
                    assigned_technician = %s,
                    opened_at           = %s,
                    resolved_at         = %s,
                    closure_comments    = %s,
                    status              = %s
                WHERE id = %s RETURNING id, title, created_by, asset_id, maintenance_type, priority,
                      estimated_time, estimated_time_unit, description,
                      assigned_technician, opened_at, resolved_at,
                      closure_comments, status; \
                """
        with self._db_manager.get_connection().cursor() as cursor:
            # Ejecuta la actualización con los valores del objeto order
            cursor.execute(query, (
                order.title,
                order.created_by,
                order.asset_id,
                order.maintenance_type.value,
                order.priority.value,
                order.estimated_time,
                order.estimated_time_unit.value,
                order.description,
                order.assigned_to,
                order.opened_at,
                order.resolved_at,
                order.closure_comments,
                order.status.value,
                order.id
            ))
            # Confirma la transacción
            self._db_manager.commit_transaction()
            # Obtiene la fila actualizada (si existe)
            row = cursor.fetchone()
            self._db_manager.close_connection()
            # Convierte la fila a objeto WorkOrder o retorna None si no se encontró el registro
            return self._row_to_entity(row) if row else None

    def get_by_id(self, order_id: int) -> Optional[WorkOrder]:
        # Busca y devuelve una orden de trabajo por su ID, o None si no existe
        query = "SELECT * FROM WORK_ORDERS WHERE id = %s"
        with self._db_manager.get_connection().cursor() as cursor:
            cursor.execute(query, (order_id,))
            row = cursor.fetchone()
            self._db_manager.close_connection()
            return self._row_to_entity(row) if row else None

    def list_by_criteria(self, filters: Optional[Dict[str, any]] = None, sort: str = "id") -> Optional[List[WorkOrder]]:
        # Lista las ordenes de trabajo que cumplan con ciertos criterios de búsqueda (filtros)
        query = "SELECT * FROM WORK_ORDERS"
        where_clauses = []
        params = []

        if filters:
            # Por cada criterio recibido, agrega un filtro con comparación parcial (ILIKE %valor%)
            for field, value in filters.items():
                if value is not None:
                    where_clauses.append(f"{field} ILIKE %s")
                    params.append(f"%{value}%")

        # Si hay filtros, los une con AND y los agrega al query
        if where_clauses:
            query += " WHERE " + " AND ".join(where_clauses)

        # Agrega la cláusula ORDER BY para ordenar los resultados
        query += f" ORDER BY {sort}"

        with self._db_manager.get_connection().cursor() as cursor:
            cursor.execute(query, params)
            rows = cursor.fetchall()
            self._db_manager.close_connection()
            # Convierte cada fila obtenida a objeto WorkOrder y retorna la lista
            return [self._row_to_entity(row) for row in rows] if rows else None

    def delete(self, order_id: int) -> None:
        # Elimina una orden de trabajo por ID
        query = "DELETE FROM WORK_ORDERS WHERE id = %s"
        with self._db_manager.get_connection().cursor() as cursor:
            cursor.execute(query, (order_id,))
            self._db_manager.commit_transaction()
            self._db_manager.close_connection()

    @staticmethod
    def _row_to_entity(row) -> WorkOrder:
        # Mapea una fila de la base de datos a un objeto WorkOrder
        order = WorkOrder(
            title=row[1],
            created_by=row[3],
            asset_id=row[4],
            maintenance_type=MaintenanceType(row[5]),
            priority=PriorityLevel(row[6]),
            estimated_time=row[10],
            estimated_time_unit=TimeUnit(row[11]),
            description=row[13],
            assigned_to=row[2]
        )
        order.id = row[0]
        order.opened_at = row[8]
        order.resolved_at = row[9]
        order.closure_comments = row[14]
        order.status = Status(row[7])
        return order

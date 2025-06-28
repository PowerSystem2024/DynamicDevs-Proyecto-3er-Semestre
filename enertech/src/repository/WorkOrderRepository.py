from typing import Optional, List, Dict
from src.database.DatabaseManager import DatabaseManager
from src.domain.WorkOrder import WorkOrder
from src.domain.MaintenanceType import MaintenanceType
from src.domain.PriorityLevel import PriorityLevel
from src.domain.TimeUnit import TimeUnit
from src.domain.Status import Status

# Repositorio para manejar operaciones de base de datos para órdenes de trabajo (WorkOrder)
class WorkOrderRepository:
    def __init__(self, db_manager: DatabaseManager):
        # Constructor que recibe un gestor de base de datos para manejar conexiones 
        self._db_manager = db_manager

    def save(self, order: WorkOrder) -> WorkOrder:
        # Inserta una nueva orden de trabajo en la base de datos y devuelve la entidad creada con el ID asignado
        query = """
            INSERT INTO WORK_ORDERS (
                title, created_by, asset_id, maintenance_type, priority,
                estimated_time, estimated_time_unit, description,
                assigned_technician, opened_at, status
            ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            RETURNING id, title, created_by, asset_id, maintenance_type, priority,
                      estimated_time, estimated_time_unit, description,
                      assigned_technician, opened_at, resolved_at,
                      closure_comments, status;
        """
        # Abre cursor para ejecutar la consulta
        with self._db_manager.get_connection().cursor() as cursor:
            # Ejecuta la consulta con los valores del objeto order, usando el atributo .value para los enums
            cursor.execute(query, (
                order.title,
                order.created_by,
                order.asset_id,
                order.maintenance_type.value,
                order.priority.value,
                order.estimated_time,
                order.estimated_time_unit.value,
                order.description,
                order.assigned_technician,
                order.opened_at,
                order.status.value
            ))
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
            SET title = %s, created_by = %s, asset_id = %s, maintenance_type = %s,
                priority = %s, estimated_time = %s, estimated_time_unit = %s,
                description = %s, assigned_technician = %s, opened_at = %s,
                resolved_at = %s, closure_comments = %s, status = %s
            WHERE id = %s
            RETURNING id, title, created_by, asset_id, maintenance_type, priority,
                      estimated_time, estimated_time_unit, description,
                      assigned_technician, opened_at, resolved_at,
                      closure_comments, status;
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
                order.assigned_technician,
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

    def list_by_criteria(self, criteria: Optional[Dict[str, any]] = None, sort: str = "id") -> Optional[List[WorkOrder]]:
        # Lista órdenes de trabajo que cumplan con ciertos criterios de búsqueda (filtros)
        query = "SELECT * FROM WORK_ORDERS"
        filters = []  
        params = []   

        if criteria:
            # Por cada criterio recibido, agrega un filtro con comparación parcial (ILIKE %valor%)
            for field, value in criteria.items():
                if value is not None:
                    filters.append(f"{field} ILIKE %s")
                    params.append(f"%{value}%")

        # Si hay filtros, los une con AND y los agrega al query
        if filters:
            query += " WHERE " + " AND ".join(filters)

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
        # Método auxiliar que convierte una fila de la BD a un objeto WorkOrder
        order = WorkOrder(
            title=row[1],
            created_by=row[2],
            asset_id=row[3],
            maintenance_type=MaintenanceType(row[4]),  # Convierte el valor entero a enum
            priority=PriorityLevel(row[5]),
            estimated_time=row[6],
            estimated_time_unit=TimeUnit(row[7]),
            description=row[8],
            assigned_technician=row[9]
        )
        order.id = row[0]
        order.opened_at = row[10]
        order.resolved_at = row[11]
        order.closure_comments = row[12]
        order.status = Status(row[13])
        return order

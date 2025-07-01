from datetime import datetime
from typing import Optional
from enertech.src.repository.WorkOrderRepository import WorkOrderRepository
from enertech.src.domain.WorkOrder import WorkOrder
from enertech.src.domain.WorkOrderData import WorkOrderData
from enertech.src.domain.Supervisor import Supervisor
from enertech.src.domain.Technician import Technician
from enertech.src.domain.IndustrialAsset import IndustrialAsset
from enertech.src.domain.MaintenanceType import MaintenanceType
from enertech.src.domain.PriorityLevel import PriorityLevel
from enertech.src.domain.Status import Status
from enertech.src.domain.TimeUnit import TimeUnit


# Definimos el atributo protegido y el constructor público con parámetro.
class WorkOrderService:
    def __init__(self, repository: WorkOrderRepository):
        self._repository = repository

    def create_work_order(self, order_data: WorkOrderData, supervisor: Supervisor, industrial_asset: IndustrialAsset) -> WorkOrder:
        for field_name in ['title', 'description']:
            value = getattr(order_data, field_name, None)
            if not isinstance(value, str):
                raise ValueError(f"{field_name} Debe ser texto")
            if not value.strip():
                raise ValueError(f"{field_name} No puede estar vacío ni solo con espacios")
            if len(value.strip()) < 2:
                raise ValueError(f"{field_name} Debe tener más de 1 carácter válido")

        if not isinstance(order_data.maintenance_type, MaintenanceType):
            raise ValueError("maintenance_type inválido")
        if not isinstance(order_data.priority, PriorityLevel):
            raise ValueError("priority inválido")
        if not isinstance(order_data.status, Status):
            raise ValueError("status inválido")
        if not isinstance(order_data.estimated_time, int) or order_data.estimated_time <= 0:
            raise ValueError("estimated_time debe ser un entero mayor que 0")
        if not isinstance(order_data.estimated_time_unit, TimeUnit):
            raise ValueError("estimated_time_unit inválido")
        if supervisor is None:
            raise ValueError("supervisor no puede ser nulo")

        order = WorkOrder(
            title=order_data.title.strip(),
            created_by=supervisor.id,
            asset_id=industrial_asset.id,
            maintenance_type=order_data.maintenance_type,
            priority=order_data.priority,
            estimated_time=order_data.estimated_time,
            estimated_time_unit=order_data.estimated_time_unit,
            description=order_data.description.strip()
        )

        order.assigned_to = None
        order.status = Status.UNASSIGNED
        order = self._repository.save(order)
        return order

    def get_work_order_by_id(self, work_order_id: int) -> WorkOrder:
        if not isinstance(work_order_id, int) or work_order_id <= 0:
            raise ValueError("work_order_id debe ser un número entero positivo")
        work_order = self._repository.get_by_id(work_order_id)
        if not work_order:
            raise ValueError(f"Orden de trabajo con ID {work_order_id} no encontrada")
        return work_order

    def assign_technician(self, work_order: WorkOrder, technician: Technician) -> WorkOrder:
        if not isinstance(work_order, WorkOrder) or work_order is None:
            raise TypeError("work_order debe ser una instancia de WorkOrder")
        if not isinstance(technician, Technician) or technician is None:
            raise TypeError("technician debe ser una instancia de Technician")
        orders_assigned_to_this_technician = self._repository.list_by_criteria(
            {'assigned_to': technician.id, 'status': Status.IN_PROGRESS})
        if len(orders_assigned_to_this_technician) >= technician.max_active_orders:
            raise ValueError("El técnico ya tiene el máximo de órdenes de trabajo activas")
        work_order.assigned_to = technician.id
        work_order.status = Status.IN_PROGRESS
        return self._repository.update(work_order)

    def resolve_order(self, order: WorkOrder, closure_coments: str) -> WorkOrder:
        order.closure_comments = closure_coments
        order.status = Status.RESOLVED
        order.resolved_at = datetime.now()
        return self._repository.update(order)

    def list_work_orders(self, criteria: Optional[dict] = None) -> list[WorkOrder]:
        if criteria is None:
            criteria = {}
        if not isinstance(criteria, dict):
            raise TypeError("criteria debe ser un diccionario")
        return self._repository.list_by_criteria(criteria)


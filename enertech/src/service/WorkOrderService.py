from datetime import datetime 
from enertech.src.repository.WorkOrderRepository import WorkOrderRepository # repositorio encargado de manejar las órdenes de trabajo.
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

    def create_work_order(self, order_data: WorkOrderData, supervisor: Supervisor, technician: Technician, industrial_asset: IndustrialAsset) -> WorkOrder:
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
            title = order_data.title.strip(),
            maintenance_type = order_data.maintenance_type,
            priority = order_data.priority,
            status = None,
            estimated_time = order_data.estimated_time,
            estimated_time_unit = order_data.estimated_time_unit,
            description = order_data.description.strip(),
            opened_at = datetime.now(),
            created_by = supervisor.id,
            industrial_asset = industrial_asset
        )

        if technician:
            order.assigned_to = technician.id
            order.status = Status.IN_PROGRESS
        else:
            order.assigned_to = None
            order.status = Status.UNASSIGNED

        self._repository.save(order)
        return order

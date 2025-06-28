# Importamos el repositorio encargado de manejar los datos de administradores
from enertech.src.repository.AdminRepository import AdminRepository

# Importamos los servicios que el administrador podrá utilizar
from enertech.src.service.TechnicianService import TechnicianService
from enertech.src.service.SupervisorService import SupervisorService
from enertech.src.service.IndustrialAssetService import IndustrialAssetService
from enertech.src.service.WorkOrderService import WorkOrderService


# Declaramos la clase AdminService, que representa el servicio para el rol de administrador
class AdminService:
    # El constructor recibe todos los servicios y repositorio que el admin necesita
    def __init__(
        self,
        repository: AdminRepository,
        technicianService: TechnicianService,
        supervisorService: SupervisorService,
        industrialAssetService: IndustrialAssetService,
        workOrderService: WorkOrderService
    ):
        # Guardamos el repositorio en un atributo privado
        self._repository = repository

        # Guardamos el servicio de técnicos
        self._technicianService = technicianService

        # Guardamos el servicio de supervisores
        self._supervisorService = supervisorService

        # Guardamos el servicio de activos industriales
        self._industrialAssetService = industrialAssetService

        # Guardamos el servicio de órdenes de trabajo
        self._workOrderService = workOrderService

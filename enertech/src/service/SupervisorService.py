# Importamos el repositorio que maneja los datos de los supervisores
from enertech.src.repository.SupervisorRepository import SupervisorRepository

# Importamos los servicios que el supervisor puede utilizar
from enertech.src.service.WorkOrderService import WorkOrderService
from enertech.src.service.TechnicianService import TechnicianService
from enertech.src.service.IndustrialAssetService import IndustrialAssetService


# Declaramos la clase SupervisorService, que representa el servicio del supervisor
class SupervisorService:
    # Constructor que recibe todas las dependencias que el supervisor usará
    def __init__(
        self,
        repository: SupervisorRepository,
        workOrderService: WorkOrderService,
        technicianService: TechnicianService,
        industrialAssetService: IndustrialAssetService
    ):
        # Guardamos el repositorio en un atributo privado
        self._repository = repository

        # Guardamos el servicio de órdenes de trabajo
        self._workOrderService = workOrderService

        # Guardamos el servicio de técnicos
        self._technicianService = technicianService

        # Guardamos el servicio de activos industriales
        self._industrialAssetService = industrialAssetService


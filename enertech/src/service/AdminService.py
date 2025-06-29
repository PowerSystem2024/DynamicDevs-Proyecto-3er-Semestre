# Importamos el repositorio encargado de manejar los datos de administradores
from enertech.src.domain.Admin import Admin
from enertech.src.domain.UserBaseData import UserBaseData
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
            technician_service: TechnicianService,
            supervisor_service: SupervisorService,
            industrial_asset_service: IndustrialAssetService,
            work_order_service: WorkOrderService
    ):
        self._repository = repository  # Guardamos el repositorio en un atributo privado
        self._technician_service = technician_service  # Guardamos el servicio de técnicos
        self._supervisor_service = supervisor_service  # Guardamos el servicio de supervisores
        self._industrial_asset_service = industrial_asset_service  # Guardamos el servicio de activos industriales
        self._work_order_service = work_order_service  # Guardamos el servicio de órdenes de trabajo

    def create_admin(self, user_data: UserBaseData, department: str) -> Admin:
        """
        Crea un nuevo administrador con los datos proporcionados.

        :param user_data: Datos del usuario base para el administrador.
        :param department: Departamento al que pertenece el administrador.
        :return: Instancia del administrador creado.
        """
        if not isinstance(department, str) or department.strip() == "" or department is None:
            raise ValueError("El departamento debe ser una cadena de texto")
        # Validamos que los datos del usuario sean correctos
        if not isinstance(user_data, UserBaseData):
            raise ValueError("user_data debe ser una instancia de UserBaseData")

        # Creamos una nueva instancia de Admin con los datos proporcionados
        admin = Admin(
            first_name=user_data.first_name,
            last_name=user_data.last_name,
            email=user_data.email,
            password=user_data.password,
            department=department
        )
        # Guardamos el administrador en el repositorio
        return self._repository.save(admin)

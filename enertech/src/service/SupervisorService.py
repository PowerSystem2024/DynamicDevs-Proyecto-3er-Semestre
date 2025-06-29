# Importamos el repositorio que maneja los datos de los supervisores
from enertech.src.domain.Supervisor import Supervisor
from enertech.src.domain.UserBaseData import UserBaseData
from enertech.src.repository.SupervisorRepository import SupervisorRepository

# Importamos los servicios que el supervisor puede utilizar
from enertech.src.service.WorkOrderService import WorkOrderService
from enertech.src.service.TechnicianService import TechnicianService
from enertech.src.service.IndustrialAssetService import IndustrialAssetService


# Declaramos la clase SupervisorService, que representa el servicio del supervisor
class SupervisorService:
    # Constructor que recibe todas las dependencias que el supervisor usará
    def __init__(self, repository: SupervisorRepository, work_order_service: WorkOrderService,
                 technician_service: TechnicianService, industrial_asset_service: IndustrialAssetService):
        self._repository = repository  # Guardamos el repositorio en un atributo privado
        self._work_order_service = work_order_service  # Guardamos el servicio de órdenes de trabajo
        self._technician_service = technician_service  # Guardamos el servicio de técnicos
        self._industrial_asset_service = industrial_asset_service  # Guardamos el servicio de activos industriales

    def create_supervisor(self, base_data: UserBaseData, assigned_area: str) -> Supervisor:
        self._validate_type(base_data, assigned_area)
        self._validate_content(base_data, assigned_area)
        if self._repository.email_exist(base_data.email):
            raise ValueError("El email ya existe en la base de datos")
        # Creación del supervisor
        supervisor = Supervisor(first_name=base_data.first_name, last_name=base_data.last_name,
                                email=base_data.email, password=base_data.password, assigned_area=assigned_area)
        # Persistencia y retorno
        return self._repository.save(supervisor)

    @staticmethod
    def _validate_type(base_data: UserBaseData, assigned_area: str):
        if not isinstance(base_data.first_name, str):
            raise TypeError("first_name debe ser una cadena de texto")
        if not isinstance(base_data.last_name, str):
            raise TypeError("last_name debe ser una cadena de texto")
        if not isinstance(base_data.email, str):
            raise TypeError("email debe ser una cadena de texto")
        if not isinstance(base_data.password, str):
            raise TypeError("password debe ser una cadena de texto")
        if not isinstance(assigned_area, str):
            raise TypeError("assigned_area debe ser una cadena de texto")

    def _validate_content(self, base_data: UserBaseData, assigned_area: str):
        self._validate_string_field("first_name", base_data.first_name)
        self._validate_string_field("last_name", base_data.last_name)
        self._validate_string_field("email", base_data.email)
        self._validate_string_field("password", base_data.password, min_length=8)
        self._validate_string_field("assigned_area", assigned_area)

    @staticmethod
    def _validate_string_field(field_name: str, value: str, min_length: int = 2):
        if not value or value.strip() == "":
            raise ValueError(f"{field_name} no puede estar vacío")
        if len(value.strip()) < min_length:
            raise ValueError(f"{field_name} debe tener al menos {min_length} caracteres")
        if not any(char.isalpha() for char in value):
            raise ValueError(f"{field_name} debe contener al menos una letra")
        # Aquí podrían añadirse validaciones específicas para el área

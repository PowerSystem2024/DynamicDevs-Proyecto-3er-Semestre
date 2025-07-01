# Importamos el repositorio que maneja los datos de los supervisores
from enertech.src.domain.Supervisor import Supervisor
from enertech.src.domain.UserBaseData import UserBaseData
from enertech.src.domain.WorkOrder import WorkOrder
from enertech.src.domain.WorkOrderData import WorkOrderData
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

    def update_supervisor_details(self, supervisor_id: int, base_data: UserBaseData, assigned_area: str) -> Supervisor:
        self._validate_type(base_data, assigned_area)
        self._validate_content(base_data, assigned_area)
        # Verificamos si el supervisor existe
        supervisor = self.get_supervisor_by_id(supervisor_id)
        # Actualizamos los datos del supervisor
        if base_data.first_name and base_data.last_name not in (None, ""):
            supervisor.first_name = base_data.first_name
        if base_data.last_name and base_data.last_name not in (None, ""):
            supervisor.last_name = base_data.last_name
        if base_data.email and base_data.email not in (None, ""):
            if self._repository.email_exist(base_data.email):
                raise ValueError("El email ya existe en la base de datos")
            supervisor.email = base_data.email
        if base_data.password and base_data.password not in (None, ""):
            supervisor.password = base_data.password
        if assigned_area and assigned_area not in (None, ""):
            supervisor.assigned_area = assigned_area
        # Guardamos los cambios y retornamos el supervisor actualizado
        return self._repository.update(supervisor)

    def initiate_work_order(self, order_data: WorkOrderData, asset_id: int, supervisor_id: int) -> WorkOrder:
        asset = self._industrial_asset_service.get_asset_by_id(asset_id)
        supervisor = self.get_supervisor_by_id(supervisor_id)
        # Guardamos la orden de trabajo y retornamos
        return self._work_order_service.create_work_order(order_data, supervisor, asset)

    def assign_work_order(self, tehcnician_id: int, work_order_id: int) -> WorkOrder:
        technician = self._technician_service.get_technician_by_id(tehcnician_id)
        work_order = self._work_order_service.get_work_order_by_id(work_order_id)
        return self._work_order_service.assign_technician(work_order, technician)

    def get_supervisor_by_id(self, supervisor_id: int) -> Supervisor:
        if not isinstance(supervisor_id, int) or supervisor_id <= 0:
            raise ValueError("El ID del supervisor debe ser un número entero positivo")
        # Obtenemos el supervisor por su ID
        supervisor = self._repository.get_by_id(supervisor_id)
        if not supervisor:
            raise ValueError(f"Supervisor con {supervisor_id} no encontrado")
        return supervisor

    def exist_supervisor_by_credentials(self, email: str, password: str):
        if not isinstance(email, str) or not isinstance(password, str):
            raise TypeError("El email y la contraseña deben ser cadenas de texto")
        if not self._repository.exists_by_credentials(email, password):
            raise PermissionError("Credenciales incorrectas, vuelva a intentarlo.")

    def get_supervisor_by_email(self, email: str) -> Supervisor:
        if not isinstance(email, str) or email.strip() == "" or "@" not in email:
            raise TypeError("Email inválido")
        supervisor = self._repository.get_by_email(email)
        if not supervisor:
            raise ValueError(f"Supervisor con email {email} no encontrado")
        return supervisor

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

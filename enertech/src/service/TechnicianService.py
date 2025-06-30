from enertech.src.domain.Technician import Technician
from enertech.src.domain.UserBaseData import UserBaseData
from enertech.src.repository.TechnicianRepository import TechnicianRepository
from enertech.src.service.WorkOrderService import WorkOrderService


class TechnicianService:
    def _init_(self, repository: TechnicianRepository, work_order_service: WorkOrderService):
        self._repository = repository
        self._work_order_service = work_order_service

    def create_technician(self, base_data: UserBaseData, max_active_orders: int) -> Technician:
        self._validate_type(base_data, max_active_orders)
        self._validate_content(base_data, max_active_orders)
        if self._repository.email_exist(base_data.email):
            raise ValueError("El email ya existe en la base de datos")
        technician = Technician(first_name=base_data.first_name, last_name=base_data.last_name,
                                email=base_data.email, password=base_data.password,
                                max_active_orders=max_active_orders)
        return self._repository.save(technician)

    def get_technician_by_id(self, technician_id: int) -> Technician:
        if not isinstance(technician_id, int) or technician_id < 0:
            raise TypeError("technician_id debe ser un entero positivo")
        technician = self._repository.get_by_id(technician_id)
        if not technician:
            raise ValueError(f"Técnico con ID {technician_id} no encontrado")
        return technician

    @staticmethod
    def _validate_type(base_data: UserBaseData, max_active_orders: int):
        if not isinstance(base_data.first_name, str):
            raise TypeError("first_name debe ser una cadena de texto")
        if not isinstance(base_data.last_name, str):
            raise TypeError("last_name debe ser una cadena de texto")
        if not isinstance(base_data.email, str):
            raise TypeError("email debe ser una cadena de texto")
        if not isinstance(base_data.password, str):
            raise TypeError("password debe ser una cadena de texto")
        if not isinstance(max_active_orders, int):
            raise TypeError("max_active_orders debe ser un entero")

    def _validate_content(self, base_data: UserBaseData, max_active_orders: int):
        self._validate_string_field("first_name", base_data.first_name)
        self._validate_string_field("last_name", base_data.last_name)
        self._validate_string_field("email", base_data.email)
        self._validate_string_field("password", base_data.password, min_length=8)
        if not (2 <= max_active_orders <= 6):
            raise ValueError("max_active_orders debe estar entre 2 y 6")

    @staticmethod
    def _validate_string_field(field_name: str, value: str, min_length: int = 2):
        if not value or value.strip() == "":
            raise ValueError(f"{field_name} no puede estar vacío")
        if len(value.strip()) < min_length:
            raise ValueError(f"{field_name} debe tener al menos {min_length} caracteres")
        if not any(char.isalpha() for char in value):
            raise ValueError(f"{field_name} debe contener al menos una letra")

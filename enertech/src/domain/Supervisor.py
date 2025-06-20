# Importa el enum que representa los roles del usuario
from src.domain.UserRole import UserRole
# Importa la clase User
from src.domain.User import User


# La clase Supervisor hereda de la clase User y representa a un usuario con rol de supervisor
class Supervisor(User):
    def __init__(self, first_name: str, last_name: str, email: str, password: str, assigned_area: str):
        # Llama al constructor de la clase padre User
        super().__init__(first_name, last_name, email, password)
        # Atributos específicos de la clase Supervisor
        self._assigned_area = assigned_area  # Área donde el supervisor fue asignado

    @property
    def role(self) -> UserRole:
        return self._role

    def _determine_role(self):
        self._role = UserRole.SUPERVISOR  # Establece el rol del usuario como SUPERVISOR

    # Getter para el área asignada
    @property
    def assigned_area(self) -> str:
        return self._assigned_area

    # Setter para modificar el área asignada, validando que sea una cadena
    @assigned_area.setter
    def assigned_area(self, value: str):
        if not isinstance(value, str):
            raise TypeError("El área asignada debe ser una cadena de texto.")
        self._assigned_area = value

    # Devuelve una representación como string del objeto Supervisor
    def __str__(self):
        return f"Supervisor(id={self.id}, name={self.first_name} {self.last_name}, area_asignada={self.assigned_area})"

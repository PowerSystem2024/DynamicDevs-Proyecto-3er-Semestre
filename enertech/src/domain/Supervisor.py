# Importa el enum que representa los roles del usuario
from domain.UserRole import UserRole
# Importa la clase User
from domain.User import User

# La clase Supervisor hereda de la clase User y representa a un usuario con rol de supervisor
class Supervisor(User):
    def __init__(self, first_name: str, last_name: str, email: str, password: str, role: UserRole, area_asignada: str):
        # Llama al constructor de la clase padre User
        super().__init__(first_name, last_name, email, password)

        # Atributos específicos de la clase Supervisor
        self._role = role                  # Rol del usuario (debe ser UserRole.SUPERVISOR)
        self._area_asignada = area_asignada  # Área donde el supervisor fue asignado

    @property
    def role(self) -> UserRole:
        return self._role

    def _determine_role(self) -> UserRole:
        return self._role

    # Getter para el área asignada
    @property
    def area_asignada(self) -> str:
        return self._area_asignada

    # Setter para modificar el área asignada, validando que sea una cadena
    @area_asignada.setter
    def area_asignada(self, value: str):
        if not isinstance(value, str):
            raise ValueError("El área asignada debe ser una cadena de texto.")
        self._area_asignada = value

    def cambiar_area(self, nueva_area: str):
        self.area_asignada = nueva_area

    # Devuelve una representación como string del objeto Supervisor

    def __str__(self):
        return f"Supervisor(id={self.id}, name={self.first_name} {self.last_name}, area_asignada={self.area_asignada})"

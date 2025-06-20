# Importa el enum que representa los roles del usuario
from src.domain.UserRole import UserRole
# Importa la clase User
from src.domain.User import User


# La clase Admin hereda de la clase User y representa a un usuario administrador 
class Admin(User):
    def __init__(self, first_name: str, last_name: str, email: str, password: str, department: str):
        # Llama al constructor de la clase padre User 
        super().__init__(first_name, last_name, email, password)
        # Atributos de la clase Admin
        self._department = department  # Departamento al que pertenece el administrador

    @property
    def role(self) -> UserRole:
        return self._role

    def _determine_role(self):
        self._role = UserRole.ADMIN  # Establece el rol del usuario como ADMIN

    # Propiedad para obtener el departamento del administrador
    @property
    def department(self) -> str:
        return self._department

    # Setter para modificar el departamento, validando que sea una cadena
    @department.setter
    def department(self, value: str):
        if not isinstance(value, str):
            raise ValueError("El departamento debe ser una cadena de texto")
        self._department = value

    # Devuelve una representación como string del objeto Admin
    def __str__(self):
        return f"Admin(id={self.id}, name={self.first_name} {self.last_name}, role={self.role.value}, department={self.department})"

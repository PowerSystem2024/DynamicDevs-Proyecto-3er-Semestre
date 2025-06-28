# Importa el enum que representa los roles del usuario
from enertech.src.domain.UserRole import UserRole
# Importa la clase User
from enertech.src.domain.User import User


# La clase Technician hereda de la clase User y representa a un técnico en la aplicación
class Technician(User):
    def __init__(self, first_name: str, last_name: str, email: str, password: str, max_active_orders: int):
        # Llama al constructor de la clase padre User
        super().__init__(first_name, last_name, email, password)
        # Atributos propios de la clase Technician
        self._max_active_orders = max_active_orders  # Máximo de órdenes activas que puede tener asignadas

    # Implementación del metodo abstracto
    @property
    def role(self) -> UserRole:
        return self._role

    # Metodo privado que determina el rol del usuario
    def _determine_role(self):
        self._role = UserRole.TECHNICIAN  # Establece el rol del usuario como TECHNICIAN

    # Propiedad para obtener el máximo de órdenes activas
    @property
    def max_active_orders(self) -> int:
        return self._max_active_orders

    # Setter para definir un nuevo límite de órdenes activas (debe ser un número entero positivo)
    @max_active_orders.setter
    def max_active_orders(self, value: int):
        if not isinstance(value, int) or value < 0:
            raise ValueError("El número máximo de órdenes activas debe ser un entero positivo.")
        self._max_active_orders = value

    # Devuelve una representación como string del objeto Technician
    def __str__(self):
        return f"Technician(id={self.id}, name={self.first_name} {self.last_name}, max_orders={self.max_active_orders}, active_orders={len(self.assigned_orders)})"

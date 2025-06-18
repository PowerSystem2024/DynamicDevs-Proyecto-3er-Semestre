# Importa el enum que representa los roles del usuario
from domain.UserRole import UserRole
# Importa la clase User
from domain.User import User

# La clase Technician hereda de la clase User y representa a un técnico en la aplicación
class Technician(User):
    def __init__(self, first_name: str, last_name: str, email: str, password: str, role: UserRole, max_active_orders: int):
        # Llama al constructor de la clase padre User
        super().__init__(first_name, last_name, email, password)
        
        # Atributos propios de la clase Technician
        self._role = role                          
        self._max_active_orders = max_active_orders  # Máximo de órdenes activas que puede tener asignadas
        self._assigned_orders = []                 # Lista de órdenes actualmente asignadas

    # Implementación del método abstracto role
    @property
    def role(self) -> UserRole:
        return self._role

    # Método privado que determina el rol del usuario
    def _determine_role(self) -> UserRole:
        return self._role

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

    # Propiedad para obtener las órdenes actualmente asignadas al técnico
    @property
    def assigned_orders(self) -> list:
        return self._assigned_orders

    # Método para asignar una nueva orden al técnico
    def assign_order(self, order):
        if len(self._assigned_orders) >= self._max_active_orders:
            raise Exception("El técnico alcanzo el máximo de órdenes activas permitidas.")
        self._assigned_orders.append(order)

    # Método para finalizar una orden 
    def complete_order(self, order):
        if order in self._assigned_orders:
            self._assigned_orders.remove(order)

    # Devuelve una representación como string del objeto Technician
    def __str__(self):
        return f"Technician(id={self.id}, name={self.first_name} {self.last_name}, max_orders={self.max_active_orders}, active_orders={len(self.assigned_orders)})"

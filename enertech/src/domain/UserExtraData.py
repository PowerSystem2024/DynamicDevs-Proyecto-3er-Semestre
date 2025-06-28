class UserExtraData:
    def __init__(self, max_active_orders: int, assigned_area: str, department: str):
        """
        Constructor de la clase UserExtraData
            Atributos:
            max_active_orders (int): Número máximo de pedidos activos
            assigned_area (str): Área asignada al usuario
            department (str): Departamento al que pertenece el usuario
        """
        self._max_active_orders = max_active_orders
        self._assigned_area = assigned_area
        self._department = department
    #Getters
    @property
    def max_active_orders(self) -> int:
        return self._max_active_orders

    @property
    def assigned_area(self) -> str:
        return self._assigned_area

    @property
    def department(self) -> str:
        return self._department

    def __str__(self) -> str:
        """String del objeto"""
        return (f"UserExtraData [max_active_orders={self._max_active_orders}, "
                f"assigned_area='{self._assigned_area}', department='{self._department}']")
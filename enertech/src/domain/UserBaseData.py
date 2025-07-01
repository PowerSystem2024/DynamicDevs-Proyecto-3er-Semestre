class UserBaseData:
    """
    Clase que engloba los atributos comunes para Admin, Supervisor y Technician.
    Proporciona acceso de solo lectura (getters) a los datos básicos del usuario.
    No incluye setters ya que no son necesarios según los requerimientos.
    """
    
    def __init__(self, first_name: str, last_name: str, email: str, password: str):
        """Constructor de la clase UserBaseData."""
        self._first_name = first_name
        self._last_name = last_name
        self._email = email
        self._password = password
    
    @property
    def first_name(self) -> str:
        """Devuelve el nombre del usuario"""
        return self._first_name
    
    @property
    def last_name(self) -> str:
        """Devuelve el apellido del usuario"""
        return self._last_name
    
    @property
    def email(self) -> str:
        """Devuelve el email del usuario"""
        return self._email
    
    @property
    def password(self) -> str:
        """Devuelve la contraseña del usuario"""
        return self._password
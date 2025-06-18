# Importa el enum que representa los roles del usuario
from domain.UserRole import UserRole
# Importa la clase User
from domain.User import User 

# La clase Admin hereda de la clase User y representa a un usuario administrador 
class Admin(User):
    def __init__(self, first_name: str, last_name: str, email: str, password: str, role: UserRole, department: str):
        # Llama al constructor de la clase padre User 
        super().__init__(first_name, last_name, email, password)

        # Atributos de la clase Admin
        self._comment = ""                   
        self._registered_assets = []        
        self._role = role                   # Rol del usuario, definido por el enum UserRole
        self._department = department       # Departamento al que pertenece el administrador

    @property
    def role(self) -> UserRole:
        return self._role

    def _determine_role(self) -> UserRole:
        return self._role

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

    # Propiedad para obtener el comentario
    @property
    def comment(self) -> str:
        return self._comment

    # Setter para modificar el comentario, validando que sea una cadena
    @comment.setter
    def comment(self, value: str):
        if not isinstance(value, str):
            raise ValueError("El comentario debe ser una cadena de texto")
        self._comment = value

    @property
    def registered_assets(self) -> list:
        return self._registered_assets

    def getDepartment(self) -> str:
        return self.department

    def changeDepartment(self, newDepartment: str):
        self.department = newDepartment

    def getRegisteredAssets(self) -> list:
        return self.registered_assets

    def registerAsset(self, industrialAsset):
        if industrialAsset not in self._registered_assets:
            self._registered_assets.append(industrialAsset)

    def registerSupervisor(self, supervisor):
        pass  

    def registerTechnician(self, technician):
        pass  

    def deactivateUser(self, user):
        pass  

    # Devuelve una representación en cadena del objeto Admin
    def __str__(self):
        return f"Admin(id={self.id}, name={self.first_name} {self.last_name}, role={self.role.value}, department={self.department})"

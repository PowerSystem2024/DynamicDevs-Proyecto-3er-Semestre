from enum import Enum

class MaintenanceType(Enum):
    """
    Enumerador que define el tipo de mantenimiento para una orden de trabajo.
    Valores:
    - PREVENTIVE: Mantenimiento preventivo (revisión programada).
    - CORRECTIVE: Mantenimiento correctivo (reparación por falla).
    """
    PREVENTIVE = 1
    CORRECTIVE = 2

    def __str__(self):
        """Devuelve el nombre del tipo en formato legible."""
        return self.name.capitalize()
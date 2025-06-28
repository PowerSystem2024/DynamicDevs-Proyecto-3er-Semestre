from enum import Enum


class MaintenanceType(Enum):
    """
    Enumerador que define el tipo de mantenimiento para una orden de trabajo.
    Valores:
    - PREVENTIVE: Mantenimiento preventivo (revisión programada).
    - CORRECTIVE: Mantenimiento correctivo (reparación por falla).
    """
    PREVENTIVE = 'PREVENTIVE'
    CORRECTIVE = 'CORRECTIVE'

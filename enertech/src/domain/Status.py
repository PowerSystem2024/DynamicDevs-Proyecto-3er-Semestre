from enum import Enum

class Status(Enum):
    """
    Enumerador que representa los estados posibles de una orden de trabajo.
    Valores:
    - UNASSIGNED: Orden creada pero sin asignar a técnico.
    - IN_PROGRESS: Orden asignada y en proceso de reparación.
    - RESOLVED: Orden completada con éxito.
    - REOPENED: Orden reabierta tras haberse resuelto.
    - WAITING_PARTS: Esperando repuestos para continuar.
    - CANCELLED: Orden cancelada antes de completarse.
    - ON_HOLD: Pausada temporalmente por algún motivo.
    """
    UNASSIGNED = 1
    IN_PROGRESS = 2
    RESOLVED = 3
    REOPENED = 4
    WAITING_PARTS = 5
    CANCELLED = 6
    ON_HOLD = 7

    def __str__(self):
        """Devuelve el nombre del estado en formato legible."""
        return self.name.replace("_", " ").title()
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
    UNASSIGNED = 'UNASSIGNED'
    IN_PROGRESS = 'IN_PROGRESS'
    RESOLVED = 'RESOLVED'
    REOPENED = 'REOPENED'
    WAITING_PARTS = 'WAITING_PARTS'
    CANCELLED = 'CANCELLED'
    ON_HOLD = 'ON_HOLD'

from enum import Enum


class PriorityLevel(Enum):
    """
    Enumerador que clasifica el nivel de prioridad de una orden de trabajo.
    Valores posibles:
    - CRITICO: Prioridad máxima (atención inmediata).
    - URGENTE: Muy alta, resolver dentro de las próximas horas.
    - ALTO: Importante, pero puede esperar un día.
    - MEDIO: Prioridad estándar.
    - BAJO: Baja urgencia (puede postergarse).
    """
    CRITICAL = 'CRITICAL'
    URGENT = 'URGENT'
    HIGH = 'HIGH'
    MEDIUM = 'MEDIUM'
    LOW = 'LOW'

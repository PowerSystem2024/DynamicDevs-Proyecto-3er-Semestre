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
    CRITICAL = 5
    URGENT = 4
    HIGH = 3
    MEDIUM = 2
    LOW = 1

    def __str__(self):
        """Representación legible del nivel de prioridad."""
        return self.name.capitalize()
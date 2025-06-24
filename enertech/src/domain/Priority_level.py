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
    CRITICO = 5
    URGENTE = 4
    ALTO = 3
    MEDIO = 2
    BAJO = 1

    def __str__(self):
        """Representación legible del nivel de prioridad."""
        return self.name.capitalize()
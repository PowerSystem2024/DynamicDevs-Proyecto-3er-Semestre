from enum import Enum


class TimeUnit(Enum):
    """
    Enumerador que representa las unidades de tiempo disponibles para estimar
    la duración de las órdenes de trabajo. (Horas, Días, Semanas)
    Este enum es utilizado por los supervisores
    """
    HOURS = "HOURS"
    DAYS = "DAYS"
    WEEKS = "WEEKS"

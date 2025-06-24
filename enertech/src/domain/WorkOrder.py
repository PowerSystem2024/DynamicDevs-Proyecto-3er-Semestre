from datetime import datetime, timedelta
from typing import Optional

from src.domain.MaintenanceType import MaintenanceType
from src.domain.PriorityLevel import PriorityLevel
from src.domain.Status import Status
from src.domain.TimeUnit import TimeUnit


class WorkOrder:
    """
    Clase que representa una orden de trabajo en el sistema EnerTech.

    Una orden de trabajo debe tener:
      - título
      - técnico asignado (opcional)
      - ID del supervisor que la crea (campo 'created_by')
      - activo asignado (campo 'asset_id')
      - tipo de mantenimiento (enum MaintenanceType)
      - nivel de prioridad (enum PriorityLevel)
      - tiempo estimado en valor entero (campo 'estimated_time')
      - tipo de unidad de tiempo (enum TimeUnit)
      - descripción
      - fecha de creación (asignada automáticamente)
      - estado actual (asignado según la presencia o ausencia de un técnico)
    """

    def __init__(
            self,
            title: str,
            created_by: int,  # ID del supervisor que crea la orden (obligatorio)
            asset_id: int,  # ID del activo asignado (obligatorio)
            maintenance_type: MaintenanceType,  # Tipo de mantenimiento (Preventive, Corrective, etc.)
            priority: PriorityLevel,  # Nivel de prioridad (Critical, High, Medium, Low)
            estimated_time: int,  # Tiempo estimado en valor entero para completar la orden
            estimated_time_unit: TimeUnit,  # Unidad de tiempo (hora, día, semana)
            description: str,  # Descripción detallada de la orden de trabajo
            assigned_technician: Optional[int] = None  # ID del técnico asignado (opcional)
    ):
        # Inicialización de los atributos básicos
        self._title = title
        self._created_by = created_by
        self._asset_id = asset_id
        self._maintenance_type = maintenance_type
        self._priority = priority
        self._estimated_time = estimated_time
        self._estimated_time_unit = estimated_time_unit
        self._description = description
        self._assigned_technician = assigned_technician

        # Se asigna la fecha de creación automáticamente al momento de instanciar
        self._opened_at = datetime.now()
        # Los siguientes atributos se establecerán cuando la orden sea resuelta
        self._resolved_at: Optional[datetime] = None
        self._closure_comments: Optional[str] = None

        # Determinación del estado inicial según la asignación del técnico:
        #   - Si assigned_technician es None => Estado UNASSIGNED.
        #   - Si assigned_technician tiene un ID => Estado IN_PROGRESS.
        if assigned_technician is None:
            self._status = Status.UNASSIGNED
        else:
            self._status = Status.IN_PROGRESS

    # ============================================================
    # Propiedades (getters y setters) para cada atributo de la clase
    # ============================================================

    @property
    def title(self) -> str:
        """ Obtiene el título de la orden de trabajo. """
        return self._title

    @title.setter
    def title(self, value: str):
        """ Establece el título de la orden de trabajo. """
        self._title = value

    @property
    def created_by(self) -> int:
        """ Obtiene el ID del supervisor que creó la orden. """
        return self._created_by

    @created_by.setter
    def created_by(self, value: int):
        """ Establece el ID del supervisor que creó la orden. """
        self._created_by = value

    @property
    def asset_id(self) -> int:
        """ Obtiene el ID del activo asignado a la orden. """
        return self._asset_id

    @asset_id.setter
    def asset_id(self, value: int):
        """ Establece el ID del activo asignado. """
        self._asset_id = value

    @property
    def maintenance_type(self) -> MaintenanceType:
        """ Obtiene el tipo de mantenimiento de la orden. """
        return self._maintenance_type

    @maintenance_type.setter
    def maintenance_type(self, value: MaintenanceType):
        """ Establece el tipo de mantenimiento. """
        self._maintenance_type = value

    @property
    def priority(self) -> PriorityLevel:
        """ Obtiene el nivel de prioridad de la orden. """
        return self._priority

    @priority.setter
    def priority(self, value: PriorityLevel):
        """ Establece el nivel de prioridad de la orden. """
        self._priority = value

    @property
    def estimated_time(self) -> int:
        """ Obtiene el tiempo estimado (un valor entero) para completar la orden. """
        return self._estimated_time

    @estimated_time.setter
    def estimated_time(self, value: int):
        """ Establece el tiempo estimado para completar la orden. """
        self._estimated_time = value

    @property
    def estimated_time_unit(self) -> TimeUnit:
        """ Obtiene la unidad de tiempo utilizada en la estimación. """
        return self._estimated_time_unit

    @estimated_time_unit.setter
    def estimated_time_unit(self, value: TimeUnit):
        """ Establece la unidad de tiempo para la estimación. """
        self._estimated_time_unit = value

    @property
    def description(self) -> str:
        """ Obtiene la descripción de la orden de trabajo. """
        return self._description

    @description.setter
    def description(self, value: str):
        """ Establece la descripción de la orden de trabajo. """
        self._description = value

    @property
    def assigned_technician(self) -> Optional[int]:
        """ Obtiene el ID del técnico asignado (puede ser None si aún no se asigna). """
        return self._assigned_technician

    @assigned_technician.setter
    def assigned_technician(self, value: Optional[int]):
        """
        Establece el ID del técnico asignado.
        Además, actualiza el estado de la orden:
          - Si se elimina el técnico (value es None), el estado pasa a UNASSIGNED.
          - Si se asigna un técnico, el estado pasa a IN_PROGRESS.
        """
        self._assigned_technician = value
        if value is None:
            self._status = Status.UNASSIGNED
        else:
            self._status = Status.IN_PROGRESS

    @property
    def opened_at(self) -> datetime:
        """ Obtiene la fecha y hora en que se abrió la orden. """
        return self._opened_at

    @property
    def resolved_at(self) -> Optional[datetime]:
        """ Obtiene la fecha y hora en que se resolvió la orden (None si aún no está resuelta). """
        return self._resolved_at

    @resolved_at.setter
    def resolved_at(self, value: datetime):
        """ Establece la fecha y hora en que se resolvió la orden. """
        self._resolved_at = value

    @property
    def closure_comments(self) -> Optional[str]:
        """ Obtiene los comentarios de cierre de la orden (puede ser None). """
        return self._closure_comments

    @closure_comments.setter
    def closure_comments(self, value: str):
        """ Establece los comentarios de cierre de la orden. """
        self._closure_comments = value

    @property
    def status(self) -> Status:
        """ Obtiene el estado actual de la orden (por ejemplo, UNASSIGNED o IN_PROGRESS). """
        return self._status

    @status.setter
    def status(self, value: Status):
        """ Establece el estado actual de la orden. """
        self._status = value

    # ===============================================================
    # Métodos auxiliares para la lógica de negocio de la orden
    # ===============================================================

    def get_remaining_time(self) -> timedelta:
        """
        Calcula el tiempo restante para completar la orden basado en:
          - La fecha de apertura (opened_at)
          - El tiempo estimado y su unidad.

        Retorna un objeto timedelta que puede ser negativo si se ha excedido el tiempo estimado.
        """
        # Determinar el delta en función de la unidad de tiempo
        if self._estimated_time_unit == TimeUnit.HOURS:
            delta = timedelta(hours=self._estimated_time)
        elif self._estimated_time_unit == TimeUnit.DAYS:
            delta = timedelta(days=self._estimated_time)
        elif self._estimated_time_unit == TimeUnit.WEEKS:
            delta = timedelta(weeks=self._estimated_time)
        else:
            delta = timedelta()

        deadline = self._opened_at + delta  # Fecha límite para completar la orden
        return deadline - datetime.now()  # Tiempo restante (puede ser negativo)

    def was_resolved_on_time(self) -> Optional[bool]:
        """
        Determina si la orden de trabajo fue resuelta a tiempo, comparando:
          - La fecha en que se resolvió la orden (resolved_at)
          - La fecha límite calculada a partir del tiempo estimado.

        Retorna:
          - True si la orden se resolvió en o antes de la fecha límite.
          - False si se resolvió después.
          - None si aun no se ha resuelto (resolved_at es None).
        """
        if self._resolved_at is None:
            return None

        if self._estimated_time_unit == TimeUnit.HOURS:
            delta = timedelta(hours=self._estimated_time)
        elif self._estimated_time_unit == TimeUnit.DAYS:
            delta = timedelta(days=self._estimated_time)
        elif self._estimated_time_unit == TimeUnit.WEEKS:
            delta = timedelta(weeks=self._estimated_time)
        else:
            delta = timedelta()

        deadline = self._opened_at + delta
        return self._resolved_at <= deadline

    def __str__(self) -> str:
        """
        Representación en forma de cadena de la orden de trabajo,
        mostrando los campos más relevantes.
        """
        return (
            f"WorkOrder(title={self._title}, created_by={self._created_by}, asset_id={self._asset_id}, "
            f"maintenance_type={self._maintenance_type.value}, priority={self._priority.value}, "
            f"estimated_time={self._estimated_time} {self._estimated_time_unit.value}, "
            f"description={self._description}, assigned_technician={self._assigned_technician}, "
            f"opened_at={self._opened_at}, status={self._status.value})"
        )

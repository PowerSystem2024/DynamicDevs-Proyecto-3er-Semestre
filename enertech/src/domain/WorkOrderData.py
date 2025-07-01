from enertech.src.domain.MaintenanceType import MaintenanceType
from enertech.src.domain.PriorityLevel import PriorityLevel
from enertech.src.domain.Status import Status
from enertech.src.domain.TimeUnit import TimeUnit


class WorkOrderData:
    def __init__(
        self,
        title: str,
        maintenance_type: MaintenanceType,
        priority: PriorityLevel,
        status: Status,
        estimated_time: int,
        estimated_time_unit: TimeUnit,
        description: str
    ):
        self._title = title
        self._maintenance_type = maintenance_type
        self._priority = priority
        self._status = status
        self._estimated_time = estimated_time
        self._estimated_time_unit = estimated_time_unit
        self._description = description

    @property
    def title(self) -> str:
        return self._title

    @property
    def maintenance_type(self) -> MaintenanceType:
        return self._maintenance_type

    @property
    def priority(self) -> PriorityLevel:
        return self._priority

    @property
    def status(self) -> Status:
        return self._status

    @property
    def estimated_time(self) -> int:
        return self._estimated_time

    @property
    def estimated_time_unit(self) -> TimeUnit:
        return self._estimated_time_unit

    @property
    def description(self) -> str:
        return self._description
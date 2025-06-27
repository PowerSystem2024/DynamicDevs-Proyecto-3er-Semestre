from datetime import date


class IndustrialAsset:
    def __init__(self, asset_type: str = None, model: str = None, location: str = None, acquisition_date: date = None):
        self._id = None
        self._asset_type = asset_type
        self._model = model
        self._location = location
        self._acquisition_date = acquisition_date

    @property
    def id(self) -> int:
        return self._id

    @property
    def acquisition_date(self) -> date:
        return self._acquisition_date

    @property
    def location(self) -> str:
        return self._location

    @property
    def model(self) -> str:
        return self._model

    @property
    def asset_type(self) -> str:
        return self._asset_type

    @id.setter
    def id(self, value: int):
        self._id = value

    @acquisition_date.setter
    def acquisition_date(self, value: date):
        self._acquisition_date = value

    @location.setter
    def location(self, value: str):
        self._location = value

    @model.setter
    def model(self, value: str):
        self._model = value

    @asset_type.setter
    def asset_type(self, value: str):
        self._asset_type = value

    def __str__(self):
        return f"IndustrialAsset({self.id}, {self.asset_type}, {self.model}, {self.location}, {self.acquisition_date})"

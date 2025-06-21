from datetime import date


class IndustrialAsset:
    def __init__(self, asset_type: str, model: str, location: str, acquisition_date: date):
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

    @acquisition_date.setter
    def acquisition_date(self, value: date):
        if value is None:
            raise ValueError("acquisition_date cannot be None")
        if not isinstance(value, date):
            raise ValueError("acquisition_date must be a date")
        self._acquisition_date = value

    @location.setter
    def location(self, value: str):
        if value is None:
            raise ValueError("location cannot be None")
        if not isinstance(value, str):
            raise ValueError("location must be a string")
        self._location = value

    @model.setter
    def model(self, value: str):
        if value is None:
            raise ValueError("model cannot be None")
        if not isinstance(value, str):
            raise ValueError("model must be a string")
        self._model = value

    @asset_type.setter
    def asset_type(self, value: str):
        if value is None:
            raise ValueError("asset_type cannot be None")
        if not isinstance(value, str):
            raise ValueError("asset_type must be a string")
        self._asset_type = value

    def __str__(self):
        return f"IndustrialAsset({self.id}, {self.asset_type}, {self.model}, {self.location}, {self.acquisition_date})"

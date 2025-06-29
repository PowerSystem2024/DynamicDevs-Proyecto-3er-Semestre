from datetime import date


class IndustrialAssetData:
    def __init__(self, asset_type: str, model: str, location: str, acquisition_date: str):
        self._asset_type = asset_type
        self._model = model
        self._location = location
        self._acquisition_date = acquisition_date

    @property
    def asset_type(self) -> str:
        return self._asset_type

    @property
    def model(self) -> str:
        return self._model

    @property
    def location(self) -> str:
        return self._location

    @property
    def acquisition_date(self) -> str:
        return self._acquisition_date

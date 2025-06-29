from datetime import datetime
from src.repository.IndustrialAssetRepository import IndustrialAssetRepository
from src.domain.IndustrialAsset import IndustrialAsset
from src.domain.IndustrialAssetData import IndustrialAssetData

class IndustrialAssetService:
    def __init__(self, repository: IndustrialAssetRepository):
        self._repository = repository

    def create_asset(self, asset_data: IndustrialAssetData) -> IndustrialAsset:
        """
        Crea y persiste un nuevo IndustrialAsset después de validar los datos.
        
        Args:
            asset_data: Objeto con los datos a validar y utilizar para la creación.
            
        Returns:
            IndustrialAsset: El objeto creado y persistido, con ID asignado.
            
        Raises:
            TypeError: Cuando el tipo de dato es incorrecto.
            ValueError: Cuando el contenido no cumple validaciones.
        """
        # Validar y procesar fecha
        date_str = asset_data.acquisition_date
        try:
            acquisition_date = self._validate_and_parse_date(date_str)
        except (TypeError, ValueError) as e:
            raise type(e)(f"Fecha inválida: {str(e)}") from e

        # Validar campos de texto
        self._validate_text_field(asset_data.location, "Ubicación")
        self._validate_text_field(asset_data.model, "Modelo")
        self._validate_text_field(asset_data.asset_type, "Tipo de activo")

        # Crear y guardar el activo
        asset = IndustrialAsset(
            asset_type= asset_data.asset_type,
            model= asset_data.model,
            location= asset_data.location,
            acquisition_date= acquisition_date
        )
        
        return self._repository.save(asset)

    @staticmethod
    def _validate_and_parse_date(self, date_str: str) -> datetime.date:
        """Valida y convierte una cadena de fecha en formato dd/mm/yyyy a date."""
        if not isinstance(date_str, str):
            raise TypeError("La fecha debe ser una cadena de texto")
        
        date_str = date_str.strip()
        if not date_str:
            raise ValueError("La fecha no puede estar vacía")
            
        try:
            return datetime.strptime(date_str, "%d/%m/%Y").date()
        except ValueError as e:
            raise ValueError("Formato de fecha inválido. Use dd/mm/yyyy") from e

    @staticmethod
    def _validate_text_field(self, value: str, field_name: str) -> None:
        """Valida campos de texto genéricos según requisitos."""
        if not isinstance(value, str):
            raise TypeError(f"{field_name} debe ser una cadena de texto")
            
        value = value.strip()
        if not value:
            raise ValueError(f"{field_name} no puede estar vacío")
        if len(value) == 1:
            raise ValueError(f"{field_name} no puede ser un único carácter")
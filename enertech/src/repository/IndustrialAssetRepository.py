import psycopg2
from typing import List, Optional
from src.domain.IndustrialAsset import IndustrialAsset

class IndustrialAssetRepository:
    def __init__(self, db_params: dict):
        """Inicializa el repositorio verificando conexión a tabla existente."""
        self._db_params = db_params
        self._verify_connection()

    def _verify_connection(self) -> None:
        """Verifica que la tabla INDUSTRIAL_ASSETS exista."""
        try:
            with self._get_connection() as conn:
                with conn.cursor() as cursor:
                    cursor.execute("SELECT 1 FROM INDUSTRIAL_ASSETS LIMIT 1")
        except psycopg2.Error as e:
            raise RuntimeError(
                "Tabla INDUSTRIAL_ASSETS no existe. Ejecute scripts SQL primero."
            ) from e

    def save(self, asset: IndustrialAsset) -> IndustrialAsset:
        # Implementación existente...
        pass

    def update(self, asset: IndustrialAsset) -> IndustrialAsset:
        # Implementación existente...
        pass

    def getById(self, assetId: int) -> Optional[IndustrialAsset]:
        """Obtiene un activo por ID. Retorna None si no existe."""
        with self._get_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute(
                    "SELECT * FROM INDUSTRIAL_ASSETS WHERE id = %s", 
                    (assetId,)
                )
                if row := cursor.fetchone():
                    return self._row_to_entity(row)
        return None

    def listByCriteria(
        self, 
        criteria: List[str], 
        sort: str = "id"
    ) -> Optional[List[IndustrialAsset]]:
        """Lista activos filtrados. Retorna None si no hay resultados."""
        query = "SELECT * FROM INDUSTRIAL_ASSETS"
        if criteria:
            query += " WHERE " + " AND ".join(criteria)
        query += f" ORDER BY {sort}"

        with self._get_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute(query)
                if results := cursor.fetchall():
                    return [self._row_to_entity(row) for row in results]
        return None

    def delete(self, assetId: int) -> None:
        """Elimina permanentemente un activo. Lanza ValueError si no existe."""
        if not self.getById(assetId):
            raise ValueError(f"Activo con ID {assetId} no encontrado")
        
        with self._get_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute(
                    "DELETE FROM INDUSTRIAL_ASSETS WHERE id = %s", 
                    (assetId,)
                )
                conn.commit()

    def _row_to_entity(self, row) -> IndustrialAsset:
        """Convierte fila de DB a objeto IndustrialAsset."""
        asset = IndustrialAsset(
            asset_type=row[1],
            model=row[2],
            location=row[3],
            acquisition_date=row[4]
        )
        asset._id = row[0]  # Asignar ID interno
        return asset
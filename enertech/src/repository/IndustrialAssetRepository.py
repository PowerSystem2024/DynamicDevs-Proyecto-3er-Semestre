from typing import Optional, List
from enertech.src.database.DatabaseManager import DatabaseManager
from enertech.src.domain.IndustrialAsset import IndustrialAsset
from enertech.src.repository.Criteria import Criteria


class IndustrialAssetRepository:
    def __init__(self, db_manager: DatabaseManager):
        self._db_manager = db_manager

    def save(self, asset: IndustrialAsset) -> IndustrialAsset:
        """
        Guarda un objeto IndustrialAsset y retorna todos sus datos
        Args:
            asset: Objeto IndustrialAsset con los atributos: [asset_type, model, location, acquisition_date]
        Returns:
            Objeto IndustrialAsset con sus datos completos.
        """
        query = """
                INSERT INTO INDUSTRIAL_ASSETS (asset_type, model, location, acquisition_date)
                VALUES (%s, %s, %s, %s) RETURNING id, asset_type, model, location, acquisition_date;
                """
        with self._db_manager.get_connection().cursor() as cursor:
            cursor.execute(
                query,
                (asset.asset_type, asset.model, asset.location, asset.acquisition_date)
            )
            self._db_manager.commit_transaction()
            result = cursor.fetchone()
            asset_saved = self._row_to_entity(result)
            self._db_manager.close_connection()
        return asset_saved

    def update(self, asset: IndustrialAsset) -> IndustrialAsset | None:
        """
        Actualiza un IndustrialAsset en la base de datos solo si hay cambios reales.
        Args:
            asset: Objeto IndustrialAsset con los atributos a actualizar.
                   Debe contener al menos el ID y uno o más campos modificados
        Returns:
            Objeto IndustrialAsset actualizado con todos sus datos o
            None si no hay cambios que realizar.
        """
        # Construir dinámicamente la parte SET del UPDATE
        updates = []
        params_set = []
        column_names = ['asset_type', 'model', 'location', 'acquisition_date']
        # Obtener campos a actualizar y sus nuevos valores
        for field in column_names:
            if hasattr(asset, field) and getattr(asset, field) is not None:
                updates.append(f"{field} = %s")
                params_set.append(getattr(asset, field))
        if not updates:
            # Si no hay campos para actualizar, retornar None
            return None
        query = f"""
                    UPDATE INDUSTRIAL_ASSETS
                    SET {', '.join(updates)}
                    WHERE id = %s
                    AND ({' OR '.join([f"{field} <> %s" for field in column_names
                                       if hasattr(asset, field) and getattr(asset, field) is not None])})
                    RETURNING id, asset_type, model, location, acquisition_date;
                """
        # Parámetros para la consulta: nuevos valores + id + valores originales para comparación
        params = params_set.copy()  # nuevos valores para SET
        params.append(asset.id)  # id para WHERE
        # Añadir valores originales para comparación en WHERE
        for field in column_names:
            if hasattr(asset, field) and getattr(asset, field) is not None:
                params.append(getattr(asset, field))
        with self._db_manager.get_connection().cursor() as cursor:
            cursor.execute(query, params)
            self._db_manager.commit_transaction()
            result = cursor.fetchone()
            self._db_manager.close_connection()
            if not result:
                return None
            asset_updated = self._row_to_entity(result)
        return asset_updated

    def get_by_id(self, asset_id: int) -> Optional[IndustrialAsset]:
        """
        Obtiene un activo industrial por ID.
        Args:
            asset_id: ID del activo industrial a buscar.
        Returns:
            Activo industrial encontrado o None si no existe.
        """
        with self._db_manager.get_connection().cursor() as cursor:
            cursor.execute(
                "SELECT * FROM INDUSTRIAL_ASSETS WHERE id = %s",
                (asset_id,)
            )
            row = cursor.fetchone()
            self._db_manager.close_connection()
            if row:
                return self._row_to_entity(row)
        return None

    def list_by_criteria(self, filters: dict) -> List[IndustrialAsset]:
        """
        Obtiene assets industriales con filtros opcionales.
        Args:
            filters: Diccionario con filtros columna : valor (ej.: {'asset_type': 'turbina', 'location': 'planta 1'})
        Returns:
            Lista de IndustrialAsset que cumplen con los filtros (o todos si no hay filtros)
        """
        _TABLE_NAME = "INDUSTRIAL_ASSETS"
        results = Criteria.list_by_criteria(_TABLE_NAME, self._db_manager, filters)
        return [self._row_to_entity(result) for result in results]

    def delete(self, asset_id: int) -> None:
        """
        Elimina permanentemente un activo por ID.
        Args:
            asset_id: ID del activo industrial a eliminar.
        """
        with self._db_manager.get_connection().cursor() as cursor:
            cursor.execute(
                "DELETE FROM INDUSTRIAL_ASSETS WHERE id = %s",
                (asset_id,)
            )
            self._db_manager.commit_transaction()
            self._db_manager.close_connection()

    @staticmethod
    def _row_to_entity(row) -> IndustrialAsset:
        """
        [USO INTERNO] Convierte fila de DB a objeto IndustrialAsset.
        Args:
            row: Fila obtenida de la base de datos.
        """
        asset = IndustrialAsset(
            asset_type=row[1],
            model=row[2],
            location=row[3],
            acquisition_date=row[4]
        )
        asset.id = row[0]  # Asignar ID interno
        return asset

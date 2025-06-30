from typing import Any, List

from enertech.src.database.DatabaseManager import DatabaseManager


class Criteria:
    def __init__(self):
        pass

    @staticmethod
    def list_by_criteria(table_name: str, db_connection: DatabaseManager, criteria: dict) -> List[Any]:
        """
        Permite obtener los resultados de una tabla en determinada base de datos. Si aplican filtros (criterio),
        devuelve los resultados filtrados, caso contrario devuelve todos los resultados o devuelve una lista
        vacía si no se encuentran resultados.
        :param table_name: Nombre de la tabla en la base de datos a buscar.
        :param db_connection: Conexión de la base de datos.
        :param criteria: Criterios de filtrado, ej.: {'columna_en_la_tabla': 'valor_en_la_columna'}. Por defecto None.
        :return: Lista de tuplas con los resultados según sí aplica filtros o no. Retorna None si no hay resultados.
        """
        base_query = f"SELECT * FROM {table_name}"

        where_clauses = []
        params = []

        if criteria:
            for field, value in criteria.items():
                if value is not None:
                    where_clauses.append(f"{field} ILIKE %s")  # ILIKE para case-insensitive
                    params.append(f"%{value}%")  # Wildcards para búsqueda parcial

        if where_clauses:
            base_query += " WHERE " + " AND ".join(where_clauses)

        with db_connection.get_connection().cursor() as cursor:
            cursor.execute(base_query, params)
            results = cursor.fetchall()
            db_connection.close_connection()
        return results

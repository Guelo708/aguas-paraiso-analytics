from decimal import Decimal
from typing import Any

from sqlalchemy import text
from sqlalchemy.engine import Engine
from sqlalchemy.sql.elements import TextClause


class PrediosRepository:
    def __init__(self, engine: Engine) -> None:
        self._engine = engine

    def obtener_predios_por_sector(
        self,
    ) -> list[dict[str, Any]]:
        consulta = text(
            """
            WITH total_predios AS (
                SELECT COUNT(*) AS total
                FROM predios
            )
            SELECT
                s.id AS categoria_id,
                s.nombre,
                COUNT(p.id) AS cantidad,
                CASE
                    WHEN total_predios.total > 0
                    THEN ROUND(
                        (
                            COUNT(p.id)::numeric
                            / total_predios.total
                        ) * 100,
                        2
                    )
                    ELSE 0
                END AS porcentaje
            FROM sectores s
            CROSS JOIN total_predios
            LEFT JOIN predios p
                ON p.sector_id = s.id
            GROUP BY
                s.id,
                s.nombre,
                total_predios.total
            ORDER BY
                cantidad DESC,
                s.nombre ASC
            """
        )

        return self._ejecutar_distribucion(consulta)

    def obtener_predios_por_tipo(
        self,
    ) -> list[dict[str, Any]]:
        consulta = text(
            """
            WITH total_predios AS (
                SELECT COUNT(*) AS total
                FROM predios
            )
            SELECT
                tp.id AS categoria_id,
                tp.nombre,
                COUNT(p.id) AS cantidad,
                CASE
                    WHEN total_predios.total > 0
                    THEN ROUND(
                        (
                            COUNT(p.id)::numeric
                            / total_predios.total
                        ) * 100,
                        2
                    )
                    ELSE 0
                END AS porcentaje
            FROM tipos_predios tp
            CROSS JOIN total_predios
            LEFT JOIN predios p
                ON p.tipo_predio_id = tp.id
            GROUP BY
                tp.id,
                tp.nombre,
                total_predios.total
            ORDER BY
                cantidad DESC,
                tp.nombre ASC
            """
        )

        return self._ejecutar_distribucion(consulta)

    def _ejecutar_distribucion(
        self,
        consulta: TextClause,
    ) -> list[dict[str, Any]]:
        with self._engine.connect() as connection:
            connection.execute(
                text("SET TRANSACTION READ ONLY")
            )

            resultados = connection.execute(
                consulta
            ).mappings().all()

            connection.rollback()

        return [
            {
                "categoria_id": int(
                    resultado["categoria_id"]
                ),
                "nombre": str(
                    resultado["nombre"]
                ),
                "cantidad": int(
                    resultado["cantidad"] or 0
                ),
                "porcentaje": Decimal(
                    resultado["porcentaje"] or 0
                ),
            }
            for resultado in resultados
        ]

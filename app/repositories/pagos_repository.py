from decimal import Decimal
from typing import Any

from sqlalchemy import text
from sqlalchemy.engine import Engine


class PagosRepository:
    def __init__(self, engine: Engine) -> None:
        self._engine = engine

    def obtener_pagos_por_metodo(
        self,
        anio: int,
    ) -> list[dict[str, Any]]:
        consulta = text(
            """
            WITH pagos_filtrados AS (
                SELECT
                    metodo_pago,
                    valor_pagado
                FROM pagos
                WHERE EXTRACT(
                    YEAR FROM fecha_pago
                )::integer = :anio
            ),
            totales AS (
                SELECT
                    COUNT(*) AS cantidad_total,
                    COALESCE(
                        SUM(valor_pagado),
                        0
                    ) AS valor_total
                FROM pagos_filtrados
            ),
            agrupados AS (
                SELECT
                    metodo_pago,
                    COUNT(*) AS cantidad,
                    COALESCE(
                        SUM(valor_pagado),
                        0
                    ) AS valor_recaudado
                FROM pagos_filtrados
                GROUP BY metodo_pago
            )
            SELECT
                agrupados.metodo_pago,
                agrupados.cantidad,
                agrupados.valor_recaudado,
                CASE
                    WHEN totales.cantidad_total > 0
                    THEN ROUND(
                        (
                            agrupados.cantidad::numeric
                            / totales.cantidad_total
                        ) * 100,
                        2
                    )
                    ELSE 0
                END AS porcentaje_cantidad,
                CASE
                    WHEN totales.valor_total > 0
                    THEN ROUND(
                        (
                            agrupados.valor_recaudado
                            / totales.valor_total
                        ) * 100,
                        2
                    )
                    ELSE 0
                END AS porcentaje_valor
            FROM agrupados
            CROSS JOIN totales
            ORDER BY
                agrupados.valor_recaudado DESC,
                agrupados.metodo_pago ASC
            """
        )

        with self._engine.connect() as connection:
            connection.execute(
                text("SET TRANSACTION READ ONLY")
            )

            resultados = connection.execute(
                consulta,
                {"anio": anio},
            ).mappings().all()

            connection.rollback()

        return [
            {
                "metodo_pago": str(
                    resultado["metodo_pago"]
                ),
                "cantidad": int(
                    resultado["cantidad"] or 0
                ),
                "valor_recaudado": Decimal(
                    resultado["valor_recaudado"] or 0
                ),
                "porcentaje_cantidad": Decimal(
                    resultado["porcentaje_cantidad"] or 0
                ),
                "porcentaje_valor": Decimal(
                    resultado["porcentaje_valor"] or 0
                ),
            }
            for resultado in resultados
        ]

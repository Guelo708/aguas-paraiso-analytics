from decimal import Decimal
from typing import Any

from sqlalchemy import text
from sqlalchemy.engine import Engine
from sqlalchemy.sql.elements import TextClause


class SeriesRepository:
    def __init__(self, engine: Engine) -> None:
        self._engine = engine

    def obtener_facturas_por_estado(
        self,
    ) -> list[dict[str, Any]]:
        consulta = text(
            """
            WITH pagos_por_factura AS (
                SELECT
                    factura_id,
                    COALESCE(
                        SUM(valor_pagado),
                        0
                    ) AS total_pagado
                FROM pagos
                GROUP BY factura_id
            )
            SELECT
                f.estado,
                COUNT(*) AS cantidad,
                COALESCE(
                    SUM(f.valor_factura),
                    0
                ) AS valor_facturado,
                COALESCE(
                    SUM(
                        GREATEST(
                            f.valor_factura
                            - COALESCE(
                                p.total_pagado,
                                0
                            ),
                            0
                        )
                    ),
                    0
                ) AS saldo_pendiente
            FROM facturas f
            LEFT JOIN pagos_por_factura p
                ON p.factura_id = f.id
            GROUP BY f.estado
            ORDER BY
                CASE f.estado
                    WHEN 'PENDIENTE' THEN 1
                    WHEN 'PARCIAL' THEN 2
                    WHEN 'PAGADA' THEN 3
                    WHEN 'VENCIDA' THEN 4
                    ELSE 5
                END
            """
        )

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
                "estado": str(resultado["estado"]),
                "cantidad": int(
                    resultado["cantidad"] or 0
                ),
                "valor_facturado": Decimal(
                    resultado["valor_facturado"] or 0
                ),
                "saldo_pendiente": Decimal(
                    resultado["saldo_pendiente"] or 0
                ),
            }
            for resultado in resultados
        ]

    def obtener_facturacion_mensual(
        self,
        anio: int,
    ) -> list[dict[str, Any]]:
        consulta = text(
            """
            WITH meses AS (
                SELECT generate_series(1, 12) AS mes
            ),
            facturacion AS (
                SELECT
                    mes,
                    COUNT(*) AS cantidad,
                    COALESCE(
                        SUM(valor_factura),
                        0
                    ) AS valor
                FROM facturas
                WHERE anio = :anio
                GROUP BY mes
            )
            SELECT
                meses.mes,
                CASE meses.mes
                    WHEN 1 THEN 'Enero'
                    WHEN 2 THEN 'Febrero'
                    WHEN 3 THEN 'Marzo'
                    WHEN 4 THEN 'Abril'
                    WHEN 5 THEN 'Mayo'
                    WHEN 6 THEN 'Junio'
                    WHEN 7 THEN 'Julio'
                    WHEN 8 THEN 'Agosto'
                    WHEN 9 THEN 'Septiembre'
                    WHEN 10 THEN 'Octubre'
                    WHEN 11 THEN 'Noviembre'
                    WHEN 12 THEN 'Diciembre'
                END AS nombre_mes,
                COALESCE(
                    facturacion.cantidad,
                    0
                ) AS cantidad,
                COALESCE(
                    facturacion.valor,
                    0
                ) AS valor
            FROM meses
            LEFT JOIN facturacion
                ON facturacion.mes = meses.mes
            ORDER BY meses.mes
            """
        )

        return self._obtener_serie_mensual(
            consulta=consulta,
            parametros={"anio": anio},
        )

    def obtener_recaudo_mensual(
        self,
        anio: int,
    ) -> list[dict[str, Any]]:
        consulta = text(
            """
            WITH meses AS (
                SELECT generate_series(1, 12) AS mes
            ),
            recaudo AS (
                SELECT
                    EXTRACT(
                        MONTH FROM fecha_pago
                    )::integer AS mes,
                    COUNT(*) AS cantidad,
                    COALESCE(
                        SUM(valor_pagado),
                        0
                    ) AS valor
                FROM pagos
                WHERE EXTRACT(
                    YEAR FROM fecha_pago
                )::integer = :anio
                GROUP BY EXTRACT(
                    MONTH FROM fecha_pago
                )
            )
            SELECT
                meses.mes,
                CASE meses.mes
                    WHEN 1 THEN 'Enero'
                    WHEN 2 THEN 'Febrero'
                    WHEN 3 THEN 'Marzo'
                    WHEN 4 THEN 'Abril'
                    WHEN 5 THEN 'Mayo'
                    WHEN 6 THEN 'Junio'
                    WHEN 7 THEN 'Julio'
                    WHEN 8 THEN 'Agosto'
                    WHEN 9 THEN 'Septiembre'
                    WHEN 10 THEN 'Octubre'
                    WHEN 11 THEN 'Noviembre'
                    WHEN 12 THEN 'Diciembre'
                END AS nombre_mes,
                COALESCE(
                    recaudo.cantidad,
                    0
                ) AS cantidad,
                COALESCE(
                    recaudo.valor,
                    0
                ) AS valor
            FROM meses
            LEFT JOIN recaudo
                ON recaudo.mes = meses.mes
            ORDER BY meses.mes
            """
        )

        return self._obtener_serie_mensual(
            consulta=consulta,
            parametros={"anio": anio},
        )

    def _obtener_serie_mensual(
        self,
        consulta: TextClause,
        parametros: dict[str, Any],
    ) -> list[dict[str, Any]]:
        with self._engine.connect() as connection:
            connection.execute(
                text("SET TRANSACTION READ ONLY")
            )

            resultados = connection.execute(
                consulta,
                parametros,
            ).mappings().all()

            connection.rollback()

        return [
            {
                "mes": int(resultado["mes"]),
                "nombre_mes": str(
                    resultado["nombre_mes"]
                ),
                "cantidad": int(
                    resultado["cantidad"] or 0
                ),
                "valor": Decimal(
                    resultado["valor"] or 0
                ),
            }
            for resultado in resultados
        ]

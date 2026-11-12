from decimal import Decimal
from typing import Any

from sqlalchemy import text
from sqlalchemy.engine import Engine


class EstadisticasRepository:
    def __init__(self, engine: Engine) -> None:
        self._engine = engine

    def obtener_resumen(self) -> dict[str, Any]:
        consulta = text(
            """
            WITH pagos_por_factura AS (
                SELECT
                    factura_id,
                    COALESCE(SUM(valor_pagado), 0) AS total_pagado
                FROM pagos
                GROUP BY factura_id
            ),
            resumen_facturas AS (
                SELECT
                    COUNT(*) AS total_facturas,
                    COUNT(*) FILTER (
                        WHERE estado = 'PENDIENTE'
                    ) AS facturas_pendientes,
                    COUNT(*) FILTER (
                        WHERE estado = 'PARCIAL'
                    ) AS facturas_parciales,
                    COUNT(*) FILTER (
                        WHERE estado = 'PAGADA'
                    ) AS facturas_pagadas,
                    COUNT(*) FILTER (
                        WHERE estado = 'VENCIDA'
                    ) AS facturas_vencidas,
                    COALESCE(
                        SUM(
                            CASE
                                WHEN estado IN (
                                    'PENDIENTE',
                                    'PARCIAL',
                                    'VENCIDA'
                                )
                                THEN GREATEST(
                                    valor_factura
                                    - COALESCE(
                                        pagos_por_factura.total_pagado,
                                        0
                                    ),
                                    0
                                )
                                ELSE 0
                            END
                        ),
                        0
                    ) AS cartera_pendiente
                FROM facturas
                LEFT JOIN pagos_por_factura
                    ON pagos_por_factura.factura_id = facturas.id
            )
            SELECT
                (
                    SELECT COUNT(*)
                    FROM usuarios
                ) AS total_suscriptores,
                (
                    SELECT COUNT(*)
                    FROM predios
                ) AS total_predios,
                resumen_facturas.total_facturas,
                (
                    SELECT COUNT(*)
                    FROM pagos
                ) AS total_pagos,
                resumen_facturas.facturas_pendientes,
                resumen_facturas.facturas_parciales,
                resumen_facturas.facturas_pagadas,
                resumen_facturas.facturas_vencidas,
                resumen_facturas.cartera_pendiente,
                (
                    SELECT COALESCE(
                        SUM(valor_pagado),
                        0
                    )
                    FROM pagos
                ) AS recaudo_acumulado
            FROM resumen_facturas
            """
        )

        with self._engine.connect() as connection:
            connection.execute(
                text("SET TRANSACTION READ ONLY")
            )

            resultado = connection.execute(
                consulta
            ).mappings().one()

            connection.rollback()

        return {
            "total_suscriptores": int(
                resultado["total_suscriptores"] or 0
            ),
            "total_predios": int(
                resultado["total_predios"] or 0
            ),
            "total_facturas": int(
                resultado["total_facturas"] or 0
            ),
            "total_pagos": int(
                resultado["total_pagos"] or 0
            ),
            "facturas_pendientes": int(
                resultado["facturas_pendientes"] or 0
            ),
            "facturas_parciales": int(
                resultado["facturas_parciales"] or 0
            ),
            "facturas_pagadas": int(
                resultado["facturas_pagadas"] or 0
            ),
            "facturas_vencidas": int(
                resultado["facturas_vencidas"] or 0
            ),
            "cartera_pendiente": Decimal(
                resultado["cartera_pendiente"] or 0
            ),
            "recaudo_acumulado": Decimal(
                resultado["recaudo_acumulado"] or 0
            ),
        }

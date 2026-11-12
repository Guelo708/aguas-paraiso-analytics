from decimal import Decimal

from pydantic import BaseModel, Field


class ResumenEstadisticas(BaseModel):
    total_suscriptores: int = Field(
        ge=0,
        description="Cantidad total de suscriptores registrados.",
    )
    total_predios: int = Field(
        ge=0,
        description="Cantidad total de predios registrados.",
    )
    total_facturas: int = Field(
        ge=0,
        description="Cantidad total de facturas generadas.",
    )
    total_pagos: int = Field(
        ge=0,
        description="Cantidad total de pagos registrados.",
    )

    facturas_pendientes: int = Field(ge=0)
    facturas_parciales: int = Field(ge=0)
    facturas_pagadas: int = Field(ge=0)
    facturas_vencidas: int = Field(ge=0)

    cartera_pendiente: Decimal = Field(
        ge=0,
        description=(
            "Valor facturado pendiente de pago después de descontar "
            "los abonos registrados."
        ),
    )
    recaudo_acumulado: Decimal = Field(
        ge=0,
        description="Suma histórica de los pagos registrados.",
    )

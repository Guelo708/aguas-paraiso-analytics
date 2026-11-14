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


class DeudorEstadistica(BaseModel):
    nombre: str = Field(
        description="Nombre completo del suscriptor propietario del predio."
    )
    predio: str = Field(
        description="Código o identificador del predio."
    )
    facturas: int = Field(
        ge=1,
        description="Cantidad de facturas pendientes, parciales o vencidas."
    )
    deuda: Decimal = Field(
        ge=0,
        description="Saldo total adeudado después de descontar abonos."
    )


class CarteraSectorEstadistica(BaseModel):
    sector: str = Field(
        description="Nombre del sector o vereda."
    )
    cartera_vencida: Decimal = Field(
        ge=0,
        description="Saldo en pesos de facturas con estado VENCIDA en el sector."
    )
    cartera_pendiente: Decimal = Field(
        ge=0,
        description="Saldo en pesos de facturas PENDIENTE o PARCIAL en el sector."
    )
    total_cartera: Decimal = Field(
        ge=0,
        description="Suma de cartera vencida y pendiente en el sector."
    )
    facturas_con_saldo: int = Field(
        ge=0,
        description="Cantidad de facturas con saldo pendiente en el sector."
    )

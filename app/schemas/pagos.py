from decimal import Decimal

from pydantic import BaseModel, Field


class PagoMetodoEstadistica(BaseModel):
    metodo_pago: str = Field(
        description="Método utilizado para registrar el pago."
    )
    cantidad: int = Field(
        ge=0,
        description="Cantidad de pagos registrados."
    )
    valor_recaudado: Decimal = Field(
        ge=0,
        description="Valor total recaudado mediante el método."
    )
    porcentaje_cantidad: Decimal = Field(
        ge=0,
        le=100,
        description=(
            "Participación porcentual del método "
            "sobre la cantidad total de pagos."
        ),
    )
    porcentaje_valor: Decimal = Field(
        ge=0,
        le=100,
        description=(
            "Participación porcentual del método "
            "sobre el recaudo total."
        ),
    )

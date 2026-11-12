from decimal import Decimal

from pydantic import BaseModel, Field


class EstadoFacturaEstadistica(BaseModel):
    estado: str
    cantidad: int = Field(ge=0)
    valor_facturado: Decimal = Field(ge=0)
    saldo_pendiente: Decimal = Field(ge=0)


class SerieMensualEstadistica(BaseModel):
    mes: int = Field(ge=1, le=12)
    nombre_mes: str
    cantidad: int = Field(ge=0)
    valor: Decimal = Field(ge=0)

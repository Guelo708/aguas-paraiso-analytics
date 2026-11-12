from decimal import Decimal

from pydantic import BaseModel, Field


class PredioCategoriaEstadistica(BaseModel):
    categoria_id: int = Field(
        ge=1,
        description="Identificador de la categoría.",
    )
    nombre: str = Field(
        description="Nombre del sector o tipo de predio.",
    )
    cantidad: int = Field(
        ge=0,
        description="Cantidad de predios asociados.",
    )
    porcentaje: Decimal = Field(
        ge=0,
        le=100,
        description=(
            "Participación porcentual sobre el total "
            "de predios registrados."
        ),
    )

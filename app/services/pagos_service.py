from app.repositories.pagos_repository import (
    PagosRepository,
)
from app.schemas.pagos import PagoMetodoEstadistica


class PagosService:
    def __init__(
        self,
        repository: PagosRepository,
    ) -> None:
        self._repository = repository

    def obtener_pagos_por_metodo(
        self,
        anio: int,
    ):
        datos = (
            self._repository
            .obtener_pagos_por_metodo(anio)
        )

        return [
            PagoMetodoEstadistica.model_validate(
                registro
            )
            for registro in datos
        ]

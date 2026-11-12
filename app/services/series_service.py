from app.repositories.series_repository import (
    SeriesRepository,
)
from app.schemas.series import (
    EstadoFacturaEstadistica,
    SerieMensualEstadistica,
)


class SeriesService:
    def __init__(
        self,
        repository: SeriesRepository,
    ) -> None:
        self._repository = repository

    def obtener_facturas_por_estado(
        self,
    ) -> list[EstadoFacturaEstadistica]:
        datos = (
            self._repository
            .obtener_facturas_por_estado()
        )

        return [
            EstadoFacturaEstadistica.model_validate(
                registro
            )
            for registro in datos
        ]

    def obtener_facturacion_mensual(
        self,
        anio: int,
    ) -> list[SerieMensualEstadistica]:
        datos = (
            self._repository
            .obtener_facturacion_mensual(anio)
        )

        return [
            SerieMensualEstadistica.model_validate(
                registro
            )
            for registro in datos
        ]

    def obtener_recaudo_mensual(
        self,
        anio: int,
    ) -> list[SerieMensualEstadistica]:
        datos = (
            self._repository
            .obtener_recaudo_mensual(anio)
        )

        return [
            SerieMensualEstadistica.model_validate(
                registro
            )
            for registro in datos
        ]

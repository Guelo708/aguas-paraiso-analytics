from app.repositories.estadisticas_repository import (
    EstadisticasRepository,
)
from app.schemas.estadisticas import (
    CarteraSectorEstadistica,
    DeudorEstadistica,
    ResumenEstadisticas,
)


class EstadisticasService:
    def __init__(
        self,
        repository: EstadisticasRepository,
    ) -> None:
        self._repository = repository

    def obtener_resumen(self) -> ResumenEstadisticas:
        datos = self._repository.obtener_resumen()

        return ResumenEstadisticas.model_validate(datos)

    def obtener_top_deudores(self) -> list[DeudorEstadistica]:
        resultados = self._repository.obtener_top_deudores()

        return [
            DeudorEstadistica.model_validate(item)
            for item in resultados
        ]

    def obtener_cartera_por_sector(self) -> list[CarteraSectorEstadistica]:
        resultados = self._repository.obtener_cartera_por_sector()

        return [
            CarteraSectorEstadistica.model_validate(item)
            for item in resultados
        ]

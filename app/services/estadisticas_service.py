from app.repositories.estadisticas_repository import (
    EstadisticasRepository,
)
from app.schemas.estadisticas import ResumenEstadisticas


class EstadisticasService:
    def __init__(
        self,
        repository: EstadisticasRepository,
    ) -> None:
        self._repository = repository

    def obtener_resumen(self) -> ResumenEstadisticas:
        datos = self._repository.obtener_resumen()

        return ResumenEstadisticas.model_validate(datos)

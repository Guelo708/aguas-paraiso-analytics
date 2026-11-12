from app.repositories.predios_repository import (
    PrediosRepository,
)
from app.schemas.predios import PredioCategoriaEstadistica


class PrediosService:
    def __init__(
        self,
        repository: PrediosRepository,
    ) -> None:
        self._repository = repository

    def obtener_predios_por_sector(self):
        datos = (
            self._repository
            .obtener_predios_por_sector()
        )

        return [
            PredioCategoriaEstadistica.model_validate(
                registro
            )
            for registro in datos
        ]

    def obtener_predios_por_tipo(self):
        datos = (
            self._repository
            .obtener_predios_por_tipo()
        )

        return [
            PredioCategoriaEstadistica.model_validate(
                registro
            )
            for registro in datos
        ]

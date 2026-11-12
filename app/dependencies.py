from functools import lru_cache

from app.database import get_engine
from app.repositories.estadisticas_repository import (
    EstadisticasRepository,
)
from app.services.estadisticas_service import (
    EstadisticasService,
)


@lru_cache
def get_estadisticas_service() -> EstadisticasService:
    repository = EstadisticasRepository(
        engine=get_engine(),
    )

    return EstadisticasService(
        repository=repository,
    )

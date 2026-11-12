from functools import lru_cache

from app.database import get_engine
from app.repositories.predios_repository import (
    PrediosRepository,
)
from app.services.predios_service import PrediosService


@lru_cache
def get_predios_service() -> PrediosService:
    repository = PrediosRepository(
        engine=get_engine(),
    )

    return PrediosService(
        repository=repository,
    )

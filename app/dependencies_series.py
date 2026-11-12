from functools import lru_cache

from app.database import get_engine
from app.repositories.series_repository import (
    SeriesRepository,
)
from app.services.series_service import SeriesService


@lru_cache
def get_series_service() -> SeriesService:
    repository = SeriesRepository(
        engine=get_engine(),
    )

    return SeriesService(
        repository=repository,
    )

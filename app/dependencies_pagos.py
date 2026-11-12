from functools import lru_cache

from app.database import get_engine
from app.repositories.pagos_repository import (
    PagosRepository,
)
from app.services.pagos_service import PagosService


@lru_cache
def get_pagos_service() -> PagosService:
    repository = PagosRepository(
        engine=get_engine(),
    )

    return PagosService(
        repository=repository,
    )

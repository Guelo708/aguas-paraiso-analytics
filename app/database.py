from functools import lru_cache
from typing import Any

from sqlalchemy import Engine, create_engine, text

from app.config import get_settings


@lru_cache
def get_engine() -> Engine:
    settings = get_settings()

    if not settings.database_url:
        raise RuntimeError(
            "DATABASE_URL no está configurada."
        )

    return create_engine(
        settings.database_url,
        pool_pre_ping=True,
        pool_size=3,
        max_overflow=2,
        pool_recycle=300,
    )


def comprobar_conexion() -> dict[str, Any]:
    engine = get_engine()

    with engine.connect() as connection:
        connection.execute(
            text("SET TRANSACTION READ ONLY")
        )

        result = connection.execute(
            text(
                """
                SELECT
                    current_database() AS database_name,
                    current_user AS database_user,
                    version() AS database_version
                """
            )
        ).mappings().one()

        connection.rollback()

    return {
        "status": "ok",
        "database": result["database_name"],
        "user": result["database_user"],
        "engine": "PostgreSQL",
    }


from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.estadisticas import (
    router as estadisticas_router,
)
from app.api.series import router as series_router
from app.api.pagos import router as pagos_router
from app.config import get_settings


settings = get_settings()

app = FastAPI(
    title=settings.app_name,
    description=(
        "Microservicio headless para indicadores y estadísticas "
        "del acueducto Aguas Paraíso."
    ),
    version=settings.app_version,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins_list,
    allow_credentials=False,
    allow_methods=["GET"],
    allow_headers=["*"],
)

app.include_router(estadisticas_router)
app.include_router(series_router)
app.include_router(pagos_router)


@app.get(
    "/health",
    tags=["Salud"],
    summary="Comprobar estado del microservicio",
)
def health_check() -> dict[str, str]:
    return {
        "status": "ok",
        "service": "aguas-paraiso-analytics",
        "version": settings.app_version,
    }


from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI(
    title="Aguas Paraíso Analytics",
    description=(
        "Microservicio headless para indicadores y estadísticas "
        "del acueducto Aguas Paraíso."
    ),
    version="0.1.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
    ],
    allow_credentials=False,
    allow_methods=["GET"],
    allow_headers=["*"],
)


@app.get(
    "/health",
    tags=["Salud"],
    summary="Comprobar estado del microservicio",
)
def health_check() -> dict[str, str]:
    return {
        "status": "ok",
        "service": "aguas-paraiso-analytics",
        "version": "0.1.0",
    }


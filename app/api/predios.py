from typing import Annotated

from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    status,
)
from sqlalchemy.exc import SQLAlchemyError

from app.dependencies_predios import (
    get_predios_service,
)
from app.schemas.predios import (
    PredioCategoriaEstadistica,
)
from app.services.predios_service import PrediosService


router = APIRouter(
    prefix="/api/estadisticas",
    tags=["Estadísticas de predios"],
)


@router.get(
    "/predios/sectores",
    response_model=list[PredioCategoriaEstadistica],
    summary="Agrupar predios por sector",
    description=(
        "Devuelve la cantidad y participación porcentual "
        "de los predios asociados a cada sector."
    ),
)
def obtener_predios_por_sector(
    service: Annotated[
        PrediosService,
        Depends(get_predios_service),
    ],
):
    try:
        return service.obtener_predios_por_sector()
    except SQLAlchemyError as error:
        raise HTTPException(
            status_code=(
                status.HTTP_503_SERVICE_UNAVAILABLE
            ),
            detail=(
                "No fue posible consultar los predios "
                "agrupados por sector."
            ),
        ) from error


@router.get(
    "/predios/tipos",
    response_model=list[PredioCategoriaEstadistica],
    summary="Agrupar predios por tipo",
    description=(
        "Devuelve la cantidad y participación porcentual "
        "de los predios asociados a cada tipo de predio."
    ),
)
def obtener_predios_por_tipo(
    service: Annotated[
        PrediosService,
        Depends(get_predios_service),
    ],
):
    try:
        return service.obtener_predios_por_tipo()
    except SQLAlchemyError as error:
        raise HTTPException(
            status_code=(
                status.HTTP_503_SERVICE_UNAVAILABLE
            ),
            detail=(
                "No fue posible consultar los predios "
                "agrupados por tipo."
            ),
        ) from error

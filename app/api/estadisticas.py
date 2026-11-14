from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.exc import SQLAlchemyError

from app.dependencies import get_estadisticas_service
from app.schemas.estadisticas import (
    CarteraSectorEstadistica,
    DeudorEstadistica,
    ResumenEstadisticas,
)
from app.services.estadisticas_service import (
    EstadisticasService,
)


router = APIRouter(
    prefix="/api/estadisticas",
    tags=["Estadísticas"],
)


@router.get(
    "/resumen",
    response_model=ResumenEstadisticas,
    summary="Obtener resumen general",
    description=(
        "Calcula indicadores generales de suscriptores, predios, "
        "facturas, pagos, recaudo y cartera pendiente."
    ),
)
def obtener_resumen(
    service: Annotated[
        EstadisticasService,
        Depends(get_estadisticas_service),
    ],
) -> ResumenEstadisticas:
    try:
        return service.obtener_resumen()
    except SQLAlchemyError as error:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=(
                "No fue posible consultar las estadísticas "
                "en la base de datos."
            ),
        ) from error


@router.get(
    "/cartera/top-deudores",
    response_model=list[DeudorEstadistica],
    summary="Obtener Top 5 deudores",
    description=(
        "Retorna los 5 predios/suscriptores con mayor saldo "
        "de cartera pendiente, parcial o vencida."
    ),
)
def obtener_top_deudores(
    service: Annotated[
        EstadisticasService,
        Depends(get_estadisticas_service),
    ],
) -> list[DeudorEstadistica]:
    try:
        return service.obtener_top_deudores()
    except SQLAlchemyError as error:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=(
                "No fue posible consultar el top de deudores "
                "en la base de datos."
            ),
        ) from error


@router.get(
    "/cartera/sectores",
    response_model=list[CarteraSectorEstadistica],
    summary="Obtener cartera vencida y pendiente por sector",
    description=(
        "Agrupa el saldo de cartera vencida y pendiente/parcial "
        "por cada sector registrado."
    ),
)
def obtener_cartera_por_sector(
    service: Annotated[
        EstadisticasService,
        Depends(get_estadisticas_service),
    ],
) -> list[CarteraSectorEstadistica]:
    try:
        return service.obtener_cartera_por_sector()
    except SQLAlchemyError as error:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=(
                "No fue posible consultar la cartera por sector "
                "en la base de datos."
            ),
        ) from error

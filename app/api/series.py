from typing import Annotated

from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    Query,
    status,
)
from sqlalchemy.exc import SQLAlchemyError

from app.dependencies_series import get_series_service
from app.schemas.series import (
    EstadoFacturaEstadistica,
    SerieMensualEstadistica,
)
from app.services.series_service import SeriesService


router = APIRouter(
    prefix="/api/estadisticas",
    tags=["Series estadísticas"],
)


@router.get(
    "/facturas/estados",
    response_model=list[EstadoFacturaEstadistica],
    summary="Agrupar facturas por estado",
    description=(
        "Devuelve la cantidad, el valor facturado y el saldo "
        "pendiente agrupados por estado de factura."
    ),
)
def obtener_facturas_por_estado(
    service: Annotated[
        SeriesService,
        Depends(get_series_service),
    ],
):
    try:
        return service.obtener_facturas_por_estado()
    except SQLAlchemyError as error:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=(
                "No fue posible consultar los estados "
                "de las facturas."
            ),
        ) from error


@router.get(
    "/facturacion/mensual",
    response_model=list[SerieMensualEstadistica],
    summary="Obtener facturación mensual",
    description=(
        "Devuelve la cantidad y el valor de las facturas "
        "generadas en cada mes del año solicitado."
    ),
)
def obtener_facturacion_mensual(
    service: Annotated[
        SeriesService,
        Depends(get_series_service),
    ],
    anio: Annotated[
        int,
        Query(
            ge=2000,
            le=2100,
            description="Año utilizado para agrupar las facturas.",
        ),
    ] = 2026,
):
    try:
        return service.obtener_facturacion_mensual(anio)
    except SQLAlchemyError as error:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=(
                "No fue posible consultar "
                "la facturación mensual."
            ),
        ) from error


@router.get(
    "/recaudo/mensual",
    response_model=list[SerieMensualEstadistica],
    summary="Obtener recaudo mensual",
    description=(
        "Devuelve la cantidad y el valor de los pagos "
        "registrados en cada mes del año solicitado."
    ),
)
def obtener_recaudo_mensual(
    service: Annotated[
        SeriesService,
        Depends(get_series_service),
    ],
    anio: Annotated[
        int,
        Query(
            ge=2000,
            le=2100,
            description="Año utilizado para agrupar los pagos.",
        ),
    ] = 2026,
):
    try:
        return service.obtener_recaudo_mensual(anio)
    except SQLAlchemyError as error:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=(
                "No fue posible consultar "
                "el recaudo mensual."
            ),
        ) from error

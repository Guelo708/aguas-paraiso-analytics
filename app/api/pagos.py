from typing import Annotated

from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    Query,
    status,
)
from sqlalchemy.exc import SQLAlchemyError

from app.dependencies_pagos import get_pagos_service
from app.schemas.pagos import PagoMetodoEstadistica
from app.services.pagos_service import PagosService


router = APIRouter(
    prefix="/api/estadisticas",
    tags=["Estadísticas de pagos"],
)


@router.get(
    "/pagos/metodos",
    response_model=list[PagoMetodoEstadistica],
    summary="Agrupar pagos por método",
    description=(
        "Devuelve la cantidad, el valor recaudado y la "
        "participación porcentual de cada método de pago "
        "durante el año solicitado."
    ),
)
def obtener_pagos_por_metodo(
    service: Annotated[
        PagosService,
        Depends(get_pagos_service),
    ],
    anio: Annotated[
        int,
        Query(
            ge=2000,
            le=2100,
            description=(
                "Año utilizado para agrupar "
                "los métodos de pago."
            ),
        ),
    ] = 2026,
):
    try:
        return service.obtener_pagos_por_metodo(
            anio
        )
    except SQLAlchemyError as error:
        raise HTTPException(
            status_code=(
                status.HTTP_503_SERVICE_UNAVAILABLE
            ),
            detail=(
                "No fue posible consultar los pagos "
                "agrupados por método."
            ),
        ) from error

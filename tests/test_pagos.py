from decimal import Decimal
from typing import Any

from fastapi.testclient import TestClient

from app.dependencies_pagos import get_pagos_service
from app.main import app
from app.schemas.pagos import PagoMetodoEstadistica


class FakePagosService:
    def obtener_pagos_por_metodo(
        self,
        anio: int,
    ):
        return [
            PagoMetodoEstadistica(
                metodo_pago="TRANSFERENCIA",
                cantidad=4,
                valor_recaudado=Decimal("80000.00"),
                porcentaje_cantidad=Decimal("40.00"),
                porcentaje_valor=Decimal("66.67"),
            ),
            PagoMetodoEstadistica(
                metodo_pago="EFECTIVO",
                cantidad=6,
                valor_recaudado=Decimal("40000.00"),
                porcentaje_cantidad=Decimal("60.00"),
                porcentaje_valor=Decimal("33.33"),
            ),
        ]


def override_pagos_service():
    return FakePagosService()


def realizar_peticion(
    ruta: str,
    parametros: dict[str, Any] | None = None,
):
    app.dependency_overrides[
        get_pagos_service
    ] = override_pagos_service

    try:
        with TestClient(app) as client:
            return client.get(
                ruta,
                params=parametros,
            )
    finally:
        app.dependency_overrides.pop(
            get_pagos_service,
            None,
        )


def test_pagos_por_metodo() -> None:
    response = realizar_peticion(
        "/api/estadisticas/pagos/metodos",
        parametros={"anio": 2026},
    )

    assert response.status_code == 200

    datos = response.json()

    assert len(datos) == 2

    assert datos[0]["metodo_pago"] == "TRANSFERENCIA"
    assert datos[0]["cantidad"] == 4
    assert datos[0]["valor_recaudado"] == "80000.00"
    assert datos[0]["porcentaje_cantidad"] == "40.00"
    assert datos[0]["porcentaje_valor"] == "66.67"


def test_pagos_por_metodo_valida_anio() -> None:
    response = realizar_peticion(
        "/api/estadisticas/pagos/metodos",
        parametros={"anio": 1999},
    )

    assert response.status_code == 422

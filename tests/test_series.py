from decimal import Decimal
from typing import Any

from fastapi.testclient import TestClient

from app.dependencies_series import get_series_service
from app.main import app
from app.schemas.series import (
    EstadoFacturaEstadistica,
    SerieMensualEstadistica,
)


class FakeSeriesService:
    def obtener_facturas_por_estado(self):
        return [
            EstadoFacturaEstadistica(
                estado="PENDIENTE",
                cantidad=3,
                valor_facturado=Decimal("150000.00"),
                saldo_pendiente=Decimal("98000.00"),
            ),
            EstadoFacturaEstadistica(
                estado="PAGADA",
                cantidad=2,
                valor_facturado=Decimal("100000.00"),
                saldo_pendiente=Decimal("0.00"),
            ),
        ]

    def obtener_facturacion_mensual(
        self,
        anio: int,
    ):
        return [
            SerieMensualEstadistica(
                mes=1,
                nombre_mes="Enero",
                cantidad=2,
                valor=Decimal("100000.00"),
            )
        ]

    def obtener_recaudo_mensual(
        self,
        anio: int,
    ):
        return [
            SerieMensualEstadistica(
                mes=1,
                nombre_mes="Enero",
                cantidad=3,
                valor=Decimal("75000.00"),
            )
        ]


def override_series_service():
    return FakeSeriesService()


def realizar_peticion(
    ruta: str,
    parametros: dict[str, Any] | None = None,
):
    app.dependency_overrides[
        get_series_service
    ] = override_series_service

    try:
        with TestClient(app) as client:
            return client.get(
                ruta,
                params=parametros,
            )
    finally:
        app.dependency_overrides.pop(
            get_series_service,
            None,
        )


def test_facturas_por_estado() -> None:
    response = realizar_peticion(
        "/api/estadisticas/facturas/estados"
    )

    assert response.status_code == 200

    datos = response.json()

    assert datos[0]["estado"] == "PENDIENTE"
    assert datos[0]["cantidad"] == 3
    assert datos[0]["valor_facturado"] == "150000.00"
    assert datos[0]["saldo_pendiente"] == "98000.00"


def test_facturacion_mensual() -> None:
    response = realizar_peticion(
        "/api/estadisticas/facturacion/mensual",
        parametros={"anio": 2026},
    )

    assert response.status_code == 200

    datos = response.json()

    assert datos[0]["mes"] == 1
    assert datos[0]["nombre_mes"] == "Enero"
    assert datos[0]["cantidad"] == 2
    assert datos[0]["valor"] == "100000.00"


def test_recaudo_mensual() -> None:
    response = realizar_peticion(
        "/api/estadisticas/recaudo/mensual",
        parametros={"anio": 2026},
    )

    assert response.status_code == 200

    datos = response.json()

    assert datos[0]["mes"] == 1
    assert datos[0]["nombre_mes"] == "Enero"
    assert datos[0]["cantidad"] == 3
    assert datos[0]["valor"] == "75000.00"

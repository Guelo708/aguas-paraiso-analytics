from decimal import Decimal

from fastapi.testclient import TestClient

from app.dependencies_predios import get_predios_service
from app.main import app
from app.schemas.predios import (
    PredioCategoriaEstadistica,
)


class FakePrediosService:
    def obtener_predios_por_sector(self):
        return [
            PredioCategoriaEstadistica(
                categoria_id=1,
                nombre="Sector Central",
                cantidad=3,
                porcentaje=Decimal("75.00"),
            ),
            PredioCategoriaEstadistica(
                categoria_id=2,
                nombre="Sector Norte",
                cantidad=1,
                porcentaje=Decimal("25.00"),
            ),
        ]

    def obtener_predios_por_tipo(self):
        return [
            PredioCategoriaEstadistica(
                categoria_id=1,
                nombre="Residencial",
                cantidad=2,
                porcentaje=Decimal("50.00"),
            ),
            PredioCategoriaEstadistica(
                categoria_id=2,
                nombre="Comercial",
                cantidad=2,
                porcentaje=Decimal("50.00"),
            ),
        ]


def override_predios_service():
    return FakePrediosService()


def realizar_peticion(ruta: str):
    app.dependency_overrides[
        get_predios_service
    ] = override_predios_service

    try:
        with TestClient(app) as client:
            return client.get(ruta)
    finally:
        app.dependency_overrides.pop(
            get_predios_service,
            None,
        )


def test_predios_por_sector() -> None:
    response = realizar_peticion(
        "/api/estadisticas/predios/sectores"
    )

    assert response.status_code == 200

    datos = response.json()

    assert len(datos) == 2
    assert datos[0]["categoria_id"] == 1
    assert datos[0]["nombre"] == "Sector Central"
    assert datos[0]["cantidad"] == 3
    assert datos[0]["porcentaje"] == "75.00"


def test_predios_por_tipo() -> None:
    response = realizar_peticion(
        "/api/estadisticas/predios/tipos"
    )

    assert response.status_code == 200

    datos = response.json()

    assert len(datos) == 2
    assert datos[0]["categoria_id"] == 1
    assert datos[0]["nombre"] == "Residencial"
    assert datos[0]["cantidad"] == 2
    assert datos[0]["porcentaje"] == "50.00"

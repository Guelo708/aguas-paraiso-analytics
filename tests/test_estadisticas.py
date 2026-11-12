from decimal import Decimal

from fastapi.testclient import TestClient

from app.dependencies import get_estadisticas_service
from app.main import app
from app.schemas.estadisticas import ResumenEstadisticas


class FakeEstadisticasService:
    def obtener_resumen(self) -> ResumenEstadisticas:
        return ResumenEstadisticas(
            total_suscriptores=7,
            total_predios=5,
            total_facturas=12,
            total_pagos=8,
            facturas_pendientes=3,
            facturas_parciales=2,
            facturas_pagadas=6,
            facturas_vencidas=1,
            cartera_pendiente=Decimal("175000.00"),
            recaudo_acumulado=Decimal("420000.00"),
        )


def override_estadisticas_service() -> FakeEstadisticasService:
    return FakeEstadisticasService()


app.dependency_overrides[
    get_estadisticas_service
] = override_estadisticas_service

client = TestClient(app)


def test_obtener_resumen_estadisticas() -> None:
    response = client.get(
        "/api/estadisticas/resumen"
    )

    assert response.status_code == 200
    assert response.json() == {
        "total_suscriptores": 7,
        "total_predios": 5,
        "total_facturas": 12,
        "total_pagos": 8,
        "facturas_pendientes": 3,
        "facturas_parciales": 2,
        "facturas_pagadas": 6,
        "facturas_vencidas": 1,
        "cartera_pendiente": "175000.00",
        "recaudo_acumulado": "420000.00",
    }


def teardown_module() -> None:
    app.dependency_overrides.clear()

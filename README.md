# Aguas Paraíso Analytics

Microservicio headless desarrollado con FastAPI para proporcionar indicadores y estadísticas del acueducto Aguas Paraíso.

## Objetivo

Este microservicio separa las consultas analíticas de las operaciones administrativas del backend principal.

Sus responsabilidades son:

- Consultar PostgreSQL en Neon.
- Ejecutar consultas estadísticas de solo lectura.
- Calcular indicadores financieros y operativos.
- Exponer los resultados mediante una API REST.
- Proporcionar datos al panel administrativo desarrollado en React.

## Tecnologías

- Python 3.14
- FastAPI
- Uvicorn
- SQLAlchemy Core
- Psycopg 3
- Pydantic Settings
- PostgreSQL en Neon
- Pytest
- Docker

## Arquitectura

```text
Frontend React
      |
      | Axios
      v
Microservicio FastAPI
      |
      | Consultas SELECT
      v
PostgreSQL en Neon
```

El backend Spring Boot continúa encargado de las operaciones CRUD y las reglas de negocio.

FastAPI se encarga de las consultas agregadas, indicadores, distribuciones, series mensuales y datos para gráficos.

## Endpoints

### Estado del servicio

```text
GET /health
```

### Resumen general

```text
GET /api/estadisticas/resumen
```

### Facturas por estado

```text
GET /api/estadisticas/facturas/estados
```

### Facturación mensual

```text
GET /api/estadisticas/facturacion/mensual?anio=2026
```

### Recaudo mensual

```text
GET /api/estadisticas/recaudo/mensual?anio=2026
```

### Pagos por método

```text
GET /api/estadisticas/pagos/metodos?anio=2026
```

### Predios por sector

```text
GET /api/estadisticas/predios/sectores
```

### Predios por tipo

```text
GET /api/estadisticas/predios/tipos
```

## Configuración local

### Crear el entorno virtual

```powershell
python -m venv .venv
```

### Activar el entorno

```powershell
.\.venv\Scripts\Activate.ps1
```

No es necesario volver a crear `.venv` si ya existe.

### Instalar las dependencias

```powershell
python -m pip install -r requirements-dev.txt
```

## Variables de entorno

Crea un archivo `.env` en la raíz del proyecto a partir de `.env.example`.

```properties
APP_NAME=Aguas Paraíso Analytics
APP_VERSION=0.1.0
ENVIRONMENT=development

DATABASE_URL=postgresql+psycopg://USUARIO:CONTRASENA@HOST/BASE_DE_DATOS?sslmode=require&channel_binding=require

CORS_ORIGINS=http://localhost:5173
```

El archivo `.env` contiene credenciales y no debe añadirse al repositorio.

## Ejecutar las pruebas

```powershell
python -m compileall app tests
python -m pytest -v
```

## Iniciar el servidor

```powershell
python -m uvicorn app.main:app `
  --reload `
  --reload-dir app
```

El servicio estará disponible en:

```text
http://127.0.0.1:8000
```

## Documentación local

```text
Swagger UI: http://127.0.0.1:8000/docs
ReDoc: http://127.0.0.1:8000/redoc
OpenAPI: http://127.0.0.1:8000/openapi.json
```

## Comprobar la conexión con Neon

```powershell
python -m app.check_database
```

## Docker

Construir la imagen:

```powershell
docker build -t aguas-paraiso-analytics .
```

Ejecutar el contenedor:

```powershell
docker run `
  --env-file .env `
  -p 8000:8000 `
  aguas-paraiso-analytics
```

## Seguridad

Los archivos excluidos del repositorio incluyen:

```text
.env
.venv/
__pycache__/
.pytest_cache/
```

Para producción se recomienda utilizar un usuario de PostgreSQL con permisos exclusivamente de lectura.

## Ramas

```text
main
└── feature/estadisticas
```

El desarrollo estadístico se realiza en `feature/estadisticas` y se fusionará con `main` después de validar las pruebas y el despliegue.
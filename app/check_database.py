from app.database import comprobar_conexion


def main() -> None:
    try:
        resultado = comprobar_conexion()

        print("Conexión establecida correctamente")
        print(f"Base de datos: {resultado['database']}")
        print(f"Usuario: {resultado['user']}")
        print(f"Motor: {resultado['engine']}")
        print("Transacción configurada como solo lectura")
    except Exception as error:
        print("No fue posible conectar con la base de datos")
        print(f"Detalle: {error}")
        raise


if __name__ == "__main__":
    main()

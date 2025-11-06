import os
from meicobaseapi.core.db.db_config import get_db_connection

class crear_tablas_gestion_guias:
    def __init__(self):
        print("Creando tablas FactGuia y FacturasDetalladas...")

        try:
            # Conexión a la base de datos
            conn = get_db_connection(os.getenv("DBNAME_MEISEL_PPAL"))
            cursor = conn.cursor()

            # =======================================================
            # 1. Eliminar tablas si ya existen
            # =======================================================
            cursor.execute("""
            IF OBJECT_ID('dbo.FactGuia', 'U') IS NOT NULL
                DROP TABLE dbo.FactGuia;

            IF OBJECT_ID('dbo.FacturasDetalladas', 'U') IS NOT NULL
                DROP TABLE dbo.FacturasDetalladas;
            """)
            conn.commit()

            # =======================================================
            # 2. Crear tabla FactGuia
            # =======================================================
            cursor.execute("""
            CREATE TABLE dbo.FactGuia (
                idGoAnyWhere VARCHAR(50),
                NumeroGuia INT,
                Transportador VARCHAR(50),
                CodigoCliente VARCHAR(50),
                NombreCliente VARCHAR(100),
                Ciudad VARCHAR(50),
                NumeroFactura INT,
                FechaFactura VARCHAR(50),
                Vendedor VARCHAR(10),
                ValorOriginal DECIMAL(18,2),
                DsctoFinanciero DECIMAL(18,2),
                NuevoDsctoFinanciero DECIMAL(18,2),
                CantidadNotasCredito VARCHAR(100),
                TotalNotasCredito DECIMAL(18,2),
                ValorConsignar DECIMAL(18,2),
                ReporteBrinks DECIMAL(18,2),
                DiferenciaValor DECIMAL(18,2),
                FechaDespachoCompleta DATETIME,
                Observaciones VARCHAR(MAX),
                Cargue VARCHAR(50)
            );
            """)
            conn.commit()

            # =======================================================
            # 3. Crear tabla FacturasDetalladas
            # =======================================================
            cursor.execute("""
            CREATE TABLE dbo.FacturasDetalladas (
                idGoAnyWhere VARCHAR(50),
                NumeroGuia INT,
                Origen VARCHAR(50),
                Transportador VARCHAR(50),
                CodigoCliente VARCHAR(50),
                NombreCliente VARCHAR(100),
                Ciudad VARCHAR(50),
                NumeroFactura INT,
                CantidadNotasCredito VARCHAR(100),
                FechaFactura VARCHAR(50),
                Vendedor VARCHAR(10),
                ValorOriginal DECIMAL(18,2),
                DsctoFinanciero DECIMAL(18,2),
                NuevoDsctoFinanciero DECIMAL(18,2),
                CantidadNotaCredito INT,
                ValorNotaCredito DECIMAL(18,2),
                ListaNotasCredito VARCHAR(MAX),
                TotalNotasCredito DECIMAL(18,2),
                TieneNotaCredito BIT,
                TipoFormaPago VARCHAR(50),
                Bodega VARCHAR(50),
                ValorConsignar DECIMAL(18,2),
                ReporteBrinks DECIMAL(18,2),
                DiferenciaValor DECIMAL(18,2),
                FechaDespachoCompleta DATETIME,
                Observaciones VARCHAR(MAX),
                Cargue VARCHAR(50)
            );
            """)
            conn.commit()

            print("Tablas FactGuia y FacturasDetalladas creadas correctamente.")

        except Exception as e:
            print(f"Error al crear las tablas: {e}")

        finally:
            try:
                cursor.close()
                conn.close()
            except:
                pass

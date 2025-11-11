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
            IF OBJECT_ID('dbo.PlanillaDetalleFactura', 'U') IS NOT NULL
                DROP TABLE dbo.PlanillaDetalleFactura;
                
            IF OBJECT_ID('dbo.Documentos', 'U') IS NOT NULL
                DROP TABLE dbo.Documentos;
                
            IF OBJECT_ID('dbo.PlanillaEncabezado', 'U') IS NOT NULL
                DROP TABLE dbo.PlanillaEncabezado;
                
            IF OBJECT_ID('dbo.PlanillaDetalles', 'U') IS NOT NULL
                DROP TABLE dbo.PlanillaDetalles;
            """)
            conn.commit()

            # =======================================================
            # 2. Crear tabla PlanillaDetalleFactura
            # =======================================================
            cursor.execute("""
                CREATE TABLE dbo.PlanillaDetalleFactura (
                    PlanillaEncId INT,
                    NumeroGuia VARCHAR(255) NULL,
                    NumeroDocumento VARCHAR(50) NULL,
                    TipoDocumento VARCHAR(255) NULL,
                    CodigoCliente VARCHAR(50) NULL,
                    RazonSocialCliente VARCHAR(255) NULL,     
                    ValorFactura DECIMAL(15,4) NULL,
                    DfrFactura DECIMAL(15,4) NULL,
                    NumerosNc DECIMAL(15,4) NULL,
                    ValorNc DECIMAL(15,4) NULL,
                    DfrReal DECIMAL(15,4) NULL,
                    ValorEsperadoRecaudar DECIMAL(15,4) NULL,
                    ValorRecaudado DECIMAL(15,4) NULL,
                    Diferencia DECIMAL(15,4) NULL,
                    Estado VARCHAR(255) NULL,
                    CodigoCondicionPago VARCHAR(255) NULL,
                    NombreCondicionPago VARCHAR(255) NULL,
                );
            """)
            conn.commit()

            # =======================================================
            # 2. Crear tabla Documentos
            # =======================================================
            cursor.execute("""
            CREATE TABLE dbo.Documentos (
                PlanillaEncId INT NULL,
                NumeroGuia VARCHAR(255) NULL,
                NumeroDocumento VARCHAR(50) NULL,
                TipoDocumento VARCHAR(255) NULL,
                ValorDocumento DECIMAL(15,4) NULL,
                FechaDocumento VARCHAR(50) NULL,
                AplicaA VARCHAR(50) NULL,
                BodegaId VARCHAR(50) NULL,
                NombreBodega VARCHAR(255) NULL,
                CodigoCliente VARCHAR(50) NULL,
                NombreCliente VARCHAR(255) NULL,
                CodigoCondicionPago VARCHAR(255) NULL,
                NombreCondicionPago VARCHAR(255) NULL,         
            );

            """)
            conn.commit()
            
            # =======================================================
            # 2. Crear tabla PlanillaEncabezado
            # =======================================================
            cursor.execute("""
            CREATE TABLE dbo.PlanillaEncabezado (
                PlanillaEncId INT IDENTITY(1,1) PRIMARY KEY,
                IdGoAnyWhere VARCHAR(255) NULL,
                FechaCreacionPlanilla DATETIME NULL,
                UsuarioCreacionPlanilla VARCHAR(255) NULL,
                TotalEsperadoRecaudar DECIMAL(18,4) NULL,
                TotalRecaudado DECIMAL(18,4) NULL,
                TotalDiferencia DECIMAL(18,4) NULL,
                CantidadGuiasDespachadas DECIMAL(18,4) NULL,
                CantidadGuiasConfirmadas DECIMAL(18,4) NULL
            );

            """)
            conn.commit()
            
            
            # =======================================================
            # 2. Crear tabla PlanillaDetalles
            # =======================================================
            cursor.execute("""
                CREATE TABLE dbo.PlanillaDetalles (
                    PlanillaEncId INT NULL,
                    NumeroGuia VARCHAR(255) NULL,
                    FechaCreacionGuia VARCHAR(255) NULL,
                    FechaDespachoGuia VARCHAR(255) NULL,
                    TipoGuia VARCHAR(100) NULL,
                    BodegaId VARCHAR(100) NULL,
                    TipoIdPropietarioTransportador VARCHAR(100) NULL,
                    IdPropietarioTransportador VARCHAR(100) NULL,
                    NombrePropietarioTransportador VARCHAR(255) NULL,
                    Placa VARCHAR(50) NULL,
                    TipoIdConductor VARCHAR(100) NULL,
                    ConductorId VARCHAR(100) NULL,
                    NombreConductor VARCHAR(255) NULL,
                    EstadoGuiaOriginal VARCHAR(100) NULL,
                    EstadoGuia VARCHAR(100) NULL,
                    CantidadFacturas DECIMAL(10,4) NULL,
                    FechaPromesa VARCHAR(255) NULL,
                    FechaRetorno VARCHAR(255) NULL,
                    ValorRecaudar DECIMAL(10,4) NULL,
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

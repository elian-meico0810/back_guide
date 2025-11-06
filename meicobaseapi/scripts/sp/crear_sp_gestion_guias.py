import os
from meicobaseapi.core.db.db_config import get_db_connection

class crear_sp_gestion_guias:
    def __init__(self):
        print("Creando procedimiento almacenado SP_GestioGuias_ZZZ...")

        try:
            # Conexión a la base de datos
            conn = get_db_connection(os.getenv("DBNAME_MEISEL_PPAL"))
            cursor = conn.cursor()

            # =======================================================
            # 1. Eliminar SP si ya existe
            # =======================================================
            cursor.execute("""
            IF OBJECT_ID('dbo.SP_GestioGuias_ZZZ', 'P') IS NOT NULL
                DROP PROCEDURE dbo.SP_GestioGuias_ZZZ;
            """)
            conn.commit()

            # =======================================================
            # 2. Crear nuevo SP
            # =======================================================
            cursor.execute("""
                CREATE PROCEDURE [dbo].[SP_GestioGuias_ZZZ]
                    @Fecha VARCHAR(50),
                    @Bodega VARCHAR(50) = NULL,
                    @IidGaw VARCHAR(50) = NULL
                AS
                BEGIN
                    SET NOCOUNT ON;

                    BEGIN TRY
                        BEGIN TRANSACTION;

                        DECLARE @Origen VARCHAR(50);
                        DECLARE @FechaInicio DATETIME = CAST(@Fecha + ' 00:00:00' AS DATETIME);
                        DECLARE @FechaFin DATETIME = CAST(@Fecha + ' 23:59:59' AS DATETIME);

                        -- Determinar origen
                        IF EXISTS (
                            SELECT 1
                            FROM intranet..log_guia_fact lgf
                            INNER JOIN intranet..log_guia lg ON lg.id = lgf.id_guia
                            WHERE lg.fecha_desp BETWEEN @FechaInicio AND @FechaFin
                              AND lgf.cargue IS NULL
                        )
                            SET @Origen = 'Mixta';
                        ELSE
                            SET @Origen = 'TAT';

                        -- CTE para consolidar facturas y descuentos
                        ;WITH FacturasCTE AS (
                            SELECT 
                                lf.id AS NumeroFactura,
                                LTRIM(RTRIM(lf.cod_cliente)) AS CodigoCliente,
                                LTRIM(RTRIM(lf.nom_cliente)) AS NombreCliente,
                                LTRIM(RTRIM(lf.destino)) AS Ciudad,
                                inv.slspsn_no AS Vendedor,
                                inv.tot_dollars AS ValorOriginal,
                                inv.DsctoFinanciero
                            FROM intranet..log_guia lg
                            INNER JOIN intranet..log_guia_fact lgf ON lg.id = lgf.id_guia
                            INNER JOIN intranet..log_factura lf ON lf.id = lgf.id_factura
                            INNER JOIN (
                                SELECT inv_no,
                                       slspsn_no,
                                       tot_dollars,
                                       CONVERT(NUMERIC(18,2), ISNULL(oeohdr.tot_sls_amt,0) * ISNULL(s.ar_terms_dsc_pct,0)/100) AS DsctoFinanciero
                                FROM oehdrhst_sql oeohdr
                                INNER JOIN SYCDEFIL_SQL s ON oeohdr.ar_terms_cd = s.sy_terms_cd
                                WHERE filler_0003 = '(CONTAD EFECTIVO)'
                                UNION
                                SELECT inv_no,
                                       slspsn_no,
                                       tot_dollars,
                                       CONVERT(NUMERIC(18,2), ISNULL(oeord.tot_sls_amt,0) * ISNULL(sy.ar_terms_dsc_pct,0)/100) AS DsctoFinanciero
                                FROM oeordhdr_sql oeord
                                INNER JOIN SYCDEFIL_SQL sy ON oeord.ar_terms_cd = sy.sy_terms_cd
                                WHERE filler_0003 = '(CONTAD EFECTIVO)' AND oeord.status = '9'
                            ) inv ON inv.inv_no = lf.id
                            WHERE lg.fecha_desp BETWEEN @FechaInicio AND @FechaFin
                        )

                        -- Insertar en FactGuia
                        INSERT INTO dbo.FactGuia (
                            NumeroGuia, Transportador, CodigoCliente, NombreCliente, Ciudad,
                            NumeroFactura, FechaFactura, Vendedor, ValorOriginal, DsctoFinanciero,
                            NuevoDsctoFinanciero, CantidadNotasCredito, TotalNotasCredito, ValorConsignar,
                            ReporteBrinks, DiferenciaValor, FechaDespachoCompleta, Observaciones, Cargue, idGoAnyWhere
                        )
                        SELECT 
                            lg.id AS NumeroGuia,
                            LTRIM(RTRIM(lg.propietario)) AS Transportador,
                            f.CodigoCliente,
                            f.NombreCliente,
                            f.Ciudad,
                            f.NumeroFactura,
                            ISNULL(lf.fecha, 0) AS FechaFactura,
                            f.Vendedor,
                            f.ValorOriginal,
                            f.DsctoFinanciero,
                            0 AS NuevoDsctoFinanciero,
                            0 AS CantidadNotasCredito,
                            0 AS TotalNotasCredito,
                            0 AS ValorConsignar,
                            0 AS ReporteBrinks,
                            0 AS DiferenciaValor,
                            lg.fecha_desp AS FechaDespachoCompleta,
                            '' AS Observaciones,
                            lgf.Cargue,
                            @IidGaw
                        FROM intranet..log_guia lg
                        INNER JOIN intranet..log_guia_fact lgf ON lg.id = lgf.id_guia
                        INNER JOIN intranet..log_factura lf ON lf.id = lgf.id_factura
                        INNER JOIN FacturasCTE f ON f.NumeroFactura = lf.id;

                        -- Insertar en FacturasDetalladas (simplificado, similar al FactGuia)
                        INSERT INTO dbo.FacturasDetalladas (
                            Origen, NumeroGuia, Transportador, CodigoCliente, NombreCliente, Ciudad,
                            NumeroFactura, FechaFactura, Vendedor, ValorOriginal, DsctoFinanciero,
                            NuevoDsctoFinanciero, CantidadNotasCredito, TotalNotasCredito, ListaNotasCredito,
                            TieneNotaCredito, TipoFormaPago, Bodega, ValorConsignar, ReporteBrinks,
                            DiferenciaValor, FechaDespachoCompleta, Observaciones, Cargue, idGoAnyWhere
                        )
                        SELECT 
                            @Origen,
                            f.NumeroGuia, f.Transportador, f.CodigoCliente, f.NombreCliente, f.Ciudad,
                            f.NumeroFactura, f.FechaFactura, f.Vendedor, f.ValorOriginal, f.DsctoFinanciero,
                            0, 0, 0, '', 0, 'CE', @Bodega, 0, 0, 0, f.FechaDespachoCompleta, '', lgf.Cargue,  @IidGaw
                        FROM dbo.FactGuia f
                        INNER JOIN intranet..log_guia_fact lgf ON f.NumeroGuia = lgf.id_guia;

                        COMMIT TRANSACTION;

                        SELECT CAST(1 AS INT) AS Resultado;

                    END TRY
                    BEGIN CATCH
                        IF @@TRANCOUNT > 0 ROLLBACK TRANSACTION;

                        DECLARE @ErrMsg NVARCHAR(4000) = ERROR_MESSAGE();
                        DECLARE @ErrLine INT = ERROR_LINE();
                        PRINT 'Error en SP_GestioGuias_ZZZ: ' + @ErrMsg + ' (línea ' + CAST(@ErrLine AS NVARCHAR(10)) + ')';

                        SELECT CAST(0 AS INT) AS Resultado;
                        THROW;
                    END CATCH
                END

            """)
            conn.commit()
           # =======================================================

            print(" Procedimiento SP_GestioGuias_ZZZ creado correctamente.")

        except Exception as e:
            print(f" Error al crear el SP SP_GestioGuias_ZZZ: {e}")

        finally:
            try:
                cursor.close()
                conn.close()
            except:
                pass

import os
from meicobaseapi.core.db.db_config import get_db_connection

class crear_sp_gestion_guias:
    def __init__(self):
        print("Creando procedimiento almacenado SP_GestinGuias_ZZZ...")

        try:
            # Conexión a la base de datos
            conn = get_db_connection(os.getenv("DBNAME_MEISEL_PPAL"))
            cursor = conn.cursor()

            # =======================================================
            # 1. Eliminar SP si ya existe
            # =======================================================
            cursor.execute("""
            IF OBJECT_ID('dbo.SP_GestionGuias_ZZZ', 'P') IS NOT NULL
                DROP PROCEDURE dbo.SP_GestionGuias_ZZZ;
            """)
            conn.commit()

            # =======================================================
            # 2. Crear nuevo SP
            # =======================================================
            cursor.execute("""
                CREATE PROCEDURE [dbo].[SP_GestionGuias_ZZZ]
                    @Fecha VARCHAR(50),
                    @Bodega VARCHAR(50) = NULL,
                    @IidGaw VARCHAR(50) = NULL
                AS
                BEGIN
                    SET NOCOUNT ON;

                    BEGIN TRY
                        BEGIN TRANSACTION;

                 		DECLARE @Origen VARCHAR(50);
                        DECLARE @FechaInicio DATETIME       = CAST(@Fecha + ' 00:00:00' AS DATETIME);
                        DECLARE @FechaFin DATETIME          = CAST(@Fecha + ' 23:59:59' AS DATETIME);
                        DECLARE @FechaEnteraInicio  int     = CONVERT(INT, CONVERT(CHAR(8), DATEADD(DAY, -30, CAST(@Fecha AS DATE)), 112))
                        DECLARE @FechaEnteraFin     int     = CONVERT(INT, CONVERT(CHAR(8), CAST(@Fecha AS DATE), 112)) 
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

                        --  Limpiar datos previos del mismo @IidGaw
                        DELETE FROM dbo.FactGuia WHERE idGoAnyWhere = @IidGaw;
                        DELETE FROM dbo.FacturasDetalladas WHERE idGoAnyWhere = @IidGaw;

                        --  Insertar FactGuia (ahora tabla física)
                        INSERT INTO dbo.FactGuia (
                            idGoAnyWhere, NumeroGuia, Transportador, CodigoCliente, NombreCliente, Ciudad,
                            NumeroFactura, FechaFactura, Vendedor, ValorOriginal, DsctoFinanciero,
                            NuevoDsctoFinanciero, CantidadNotasCredito, TotalNotasCredito, ValorConsignar,
                            ReporteBrinks, DiferenciaValor, FechaDespachoCompleta, Observaciones, Cargue
                        )
                        SELECT
                            @IidGaw,
                            lg.id AS NumeroGuia,
                            LTRIM(RTRIM(lg.propietario)) AS Transportador,
                            LTRIM(RTRIM(lf.cod_cliente)) AS CodigoCliente,
                            LTRIM(RTRIM(lf.nom_cliente)) AS NombreCliente,
                            LTRIM(RTRIM(lf.destino)) AS Ciudad,
                            lf.id AS NumeroFactura,
                            ISNULL(lf.fecha, 0) AS FechaFactura,
                            LTRIM(RTRIM(facturas.slspsn_no)) AS Vendedor,
                            facturas.tot_dollars AS ValorOriginal,
                            facturas.DsctoFinanciero,
                            0 AS NuevoDsctoFinanciero,
                            0 AS CantidadNotasCredito,
                            0 AS TotalNotasCredito,
                            0 AS ValorConsignar,
                            0 AS ReporteBrinks,
                            0 AS DiferenciaValor,
                            lg.fecha_desp AS FechaDespachoCompleta,
                            '' AS Observaciones,
                            lgf.Cargue
                        FROM intranet..log_guia lg WITH (NOLOCK)
                        INNER JOIN intranet..log_guia_fact lgf WITH (NOLOCK) ON lg.id = lgf.id_guia
                        INNER JOIN intranet..log_Factura lf WITH (NOLOCK) ON lf.id = lgf.id_factura
                        INNER JOIN (
                            SELECT 
                                inv_no,
                                slspsn_no,
                                tot_dollars,
                                CONVERT(NUMERIC(18,2),
                                    (ISNULL(oeohdr.tot_sls_amt,0) * ISNULL(s.ar_terms_dsc_pct,0)) / 100
                                ) AS DsctoFinanciero
                            FROM oehdrhst_Sql oeohdr WITH (NOLOCK)
                            INNER JOIN SYCDEFIL_SQL s WITH (NOLOCK)
                                ON oeohdr.ar_terms_cd = s.sy_terms_cd
                            WHERE filler_0003 = '(CONTAD EFECTIVO)'
                			And   oeohdr.Orig_Ord_Type In ('I', 'O')--I: TAT; O: Mayorista
                           	And   oeohdr.Mfg_Loc = @Bodega
                            And   oeohdr.Inv_dt <= @FechaEnteraFin
                            And   oeohdr.Inv_dt >= @FechaEnteraInicio
                            UNION ALL

                            SELECT 
                                inv_no,
                                slspsn_no,
                                tot_dollars,
                                CONVERT(NUMERIC(18,2),
                                    (ISNULL(oeord.tot_sls_amt,0) * ISNULL(sy.ar_terms_dsc_pct,0)) / 100
                                ) AS DsctoFinanciero
                            FROM oeordhdr_sql oeord WITH (NOLOCK)
                            INNER JOIN SYCDEFIL_SQL sy WITH (NOLOCK)
                                ON oeord.ar_terms_cd = sy.sy_terms_cd
                            WHERE filler_0003 = '(CONTAD EFECTIVO)'
                              AND oeord.status = '9'
                              And   oeord.Ord_Type In ('I', 'O')
                              And   oeord.Mfg_Loc = @Bodega
                              And   oeord.Inv_dt <= @FechaEnteraFin
                              And   oeord.Inv_dt >= @FechaEnteraInicio

                        ) facturas ON facturas.inv_no = lf.id
                       	WHERE lg.fecha_desp BETWEEN @FechaInicio AND @FechaFin
                                			And lg.Bodega = @Bodega

                        --  Insertar FacturasDetalladas (tabla física)
                        INSERT INTO dbo.FacturasDetalladas (
                            Origen, NumeroGuia, Transportador, CodigoCliente, NombreCliente, Ciudad,
                            NumeroFactura, FechaFactura, Vendedor, ValorOriginal, DsctoFinanciero,
                            NuevoDsctoFinanciero, CantidadNotasCredito, TotalNotasCredito, ListaNotasCredito,
                            TieneNotaCredito, TipoFormaPago, Bodega, ValorConsignar, ReporteBrinks,
                            DiferenciaValor, FechaDespachoCompleta, Observaciones, Cargue, idGoAnyWhere
                        )
                        SELECT 
                            @Origen,
                            f.NumeroGuia,
                            f.Transportador,
                            f.CodigoCliente,
                            f.NombreCliente,
                            f.Ciudad,
                            f.NumeroFactura,
                            f.FechaFactura,
                            f.Vendedor,
                            f.ValorOriginal,
                            f.DsctoFinanciero,
                            f.NuevoDsctoFinanciero,
                            q2.CantidadNotaCredito,
                            q2.ValorNotaCredito,
                            q2.ListaNotasCredito,
                            q2.TieneNotaCredito,
                            q2.TipoFormaPago,
                            q2.Bodega,
                            f.ValorConsignar,
                            f.ReporteBrinks,
                            f.DiferenciaValor,
                            f.FechaDespachoCompleta,
                            f.Observaciones,
                            f.Cargue,
                            @IidGaw
                        FROM dbo.FactGuia f
                        INNER JOIN (
                            SELECT 
                                inv_no AS NumeroFactura,
                                inv_dt AS FechaFactura,
                                CONVERT(datetime, CONVERT(nvarchar(8), inv_dt)) AS FechaFacturaCompleta,
                                ar_terms_Cd AS CondicionPago,
                                cus_no AS CodigoCliente,
                                bill_to_name AS NombreCliente,
                                tot_dollars AS TotalFactura,
                				CASE WHEN a.CantidadNotasCredito IS NOT NULL THEN 1 ELSE 0 END AS TieneNotaCredito,
                                ISNULL(a.CantidadNotasCredito,0) AS CantidadNotaCredito,
                                ISNULL(a.ValorNotasCredito,0) AS ValorNotaCredito,
                                (((CONVERT(NUMERIC(18,2), ISNULL(tot_sls_amt,0)) + ISNULL(a.ValorBaseNotasCredito,0)) * ar_terms_dsc_pct)/100) AS DescuentoFinanciero,
                                slspsn_no AS CodigoVendedor,
                                'CE' AS TipoFormaPago,
                                mfg_loc AS Bodega,
                                a.ListaNotasCredito
                            FROM oehdrhst_Sql o WITH (NOLOCK)
                            INNER JOIN SYCDEFIL_SQL s WITH (NOLOCK)
                                ON o.ar_terms_cd = s.sy_terms_cd
                            LEFT JOIN (
                                SELECT 
                                    NC.apply_to_no,
                                    COUNT(NC.apply_to_no) AS CantidadNotasCredito,
                                    SUM(NC.amt_1) AS ValorBaseNotasCredito,
                                    SUM(NC.amt_1 + NC.amt_2) AS ValorNotasCredito,
                                    (
                                        SELECT STUFF((
                                            SELECT '/' + LTRIM(RTRIM(nc2.doc_no))
                                            FROM aropnfil_sql nc2 WITH (NOLOCK)
                                            WHERE nc2.apply_to_no = NC.apply_to_no
                                              AND nc2.doc_type = 'C'
                                            FOR XML PATH(''), TYPE
                                        ).value('.', 'NVARCHAR(MAX)'), 1, 1, '')
                                    ) AS ListaNotasCredito
                                FROM aropnfil_sql NC WITH (NOLOCK)
                                WHERE NC.doc_type = 'C'
                                GROUP BY NC.apply_to_no
                            ) AS a ON o.inv_no = a.apply_to_no
                            WHERE filler_0003 = '(CONTAD EFECTIVO)'

                            UNION ALL

                            SELECT 
                                inv_no AS NumeroFactura,
                                inv_dt AS FechaFactura,
                                CONVERT(datetime, CONVERT(nvarchar(8), inv_dt)) AS FechaFacturaCompleta,
                                ar_terms_Cd AS CondicionPago,
                                cus_no AS CodigoCliente,
                                bill_to_name AS NombreCliente,
                                tot_dollars AS TotalFactura,
                				CASE WHEN a.CantidadNotasCredito IS NOT NULL THEN 1 ELSE 0 END AS TieneNotaCredito,
                                ISNULL(a.CantidadNotasCredito,0) AS CantidadNotaCredito,
                                ISNULL(a.ValorNotasCredito,0) AS ValorNotaCredito,
                                (((CONVERT(NUMERIC(18,2), ISNULL(tot_sls_amt,0)) + ISNULL(a.ValorBaseNotasCredito,0)) * ar_terms_dsc_pct)/100) AS DescuentoFinanciero,
                                slspsn_no AS CodigoVendedor,
                                'CE' AS TipoFormaPago,
                                mfg_loc AS Bodega,
                                a.ListaNotasCredito
                            FROM oeordhdr_sql o WITH (NOLOCK)
                            INNER JOIN SYCDEFIL_SQL s WITH (NOLOCK)
                                ON o.ar_terms_cd = s.sy_terms_cd
                            LEFT JOIN (
                                SELECT 
                                    NC.apply_to_no,
                                    COUNT(NC.apply_to_no) AS CantidadNotasCredito,
                                    SUM(NC.amt_1) AS ValorBaseNotasCredito,
                                    SUM(NC.amt_1 + NC.amt_2) AS ValorNotasCredito,
                                    (
                                        SELECT STUFF((
                                            SELECT '/' + LTRIM(RTRIM(nc2.doc_no))
                                            FROM aropnfil_sql nc2 WITH (NOLOCK)
                                            WHERE nc2.apply_to_no = NC.apply_to_no
                                              AND nc2.doc_type = 'C'
                                            FOR XML PATH(''), TYPE
                                        ).value('.', 'NVARCHAR(MAX)'), 1, 1, '')
                                    ) AS ListaNotasCredito
                                FROM aropnfil_sql NC WITH (NOLOCK)
                                WHERE NC.doc_type = 'C'
                                GROUP BY NC.apply_to_no
                            ) AS a ON o.inv_no = a.apply_to_no
                            WHERE filler_0003 = '(CONTAD EFECTIVO)' AND o.status = '9'
                        ) q2 ON f.NumeroFactura = q2.NumeroFactura;

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

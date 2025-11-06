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
                @Fecha VARCHAR(50)
            AS
            BEGIN
                SET NOCOUNT ON;
            
                BEGIN TRY
                    BEGIN TRANSACTION;
            
                    DECLARE @Origen VARCHAR(50);
            
                    -- Identificar si una guía es mixta o solo TAT
            SET @Origen = (
                SELECT
                    CASE
                        WHEN COUNT(CASE WHEN cargue IS NULL THEN 1 END) > 0 THEN 'Mixta'
                        ELSE 'TAT'
                    END
                FROM intranet..log_guia_fact WITH (NOLOCK)
            );
                    -- Limpiar las tablas permanentes antes de insertar
                    TRUNCATE TABLE dbo.FactGuia;
                    TRUNCATE TABLE dbo.FacturasDetalladas;
            
                    -- Insertar en FactGuia
                    INSERT INTO dbo.FactGuia (
                        NumeroGuia,
                        Transportador,
                        CodigoCliente,
                        NombreCliente,
                        Ciudad,
                        NumeroFactura,
                        FechaFactura,
                        Vendedor,
                        ValorOriginal,
                        DsctoFinanciero,
                        NuevoDsctoFinanciero,
                        CantidadNotasCredito,
                        TotalNotasCredito,
                        ValorConsignar,
                        ReporteBrinks,
                        DiferenciaValor,
                        FechaDespachoCompleta,
                        Observaciones,
                        Cargue
                    )
                    SELECT TOP 3 -- Solo los 3 primeros como ejemplo
                        lg.id NumeroGuia,
                        LTRIM(RTRIM(lg.propietario)) Transportador,
                        LTRIM(RTRIM(lf.cod_cliente)) CodigoCliente,
                        LTRIM(RTRIM(lf.nom_cliente)) NombreCliente,
                        LTRIM(RTRIM(lf.destino)) Ciudad,
                        lf.id NumeroFactura,
                        ISNULL(lf.fecha,0) FechaFactura,
                        LTRIM(RTRIM(facturas.slspsn_no)) Vendedor,
                        facturas.tot_dollars ValorOriginal,
                        facturas.DsctoFinanciero DsctoFinanciero,
                        0 NuevoDsctoFinanciero,
                        0 CantidadNotasCredito,
                        0 TotalNotasCredito,
                        0 ValorConsignar,
                        0 ReporteBrinks,
                        0 DiferenciaValor,
                        lg.fecha_desp FechaDespachoCompleta,
                        '' Observaciones,
                        lgf.Cargue
                    FROM intranet..log_guia lg WITH (NOLOCK)
                    INNER JOIN intranet..log_guia_fact lgf WITH (NOLOCK) ON lg.id = lgf.id_guia
                    INNER JOIN intranet..log_Factura lf WITH (NOLOCK) ON lf.id = lgf.id_factura
                    INNER JOIN (
                        SELECT 
                            inv_no, slspsn_no, tot_dollars,
                            CONVERT(NUMERIC(18,2),(ISNULL(oeohdr.tot_sls_amt,0) * ISNULL(s.ar_terms_dsc_pct,0))/100) DsctoFinanciero
                        FROM oehdrhst_Sql oeohdr WITH (NOLOCK)
                        INNER JOIN SYCDEFIL_SQL s WITH (NOLOCK) ON oeohdr.ar_terms_cd = s.sy_terms_cd
                        WHERE filler_0003 ='(CONTAD EFECTIVO)'
                        UNION
                        SELECT 
                            inv_no, slspsn_no, tot_dollars,
                            CONVERT(NUMERIC(18,2),(ISNULL(oeord.tot_sls_amt,0) * ISNULL(sy.ar_terms_dsc_pct,0))/100) DsctoFinanciero
                        FROM oeordhdr_sql oeord WITH (NOLOCK)
                        INNER JOIN SYCDEFIL_SQL sy WITH (NOLOCK) ON oeord.ar_terms_cd = sy.sy_terms_cd
                        WHERE filler_0003 ='(CONTAD EFECTIVO)' AND oeord.status = '9'
                    ) facturas ON facturas.inv_no = lf.id
                    WHERE lg.fecha_desp BETWEEN CAST(CONCAT(@Fecha,' 00:00:00') AS DATETIME)
                                            AND CAST(CONCAT(@Fecha,' 23:59:59') AS DATETIME);
            
            
                                -- Insertar en FacturasDetalladas
                                INSERT INTO dbo.FacturasDetalladas (
                                    Origen,
                                    NumeroGuia,
                                    Transportador,
                                    CodigoCliente,
                                    NombreCliente,
                                    Ciudad,
                                    NumeroFactura,
                                    FechaFactura,
                                    Vendedor,
                                    ValorOriginal,
                                    DsctoFinanciero,
                                    NuevoDsctoFinanciero,
                                    CantidadNotasCredito,
                                    TotalNotasCredito,
                                    ListaNotasCredito,
                                    TieneNotaCredito,
                                    TipoFormaPago,
                                    Bodega,
                                    ValorConsignar,
                                    ReporteBrinks,
                                    DiferenciaValor,
                                    FechaDespachoCompleta,
                                    Observaciones,
                                    Cargue
                                )
                                SELECT 
                                    @Origen Origen,
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
                                    f.Cargue
                                FROM dbo.FactGuia f
                               INNER JOIN (select inv_no NumeroFactura
                        					 , inv_dt FechaFactura  
                                             , CONVERT(datetime, convert(nvarchar(8), inv_dt)) FechaFacturaCompleta  
                                             , ar_terms_Cd CondicionPago, LTRIM(RTRIM(ar_terms_Cd)) + ' ' + LTRIM(RTRIM(s.filler_0003)) CondicionPagoConcatenado  
                                             , cus_no CodigoCliente
                        					 , bill_to_name NombreCliente
                        					 , tot_dollars TotalFactura  
                                             , CASE WHEN a.CantidadNotasCredito IS NOT NULL THEN 1 
                                                    ELSE 0 
                                                    END TieneNotaCredito  
                                             , ISNULL(a.CantidadNotasCredito,0) CantidadNotaCredito
                        					 , ISNULL(a.ValorNotasCredito,0) ValorNotaCredito  
                                            , (((convert(numeric(18,2),(isnull(tot_sls_amt,0))) + ISNULL(a.ValorBaseNotasCredito,0))* ar_terms_dsc_pct)/100) DescuentoFinanciero  
                        					, slspsn_no CodigoVendedor  
                                             , 'CE' TipoFormaPago  
                                             , mfg_loc Bodega  
                        					 ,a.ListaNotasCredito
                                             from oehdrhst_Sql o with (nolock) -- HISTORICAS MACOLA
                        					 inner join SYCDEFIL_SQL s with (nolock) on o.ar_terms_cd = s.sy_terms_cd  
                                             left join ( 
                        								 select NC.apply_to_no, COUNT(NC.apply_to_no) CantidadNotasCredito 
                        								 , sum(NC.amt_1) ValorBaseNotasCredito  
                        								 , sum(NC.amt_1+ NC.amt_2) ValorNotasCredito  
                        								 ,(
                        										SELECT STUFF((
                        											SELECT '/' + LTRIM(RTRIM(nc2.doc_no))
                        											FROM aropnfil_sql nc2 with (nolock)
                        											WHERE nc2.apply_to_no = NC.apply_to_no
                        											  AND nc2.doc_type = 'C'
                        											FOR XML PATH(''), TYPE
                        										).value('.', 'NVARCHAR(MAX)'), 1, 1, '')
                        									) AS ListaNotasCredito
                        								 from aropnfil_sql  NC with (nolock)
                        								 where 
                        								 NC.doc_type = 'C'   
                        								 group by NC.apply_to_no  
                        					) as a on o.inv_no = a.apply_to_no  
            
                                             where filler_0003 ='(CONTAD EFECTIVO)'   --La factura debe ser contado efectivo
            
                                             union   
                                             select 
                        					 inv_no NumeroFactura
                        					 , inv_dt FechaFactura  
                                             , CONVERT(datetime, convert(nvarchar(8), inv_dt)) FechaFacturaCompleta  
                                             , ar_terms_Cd CondicionPago, LTRIM(RTRIM(ar_terms_Cd)) + ' ' + LTRIM(RTRIM(s.filler_0003)) CondicionPagoConcatenado  
                                             , cus_no CodigoCliente, bill_to_name NombreCliente, tot_dollars TotalFactura  
                                             , CASE WHEN a.CantidadNotasCredito IS NOT NULL THEN 'SI'  
                        							ELSE 'NO'  
                        						 END TieneNotaCredito  
                                             , ISNULL(a.CantidadNotasCredito,0) CantidadNotaCredito, ISNULL(a.ValorNotasCredito,0) ValorNotaCredito  
                                             , (((convert(numeric(18,2),(isnull(tot_sls_amt,0))) + ISNULL(a.ValorBaseNotasCredito,0))* ar_terms_dsc_pct)/100) DescuentoFinanciero  
                                             , slspsn_no CodigoVendedor  
                                             , 'CE' TipoFormaPago  
                                             , mfg_loc Bodega  
                        					 ,a.ListaNotasCredito
                                             from oeordhdr_sql o with (nolock) inner join SYCDEFIL_SQL s  with (nolock)-- FACTURACION MACOLA
                                             on o.ar_terms_cd = s.sy_terms_cd  
                                             left join ( 
                        								 select NC.apply_to_no, COUNT(NC.apply_to_no) CantidadNotasCredito 
                        								 , sum(NC.amt_1) ValorBaseNotasCredito  
                        								 , sum(NC.amt_1+ NC.amt_2) ValorNotasCredito  
                        								 ,(
                        										SELECT STUFF((
                        											SELECT '/' + LTRIM(RTRIM(nc2.doc_no))
                        											FROM aropnfil_sql nc2 with (nolock)
                        											WHERE nc2.apply_to_no = NC.apply_to_no
                        											  AND nc2.doc_type = 'C'
                        											FOR XML PATH(''), TYPE
                        										).value('.', 'NVARCHAR(MAX)'), 1, 1, '')
                        									) AS ListaNotasCredito
                        								 from aropnfil_sql  NC with (nolock)
                        								 where 
                        								 NC.doc_type = 'C'   
                        								 group by NC.apply_to_no  
                        					) as a on o.inv_no = a.apply_to_no  
                                             where filler_0003 ='(CONTAD EFECTIVO)'  --La factura debe ser contado efectivo
                                             and O.status = '9'  
                        					 ) q2 ON f.NumeroFactura = q2.NumeroFactura
            
                                SELECT 
                        			Origen,
                                    NumeroGuia,
                                    Transportador,
                                    '' CodigoCliente,
                                    '' NombreCliente,
                                    '' Ciudad,
                        			0 NumeroFactura,
                                    Cargue,
                        			'' Vendedor,
                                    ISNULL(Max(CantidadNotaCredito),0) AS CantidadNotaCredito,
                                    ISNULL(SUM(ValorOriginal),0) AS ValorOriginal,
                                    ISNULL(SUM(ValorNotaCredito),0) AS TotalNotasCredito,
                                    ISNULL(SUM(DsctoFinanciero),0) AS DsctoFinanciero,
                        			ISNULL(SUM(ValorConsignar),0) AS ValorConsignar,
                        			0 ReporteBrinks,
                        			0 NotaCreditoLogistica,
                        			0 ConsignacionRuta,
                        			0 ConsignacionQR,
                                    0 DiferenciaValor,
                        			ISNULL(STUFF((
                        					SELECT '/ ' + d.ListaNotasCredito
                        					FROM dbo.FacturasDetalladas d
                        					WHERE d.Cargue = f.Cargue 
                        					  AND d.NumeroGuia = f.NumeroGuia
                        					  AND d.Transportador = f.Transportador
                        					FOR XML PATH(''), TYPE).value('.', 'NVARCHAR(MAX)'), 1, 2, ''
                        					),'') AS ListaNotasCreditos,
                        		0 AS FechaFactura,
                        		0 NuevoDsctoFinanciero
                                FROM dbo.FacturasDetalladas f
                                WHERE Cargue IS NOT NULL
                                GROUP BY Origen,NumeroGuia, Transportador, Cargue,FechaFactura
            
                                UNION ALL
            
                                SELECT 
                        			Origen,
                                    NumeroGuia,
                                    Transportador,
                                    CodigoCliente,
                                    NombreCliente,
                                    Ciudad,
                        			NumeroFactura,
                                    '' AS Cargue,
                        			Vendedor,
                                    ISNULL(CantidadNotaCredito,0),
                                    ISNULL(ValorOriginal,0),
                                    ISNULL(ValorNotaCredito*-1,0) AS TotalNotasCredito,
                        			--ISNULL(100000,0) AS TotalNotasCredito,
                                    ISNULL(DsctoFinanciero*-1,0),
                        			--ISNULL(10000,0),
                        			ISNULL(ValorConsignar,0),
                        			0 ReporteBrinks,
                        			0 NotaCreditoLogistica,
                        			0 ConsignacionRuta,
                        			0 ConsignacionQR,
                                    0 DiferenciaValor,
                        			ISNULL(ListaNotasCredito,''),
                        			FechaFactura,
                        			0 NuevoDsctoFinanciero
                                FROM dbo.FacturasDetalladas
                                WHERE Cargue IS NULL;
            
                                COMMIT TRANSACTION;
                            END TRY
                            BEGIN CATCH
                                IF @@TRANCOUNT > 0
                        		            ROLLBACK TRANSACTION;
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

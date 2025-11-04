import os
from meicobaseapi.core.db.db_config import get_db_connection

class INFO_GUIA_ZZZ_VIEW:
    def __init__(self):
        print("Creando vista INFO_GUIA_ZZZ_VIEW...")

        try:
            # Nos conectamos a la base donde queremos crear la vista (por ejemplo MEISEL_PPAL)
            conn = get_db_connection(os.getenv("DBNAME_MEISEL_PPAL"))
            cursor = conn.cursor()

            # Eliminar la vista si ya existe
            cursor.execute("""
            IF OBJECT_ID('dbo.INFO_GUIA_ZZZ_VIEW', 'V') IS NOT NULL
                DROP VIEW dbo.INFO_GUIA_ZZZ_VIEW;
            """)
            conn.commit()

            # Crear la nueva vista
            cursor.execute("""
            CREATE VIEW dbo.INFO_GUIA_ZZZ_VIEW AS
            SELECT
                ord.inv_no,
                lg_gc.id_factura,
                lg_gc.id_guia,
                lg_f.cod_cliente,
                lg_f.nom_cliente,
                lg_f.dir_cliente,
                lg_f.destino,
                lg_f.estado,
                lg_f.ccosto,
                lg_f.fecha,
                lg_f.orden
            FROM Intranet.dbo.log_guia AS lg_g
            INNER JOIN Intranet.dbo.log_guia_fact AS lg_gc 
                ON lg_gc.id_guia = lg_g.id
            INNER JOIN Intranet.dbo.log_factura AS lg_f 
                ON lg_f.id = lg_gc.id_factura
            INNER JOIN MEISEL_PPAL.dbo.OeOrdHdr_Sql AS ord
                ON ord.inv_no = lg_gc.id_factura
            WHERE ord.ord_type IN ('I', 'O', 'C');
            """)
            conn.commit()

            print("INFO_GUIA_ZZZ_VIEW creada correctamente.")

        except Exception as e:
            print(f"Error al crear la vista INFO_GUIA_ZZZ_VIEW: {e}")

        finally:
            try:
                cursor.close()
                conn.close()
            except:
                pass

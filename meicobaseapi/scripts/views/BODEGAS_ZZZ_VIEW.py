import os
from meicobaseapi.core.db.db_config import get_db_connection

class BODEGAS_ZZZ_VIEW:
    def __init__(self):
        print("Seeding BODEGAS_ZZZ_VIEW...")

        try:
            conn = get_db_connection(os.getenv("DBNAME_MEISEL_PPAL"))
            cursor = conn.cursor()

            # Eliminar vista si existe
            cursor.execute("""
            IF OBJECT_ID('dbo.BODEGAS_ZZZ_VIEW', 'V') IS NOT NULL
                DROP VIEW dbo.BODEGAS_ZZZ_VIEW;
            """)
            conn.commit()

            # Crear vista con el esquema correcto
            cursor.execute("""
            CREATE VIEW dbo.BODEGAS_ZZZ_VIEW AS
            SELECT 
                loc_desc, 
                city, 
                addr_1, 
                addr_2
            FROM dbo.IMLOCFIL_SQL  
            WHERE phone_ext_1 = 'DISP';
            """)
            conn.commit()

            print("BODEGAS_ZZZ_VIEW -- Executed! Vista creada correctamente.")

        except Exception as e:
            print(f"Error al crear la vista: {e}")

        finally:
            try:
                cursor.close()
                conn.close()
            except:
                pass

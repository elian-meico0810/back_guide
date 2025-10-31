import os
import pyodbc

def get_db_connection():
    try:
        """
            Devuelve una conexión a SQL Server usando variables de entorno.
            Se puede usar desde cualquier módulo del proyecto.
        """
        server = os.getenv("DBHOST")
        database = os.getenv("DBNAME_MEISEL_PPAL")
        username = os.getenv("DBUSER")
        password = os.getenv("DBPASSWORD")

        if not all([server, database, username, password]):
            raise ValueError("❌ Faltan variables de entorno para la conexión a la base de datos.")

        conn = pyodbc.connect(
            f"DRIVER={{ODBC Driver 17 for SQL Server}};"
            f"SERVER={server};"
            f"DATABASE={database};"
            f"UID={username};"
            f"PWD={password};"
        )
        return conn
    except Exception as e:
        raise e
    

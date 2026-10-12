
import os
import psycopg
from dotenv import load_dotenv

load_dotenv()

try:
    with psycopg.connect(
        host=os.getenv("DB_HOST"),
        port=os.getenv("DB_PORT"),
        dbname=os.getenv("TEST_DB_NAME"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        connect_timeout=5
    ) as conexion:

        print("CONEXION EXITOSA A POSTGRESQL")
        print("Base:", conexion.info.dbname)

except Exception as error:
    print("ERROR DE CONEXION:")
    print(type(error).__name__)
    print(str(error))
payt
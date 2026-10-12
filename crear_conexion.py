from sqlalchemy import text
from database import engine

with engine.connect() as conexion:
    resultado = conexion.execute(
        text("SELECT current_database(), current_user")
    )
    print("Conexión exitosa:", resultado.fetchone())
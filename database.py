
import os

from dotenv import load_dotenv
from sqlalchemy import create_engine, URL, text
from sqlalchemy.orm import DeclarativeBase, sessionmaker

# Leer el archivo .env
load_dotenv()

# Construir la conexión con PostgreSQL
DATABASE_URL = URL.create(
    drivername="postgresql+psycopg",
    username=os.getenv("DB_USER"),
    password=os.getenv("DB_PASSWORD"),
    host=os.getenv("DB_HOST", "localhost"),
    port=int(os.getenv("DB_PORT", "5432")),
    database=os.getenv("DB_NAME")
)

# Motor de conexión
engine = create_engine(
    DATABASE_URL,
    pool_pre_ping=True
)

# Fábrica de sesiones
SessionLocal = sessionmaker(
    bind=engine,
    autoflush=False,
    expire_on_commit=False
)

# Clase base para los modelos ORM
class Base(DeclarativeBase):
    pass


# Dependencia para obtener una sesión
def get_db():
    with SessionLocal() as db:
        yield db


import os
import uuid

from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.engine import URL
from sqlalchemy.orm import Session

from database import Base
from entidades.paciente import Paciente
from entidades.observacion import Observacion
from repositorios.observacion_repository import (
    ObservacionRepository
)

load_dotenv()


def test_guardar_y_buscar_observacion():

    assert os.getenv("TEST_DB_NAME") == "curso_fastapi_test"

    url = URL.create(
        drivername="postgresql+psycopg",
        username=os.environ["DB_USER"],
        password=os.environ["DB_PASSWORD"],
        host=os.getenv("DB_HOST", "localhost"),
        port=int(os.getenv("DB_PORT", "5432")),
        database=os.environ["TEST_DB_NAME"]
    )

    engine = create_engine(url)

    # Solo crea tablas faltantes en la BD de pruebas.
    Base.metadata.create_all(bind=engine)

    with Session(engine) as db:

        paciente = Paciente(
            nombre="Paciente Test",
            edad=30
        )

        db.add(paciente)
        db.commit()
        db.refresh(paciente)

        repository = ObservacionRepository(db)

        texto = (
            "Observación ficticia para verificar "
            "el funcionamiento del repositorio "
            + str(uuid.uuid4())
        )

        observacion = repository.guardar(
            paciente.id,
            texto
        )

        encontrada = repository.buscar_por_id(
            observacion.id
        )

        assert encontrada is not None
        assert encontrada.paciente_id == paciente.id
        assert encontrada.texto == texto
        assert encontrada.resumen_ia is None

        # Limpieza de los registros creados por la prueba.
        db.delete(encontrada)
        db.flush()
        db.delete(paciente)
        db.commit()

    engine.dispose()

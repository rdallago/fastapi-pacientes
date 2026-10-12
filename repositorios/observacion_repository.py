
from sqlalchemy import select
from sqlalchemy.orm import Session

from entidades.observacion import Observacion


class ObservacionRepository:

    def __init__(self, db: Session):
        self.db = db

    def listar(self):
        consulta = select(Observacion).order_by(
            Observacion.id
        )
        return self.db.scalars(consulta).all()

    def buscar_por_id(self, id: int):
        return self.db.get(Observacion, id)

    def guardar(self, paciente_id: int, texto: str):
        observacion = Observacion(
            paciente_id=paciente_id,
            texto=texto
        )

        self.db.add(observacion)
        self.db.commit()
        self.db.refresh(observacion)

        return observacion
    
    
    def guardar_resumen(
        self,
        observacion: Observacion,
        resumen: str
    ):
        observacion.resumen_ia = resumen

        self.db.add(observacion)
        self.db.commit()
        self.db.refresh(observacion)

        return observacion
    
    

from sqlalchemy import select
from sqlalchemy.orm import Session

from entidades.paciente import Paciente
from modelos.paciente import PacienteCrear


class PacienteRepository:

    def __init__(self, db: Session):
        self.db = db

    def listar(self):
        consulta = select(Paciente).order_by(Paciente.id)

        return self.db.scalars(consulta).all()

    def buscar_por_id(self, id: int):
        return self.db.get(Paciente, id)

    def guardar(self, datos: PacienteCrear):
        paciente = Paciente(
            nombre=datos.nombre,
            edad=datos.edad
        )

        self.db.add(paciente)
        self.db.commit()
        self.db.refresh(paciente)

        return paciente

    def actualizar(self, paciente: Paciente, datos: PacienteCrear):
        paciente.nombre = datos.nombre
        paciente.edad = datos.edad

        self.db.commit()
        self.db.refresh(paciente)

        return paciente

    def eliminar(self, paciente: Paciente):
        self.db.delete(paciente)
        self.db.commit()

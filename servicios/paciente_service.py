
from fastapi import HTTPException

from modelos.paciente import PacienteCrear
from repositorios.paciente_repository import PacienteRepository


class PacienteService:

    def __init__(self, repository: PacienteRepository):
        self.repository = repository

    def listar(self):
        return self.repository.listar()

    def buscar_por_id(self, id: int):
        paciente = self.repository.buscar_por_id(id)

        if paciente is None:
            raise HTTPException(
                status_code=404,
                detail="Paciente no encontrado"
            )

        return paciente

    def guardar(self, datos: PacienteCrear):
        return self.repository.guardar(datos)

    def actualizar(self, id: int, datos: PacienteCrear):
        paciente = self.buscar_por_id(id)

        return self.repository.actualizar(
            paciente,
            datos
        )

    def eliminar(self, id: int):
        paciente = self.buscar_por_id(id)

        # La validación de visitas se implementará
        # cuando exista la entidad Visita en PostgreSQL.

        self.repository.eliminar(paciente)

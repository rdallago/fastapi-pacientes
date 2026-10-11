
from fastapi import HTTPException
from modelos.paciente import PacienteCrear


class PacienteService:

    def __init__(self):
        self.pacientes = [
            {"id": 1, "nombre": "Ana", "edad": 35},
            {"id": 2, "nombre": "Pedro", "edad": 42}
        ]

        self.visitas = [
            {"id": 1, "paciente_id": 1}
        ]

        self.siguiente_id = 3

    def listar(self):
        return self.pacientes

    def buscar_por_id(self, id: int):
        for paciente in self.pacientes:
            if paciente["id"] == id:
                return paciente

        raise HTTPException(
            status_code=404,
            detail="Paciente no encontrado"
        )

    def guardar(self, datos: PacienteCrear):
        nuevo = {
            "id": self.siguiente_id,
            "nombre": datos.nombre,
            "edad": datos.edad
        }

        self.pacientes.append(nuevo)
        self.siguiente_id += 1

        return nuevo

    def actualizar(self, id: int, datos: PacienteCrear):
        paciente = self.buscar_por_id(id)

        paciente["nombre"] = datos.nombre
        paciente["edad"] = datos.edad

        return paciente

    def eliminar(self, id: int):
        paciente = self.buscar_por_id(id)

        tiene_visitas = any(
            visita["paciente_id"] == id
            for visita in self.visitas
        )

        if tiene_visitas:
            raise HTTPException(
                status_code=409,
                detail="No se puede eliminar un paciente con visitas"
            )

        self.pacientes.remove(paciente)

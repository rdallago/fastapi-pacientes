
from fastapi import APIRouter, Depends, Response, status

from modelos.paciente import PacienteCrear, PacienteRespuesta
from servicios.paciente_service import PacienteService


router = APIRouter(
    prefix="/api/pacientes",
    tags=["Pacientes"]
)


# INSTANCIA COMPARTIDA PARA ESTE EJEMPLO
servicio = PacienteService()


def obtener_servicio() -> PacienteService:
    return servicio


# GET - LISTAR
@router.get("/", response_model=list[PacienteRespuesta])
def listar(
    service: PacienteService = Depends(obtener_servicio)
):
    return service.listar()


# GET - BUSCAR
@router.get("/{id}", response_model=PacienteRespuesta)
def buscar(
    id: int,
    service: PacienteService = Depends(obtener_servicio)
):
    return service.buscar_por_id(id)


# POST - GUARDAR
@router.post(
    "/",
    response_model=PacienteRespuesta,
    status_code=201
)
def guardar(
    datos: PacienteCrear,
    service: PacienteService = Depends(obtener_servicio)
):
    return service.guardar(datos)


# PUT - ACTUALIZAR
@router.put("/{id}", response_model=PacienteRespuesta)
def actualizar(
    id: int,
    datos: PacienteCrear,
    service: PacienteService = Depends(obtener_servicio)
):
    return service.actualizar(id, datos)


# DELETE - ELIMINAR
@router.delete("/{id}", status_code=204)
def eliminar(
    id: int,
    service: PacienteService = Depends(obtener_servicio)
):
    service.eliminar(id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)

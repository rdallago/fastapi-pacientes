
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from database import get_db

from modelos.observacion import (
    ObservacionCrear,
    ObservacionRespuesta
)

from repositorios.observacion_repository import (
    ObservacionRepository
)

from repositorios.paciente_repository import (
    PacienteRepository
)

from servicios.observacion_service import (
    ObservacionService
)


router = APIRouter(
    prefix="/api/observaciones",
    tags=["Observaciones"]
)


def obtener_servicio(
    db: Session = Depends(get_db)
) -> ObservacionService:

    observacion_repository = ObservacionRepository(db)
    paciente_repository = PacienteRepository(db)

    return ObservacionService(
        observacion_repository,
        paciente_repository
    )


@router.get(
    "/",
    response_model=list[ObservacionRespuesta]
)
def listar(
    service: ObservacionService = Depends(obtener_servicio)
):
    return service.listar()


@router.get(
    "/{id}",
    response_model=ObservacionRespuesta
)
def buscar(
    id: int,
    service: ObservacionService = Depends(obtener_servicio)
):
    return service.buscar_por_id(id)


@router.post(
    "/",
    response_model=ObservacionRespuesta,
    status_code=201
)
def guardar(
    datos: ObservacionCrear,
    service: ObservacionService = Depends(obtener_servicio)
):
    return service.guardar(datos)


@router.post(
    "/{id}/resumir",
    response_model=ObservacionRespuesta
)
def resumir_observacion(
    id: int,
    nivel: str = "medio",
    service: ObservacionService = Depends(obtener_servicio)
):
    if nivel not in ["breve", "medio", "detallado"]:
        raise HTTPException(
            status_code=400,
            detail="Nivel de resumen no válido"
        )

    return service.generar_resumen(id, nivel)


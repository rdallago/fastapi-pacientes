
from fastapi import APIRouter, HTTPException
from openai import (
    APIConnectionError,
    APIStatusError,
    APITimeoutError,
    RateLimitError
)

from modelos.ia import (
    SolicitudResumen,
    RespuestaResumen
)
from servicios.ia_service import IAService


router = APIRouter(
    prefix="/api/ia",
    tags=["Inteligencia Artificial"]
)


@router.post(
    "/resumir",
    response_model=RespuestaResumen
)
def resumir_texto(datos: SolicitudResumen):

    try:
        servicio = IAService()
        resumen = servicio.resumir(
                datos.texto,
                datos.nivel
      )

        return RespuestaResumen(
            resumen=resumen
        )

    except RateLimitError:
        raise HTTPException(
            status_code=503,
            detail="Límite o cuota del proveedor de IA"
        )

    except (APIConnectionError, APITimeoutError):
        raise HTTPException(
            status_code=503,
            detail="No se pudo conectar con el proveedor de IA"
        )

    except APIStatusError:
        raise HTTPException(
            status_code=502,
            detail="El proveedor de IA rechazó la solicitud"
        )

    except ValueError:
        raise HTTPException(
            status_code=503,
            detail="El servicio de IA no está configurado"
        )

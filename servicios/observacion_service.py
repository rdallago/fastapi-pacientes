
from fastapi import HTTPException

from modelos.observacion import ObservacionCrear
from repositorios.observacion_repository import (
    ObservacionRepository
)
from repositorios.paciente_repository import (
    PacienteRepository
)

from openai import (
    APIConnectionError,
    APIStatusError,
    APITimeoutError,
    RateLimitError
)

from servicios.ia_service import IAService


class ObservacionService:

    def __init__(
        self,
        observacion_repository: ObservacionRepository,
        paciente_repository: PacienteRepository
    ):
        self.observacion_repository = observacion_repository
        self.paciente_repository = paciente_repository

    def listar(self):
        return self.observacion_repository.listar()

    def buscar_por_id(self, id: int):
        observacion = (
            self.observacion_repository.buscar_por_id(id)
        )

        if observacion is None:
            raise HTTPException(
                status_code=404,
                detail="Observación no encontrada"
            )

        return observacion

    def guardar(self, datos: ObservacionCrear):
        paciente = self.paciente_repository.buscar_por_id(
            datos.paciente_id
        )

        if paciente is None:
            raise HTTPException(
                status_code=404,
                detail="El paciente no existe"
            )

        return self.observacion_repository.guardar(
            datos.paciente_id,
            datos.texto
        )
    
    def generar_resumen(self, id: int, nivel: str = "medio"):

        # 1. Buscar la observación en PostgreSQL
        observacion = self.buscar_por_id(id)

        # 2. Verificar que tenga contenido
        if not observacion.texto.strip():
            raise HTTPException(
                status_code=400,
                detail="La observación no tiene texto"
            )

        # 3. Solicitar el resumen a OpenRouter
        try:
            ia_service = IAService()

            resumen = ia_service.resumir(
                observacion.texto,
                nivel
            )

        except RateLimitError:
            raise HTTPException(
                status_code=503,
                detail="Se alcanzó el límite de OpenRouter"
            )

        except (APIConnectionError, APITimeoutError):
            raise HTTPException(
                status_code=503,
                detail="No se pudo conectar con OpenRouter"
            )

        except APIStatusError:
            raise HTTPException(
                status_code=502,
                detail="OpenRouter rechazó la solicitud"
            )

        except ValueError:
            raise HTTPException(
                status_code=503,
                detail="No se pudo generar el resumen"
            )

        # 4. Guardar el resultado en PostgreSQL
        return self.observacion_repository.guardar_resumen(
            observacion,
            resumen
        )


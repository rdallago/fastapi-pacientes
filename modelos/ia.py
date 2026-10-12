
from typing import Literal

from pydantic import BaseModel, Field


class SolicitudResumen(BaseModel):
    texto: str = Field(
        min_length=10,
        max_length=10000
    )

    nivel: Literal[
        "breve",
        "medio",
        "detallado"
    ] = "medio"


class RespuestaResumen(BaseModel):
    resumen: str

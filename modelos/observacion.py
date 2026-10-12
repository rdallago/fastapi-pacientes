
from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class ObservacionCrear(BaseModel):
    paciente_id: int = Field(gt=0)

    texto: str = Field(
        min_length=10,
        max_length=10000
    )


class ObservacionRespuesta(BaseModel):
    id: int
    paciente_id: int
    texto: str
    resumen_ia: str | None
    fecha_creacion: datetime

    model_config = ConfigDict(
        from_attributes=True
    )

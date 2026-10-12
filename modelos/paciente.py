
from pydantic import (
    BaseModel,
    ConfigDict,
    Field,
    field_validator
)


class PacienteCrear(BaseModel):
    nombre: str = Field(min_length=1, max_length=100)
    edad: int = Field(ge=0, le=120, strict=True)

    @field_validator("nombre")
    @classmethod
    def validar_nombre(cls, valor: str) -> str:
        valor = valor.strip()

        if not valor:
            raise ValueError("El nombre es obligatorio")

        return valor


class PacienteRespuesta(PacienteCrear):
    id: int

    model_config = ConfigDict(from_attributes=True)


from sqlalchemy import Integer, String
from sqlalchemy.orm import (
    Mapped,
    mapped_column,
    relationship
)

from database import Base


class Paciente(Base):
    __tablename__ = "pacientes_curso"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        autoincrement=True
    )

    nombre: Mapped[str] = mapped_column(
        String(100),
        nullable=False
    )

    edad: Mapped[int] = mapped_column(
        Integer,
        nullable=False
    )

    observaciones: Mapped[list["Observacion"]] = relationship(
        "Observacion",
        back_populates="paciente",
        passive_deletes="all"
    )

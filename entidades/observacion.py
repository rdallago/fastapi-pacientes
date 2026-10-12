
from datetime import datetime

from sqlalchemy import (
    DateTime,
    ForeignKey,
    Integer,
    Text,
    func
)

from sqlalchemy.orm import Mapped, mapped_column, relationship

from database import Base


class Observacion(Base):
    __tablename__ = "observaciones_curso"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        autoincrement=True
    )

    paciente_id: Mapped[int] = mapped_column(
        ForeignKey(
            "pacientes_curso.id",
            ondelete="RESTRICT"
        ),
        nullable=False,
        index=True
    )

    texto: Mapped[str] = mapped_column(
        Text,
        nullable=False
    )

    resumen_ia: Mapped[str | None] = mapped_column(
        Text,
        nullable=True
    )

    fecha_creacion: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False
    )

    paciente: Mapped["Paciente"] = relationship(
        "Paciente",
        back_populates="observaciones"
    )

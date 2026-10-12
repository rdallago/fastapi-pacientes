
from fastapi import FastAPI

from routers.paciente import router as pacientes_router
from routers.ia import router as ia_router
from routers.observaciones import router as observaciones_router

app = FastAPI(
    title="Sistema de Pacientes",
    description="API REST desarrollada con Python y FastAPI",
    version="1.0.0"
)

app.include_router(pacientes_router)
app.include_router(ia_router)
app.include_router(observaciones_router)


@app.get("/")
def inicio():
    return {
        "mensaje": "Bienvenido al Sistema de Pacientes"
    }

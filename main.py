
from fastapi import FastAPI
from routers.paciente import router as pacientes_router


app = FastAPI(
    title="Sistema de Pacientes",
    description="API REST desarrollada con Python y FastAPI",
    version="1.0.0"
)


app.include_router(pacientes_router)


@app.get("/")
def inicio():
    return {"mensaje": "API funcionando correctamente"}

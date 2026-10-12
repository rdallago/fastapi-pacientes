import os

from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()


class IAService:

    def __init__(self):
        api_key = os.getenv("OPENROUTER_API_KEY")

        if not api_key:
            raise ValueError(
                "Falta configurar OPENROUTER_API_KEY"
            )

        self.modelo = os.getenv(
            "OPENROUTER_MODEL",
            "openrouter/free"
        )

        self.cliente = OpenAI(
            api_key=api_key,
            base_url="https://openrouter.ai/api/v1",
            timeout=30.0,
            max_retries=1
        )

    def resumir(self, texto: str, nivel: str = "medio") -> str:

        configuraciones = {
            "breve": {
                "porcentaje": 15,
                "descripcion": "Muy breve: solo la idea central."
            },
            "medio": {
                "porcentaje": 35,
                "descripcion": (
                    "Síntesis de las ideas principales, "
                    "conceptos y autores relevantes."
                )
            },
            "detallado": {
                "porcentaje": 60,
                "descripcion": (
                    "Resumen amplio que conserva más "
                    "detalles, sin repetir explicaciones."
                )
            }
        }

        if nivel not in configuraciones:
            raise ValueError("Nivel de resumen no válido")

        config = configuraciones[nivel]

        palabras_originales = len(texto.split())

        palabras_objetivo = max(
            15,
            int(
                palabras_originales
                * config["porcentaje"] / 100
            )
        )

        instrucciones = f"""
Sos un asistente especializado en resumir textos
en español.

Tu tarea es SINTETIZAR, no explicar ni ampliar.

REGLAS OBLIGATORIAS:
1. Utilizá exclusivamente información del texto.
2. Eliminá repeticiones y ejemplos secundarios.
3. Conservá los conceptos y nombres fundamentales.
4. No agregues explicaciones propias.
5. No inventes información.
6. No repitas el texto original con otras palabras.
7. El resumen debe ser más corto que el original.

NIVEL: {nivel}
DESCRIPCIÓN: {config["descripcion"]}

EXTENSIÓN OBJETIVO:
Aproximadamente {palabras_objetivo} palabras.

Devolvé solamente el resumen.
"""

        respuesta = self.cliente.chat.completions.create(
            model=self.modelo,
            messages=[
                {
                    "role": "system",
                    "content": instrucciones
                },
                {
                    "role": "user",
                    "content": texto
                }
            ],
            max_tokens=500,
            temperature=0.1
        )

        resumen = respuesta.choices[0].message.content

        if not resumen or not resumen.strip():
            raise ValueError(
                "El modelo no devolvió contenido"
            )
            
        palabras_resumen = len(resumen.split())
        reduccion = (1 - palabras_resumen / palabras_originales) * 100

        print("Modelo:", respuesta.model)
        print("Palabras originales:", palabras_originales)
        print("Palabras del resumen:", palabras_resumen)
        print(f"Reducción: {reduccion:.1f}%")

        return resumen.strip()

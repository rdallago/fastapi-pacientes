
from unittest.mock import MagicMock, patch

from servicios.ia_service import IAService


def test_resumir_con_openrouter_simulado():

    with patch.dict(
        "os.environ",
        {"OPENROUTER_API_KEY": "clave_ficticia"}
    ):
        with patch(
            "servicios.ia_service.OpenAI"
        ) as mock_openai:

            cliente_simulado = MagicMock()
            mock_openai.return_value = cliente_simulado

            respuesta_simulada = MagicMock()
            respuesta_simulada.model = "modelo-simulado"

            respuesta_simulada.choices[
                0
            ].message.content = (
                "El conductismo estudia "
                "la conducta observable."
            )

            cliente_simulado.chat.completions.create.return_value = (
                respuesta_simulada
            )

            servicio = IAService()

            resultado = servicio.resumir(
                "El conductismo es una corriente "
                "de la psicología que estudia "
                "objetivamente la conducta "
                "observable de las personas.",
                "breve"
            )

            assert resultado == (
                "El conductismo estudia "
                "la conducta observable."
            )

            cliente_simulado.chat.completions.create.assert_called_once()

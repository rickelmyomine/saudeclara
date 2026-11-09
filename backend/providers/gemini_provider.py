import os
import time

from google import genai
from google.genai import types


class LLMError(Exception):
    pass


_client = None


def _get_client():
    global _client
    key = os.getenv("GEMINI_API_KEY")
    if not key:
        raise LLMError("GEMINI_API_KEY não configurada")
    if _client is None:
        _client = genai.Client(
            api_key=key,
            http_options=types.HttpOptions(timeout=30000),  # 30 s por tentativa
        )
    return _client


def _modelos() -> list[str]:
    principal = os.getenv("GEMINI_MODEL", "gemini-3.8-flash")
    reserva = os.getenv("GEMINI_FALLBACK_MODEL", "gemini-3.6-flash")
    return [principal] + ([reserva] if reserva and reserva != principal else [])


def _transitorio(e: Exception) -> bool:
    msg = str(e)
    return any(c in msg for c in ("503", "429", "UNAVAILABLE", "RESOURCE_EXHAUSTED", "500"))


def gerar_estruturado(prompt: str, system: str, schema, tentativas: int = 2):
    """Chama o Gemini com saída estruturada, retry com espera e modelo reserva."""
    config = types.GenerateContentConfig(
        system_instruction=system,
        response_mime_type="application/json",
        response_schema=schema,
        temperature=0.2,
    )
    ultimo_erro = None
    for modelo in _modelos():
        for i in range(tentativas):
            try:
                resp = _get_client().models.generate_content(
                    model=modelo, contents=prompt, config=config
                )
                if resp.parsed is None:
                    raise LLMError("Resposta inválida do modelo")
                return resp.parsed
            except LLMError:
                raise
            except Exception as e:
                ultimo_erro = e
                if not _transitorio(e):
                    break  # erro permanente neste modelo: tenta o reserva
                time.sleep(2 ** i)  # espera 1s, 2s...
    raise LLMError(str(ultimo_erro))
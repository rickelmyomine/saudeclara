import os
import requests


class ApiError(Exception):
    """Erro com mensagem já amigável para o cidadão."""


API_URL = os.getenv("API_URL", "http://localhost:8000")


def api_online() -> bool:
    try:
        return requests.get(f"{API_URL}/health", timeout=3).ok
    except requests.RequestException:
        return False


def enviar_triagem(payload: dict) -> dict:
    try:
        r = requests.post(f"{API_URL}/triagem", json=payload, timeout=90)
    except requests.ConnectionError:
        raise ApiError("Não conseguimos conectar ao serviço. Tente novamente em instantes.")
    except requests.Timeout:
        raise ApiError("A análise demorou mais que o esperado. Tente novamente.")
    if r.status_code == 422:
        raise ApiError("Alguns dados parecem inválidos. Revise o formulário.")
    if r.status_code >= 500:
        raise ApiError("O serviço de análise está indisponível agora. Tente novamente.")
    try:
        return r.json()
    except ValueError:
        raise ApiError("Recebemos uma resposta inesperada. Tente novamente.")

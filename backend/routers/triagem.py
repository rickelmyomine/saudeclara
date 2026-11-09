import logging
from fastapi import APIRouter, HTTPException

from schemas.triagem import TriagemRequest, TriagemResponse
from pipelines import triagem_pipeline
from providers.gemini_provider import LLMError

router = APIRouter()
log = logging.getLogger("triagem")


@router.get("/health")
def health():
    return {"status": "ok"}


@router.post("/triagem", response_model=TriagemResponse)
def triagem(req: TriagemRequest):
    try:
        return triagem_pipeline.executar(req)
    except LLMError as e:
        log.error("Erro LLM: %s", e)  # detalhe só no log do servidor
        raise HTTPException(status_code=502, detail="Serviço de IA indisponível no momento.")

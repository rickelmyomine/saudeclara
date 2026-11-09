from datetime import datetime
from typing import Literal
from pydantic import BaseModel, Field, field_validator

Urgencia = Literal["emergencia", "urgente", "pouco_urgente", "orientacao_domiciliar"]


class TriagemRequest(BaseModel):
    sintomas: str = Field(..., min_length=10, max_length=1000)
    idade: int = Field(..., ge=0, le=120)
    duracao: Literal["menos de 24h", "1 a 3 dias", "mais de 3 dias", "mais de 1 semana"]

    @field_validator("sintomas")
    @classmethod
    def limpar(cls, v: str) -> str:
        v = " ".join(v.split())
        if len(v) < 10:
            raise ValueError("Descreva melhor os sintomas.")
        return v


class TriagemIA(BaseModel):
    """Saída estruturada exigida do LLM."""
    nivel_urgencia: Urgencia
    resumo: str = Field(description="Resumo curto e em linguagem simples do quadro")
    sinais_alerta: list[str] = Field(description="Sinais que exigem procurar ajuda imediata")
    orientacoes: list[str] = Field(description="Cuidados e orientações práticas")
    onde_buscar: str = Field(description="SAMU 192, UPA, UBS ou autocuidado")


class TriagemResponse(TriagemIA):
    protocolo: str
    criado_em: datetime
    aviso: str = "Esta orientação NÃO substitui avaliação de um profissional de saúde."

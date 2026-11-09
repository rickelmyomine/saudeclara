# 🩺 SaúdeClara — CitizenTech em Saúde

Triagem de sintomas com IA para orientar o cidadão sobre **onde buscar atendimento no SUS** (SAMU, UPA ou UBS).

## Fluxo CitizenTech
Entrada (formulário validado) → FastAPI → Gemini (saída estruturada Pydantic) → resposta com urgência, orientações e confirmação do cidadão (human-in-the-loop) → painel Plotly.

## Arquitetura
```
Streamlit (frontend/)  --HTTP-->  FastAPI (backend/)  -->  Gemini
 features/ ui/ state/ providers/     routers/ schemas/ pipelines/ providers/
```
(Substitua por um diagrama visual, ex.: Mermaid ou draw.io.)

## Como executar
**Local**
```bash
cd backend && cp .env.example .env   # coloque sua GEMINI_API_KEY
pip install -r requirements.txt && uvicorn main:app --reload
# outro terminal
cd frontend && pip install -r requirements.txt && streamlit run app.py
```
**Docker:** `cp backend/.env.example backend/.env` (preencha a chave) e `docker compose up --build` → http://localhost:8501

## Acessibilidade aplicada
- Cores de urgência sempre com ícone + texto; contraste alto (texto branco sobre cores escuras)
- Rótulos e textos de ajuda em todos os campos; linguagem simples
- Estados de erro, vazio e carregamento tratados

## Segurança
Chave em `.env` (fora do git); CORS restrito por `ALLOWED_ORIGINS`; validação Pydantic; regra determinística de sinais graves além do LLM; erros técnicos nunca exibidos ao usuário; aviso para não informar dados pessoais.

## Justificativas (seção 3.8) — PREENCHER
- **Problema e público:** (cite fonte: ex. dados de superlotação de UPAs / notícia / entrevista)
- **ODS:** 3 (Saúde e Bem-Estar) e 10 (Redução das Desigualdades) — justifique
- **Decisões técnicas:** Streamlit, prompt, saída estruturada, deploy
- **Ética e limites:** não diagnostica, não indica remédio, pode errar; HITL e regra de sinais graves mitigam
- **Validação (a):** teste com 3+ pessoas — roteiro, observações, ajuste feito
- **Validação (b):** tabela de casos de teste

| Entrada | Esperado | Obtido | Ajuste |
|---|---|---|---|
| | | | |

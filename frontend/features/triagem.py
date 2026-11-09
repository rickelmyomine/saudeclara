import json
from datetime import datetime

import streamlit as st

from providers.api_client import ApiError, enviar_triagem
from state.session import add_historico
from ui.components import URGENCIA, badge_urgencia, lista_com_icone

DURACOES = ["menos de 24h", "1 a 3 dias", "mais de 3 dias", "mais de 1 semana"]


@st.cache_data(ttl=600, show_spinner=False)
def _triagem_cache(payload_json: str) -> dict:
    """Mesma entrada em 10 min não repete a chamada ao LLM (erros não são cacheados)."""
    return enviar_triagem(json.loads(payload_json))


def _validar(sintomas: str) -> list[str]:
    erros = []
    if len(sintomas.strip()) < 10:
        erros.append("Descreva seus sintomas com pelo menos 10 caracteres.")
    return erros


def _formulario():
    with st.form("form_triagem"):
        sintomas = st.text_area(
            "O que você está sentindo?", max_chars=1000, height=140,
            placeholder="Ex.: febre alta há 2 dias, dor de garganta e dor no corpo",
            help="Descreva com suas palavras. Não informe nome, CPF ou endereço.",
        )
        c1, c2 = st.columns(2)
        idade = c1.number_input("Idade (anos)", min_value=0, max_value=120, value=30, step=1)
        duracao = c2.selectbox("Há quanto tempo?", DURACOES)
        enviado = st.form_submit_button("Analisar sintomas", type="primary")

    if not enviado:
        return
    erros = _validar(sintomas)
    if erros:
        for e in erros:
            st.error(e)
        return
    entrada = {"sintomas": sintomas.strip(), "idade": int(idade), "duracao": duracao}
    try:
        with st.spinner("Analisando seus sintomas com segurança..."):
            res = _triagem_cache(json.dumps(entrada, sort_keys=True))
        st.session_state["resultado_atual"] = res
        st.session_state["entrada_atual"] = entrada
    except ApiError as e:
        st.session_state["resultado_atual"] = None
        st.error(f"⚠️ {e}")


def _resultado():
    res = st.session_state["resultado_atual"]
    if not res:
        st.info("👆 Preencha o formulário para receber uma orientação.")
        return
    st.divider()
    st.caption(f"Protocolo {res['protocolo']}")
    badge_urgencia(res["nivel_urgencia"])
    st.markdown(f"### 📍 {res['onde_buscar']}")
    st.write(res["resumo"])
    col1, col2 = st.columns(2)
    with col1:
        lista_com_icone("Sinais de alerta (procure ajuda se ocorrer)", res["sinais_alerta"], "⚠️")
    with col2:
        lista_com_icone("O que fazer agora", res["orientacoes"], "✅")
    st.warning(res["aviso"])

    # ---- Human-in-the-loop ----
    st.subheader("Confirme o resultado")
    ok = st.radio("A classificação faz sentido para você?", ["Sim", "Não"], horizontal=True)
    nivel_final = res["nivel_urgencia"]
    if ok == "Não":
        nivel_final = st.selectbox(
            "Qual seria o nível correto?", list(URGENCIA),
            format_func=lambda k: f'{URGENCIA[k]["icone"]} {URGENCIA[k]["rotulo"]}',
        )
    util = st.checkbox("A orientação foi útil", value=True)
    if st.button("Confirmar e registrar"):
        add_historico({
            "protocolo": res["protocolo"],
            "data": datetime.now(),
            "idade": st.session_state["entrada_atual"]["idade"],
            "nivel_ia": res["nivel_urgencia"],
            "nivel_final": nivel_final,
            "corrigido": nivel_final != res["nivel_urgencia"],
            "util": util,
        })
        st.session_state["resultado_atual"] = None
        st.success("Registrado! Obrigado pelo seu feedback.")
        st.rerun()


def render():
    st.header("Como você está se sentindo?")
    _formulario()
    _resultado()

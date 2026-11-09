import streamlit as st

from features import painel, triagem
from providers.api_client import api_online
from state.session import init_state

st.set_page_config(page_title="SaúdeClara", page_icon="🩺", layout="wide")
init_state()


@st.cache_data(ttl=30, show_spinner=False)
def _status():
    return api_online()


with st.sidebar:
    st.title("🩺 SaúdeClara")
    st.write("Orientação rápida sobre onde buscar atendimento no SUS.")
    if _status():
        st.success("Serviço online ✅")
    else:
        st.error("Serviço offline ❌ — tente mais tarde")
    st.divider()
    st.error("🚨 Em risco de vida, ligue **192 (SAMU)** agora.")
    st.caption("Não substitui consulta médica. Não envie dados pessoais.")

tab1, tab2 = st.tabs(["🩺 Triagem", "📊 Painel"])
with tab1:
    triagem.render()
with tab2:
    painel.render()

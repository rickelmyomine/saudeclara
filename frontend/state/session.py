import streamlit as st


def init_state():
    st.session_state.setdefault("historico", [])          # solicitações confirmadas
    st.session_state.setdefault("resultado_atual", None)  # resultado aguardando confirmação
    st.session_state.setdefault("entrada_atual", None)


def add_historico(registro: dict):
    st.session_state["historico"].append(registro)


def get_historico() -> list[dict]:
    return st.session_state["historico"]

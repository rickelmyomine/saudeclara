import streamlit as st

# Cor SEMPRE acompanhada de ícone + texto (acessibilidade)
URGENCIA = {
    "emergencia":            {"rotulo": "EMERGÊNCIA",       "icone": "🚨", "cor": "#B00020", "txt": "#FFFFFF"},
    "urgente":               {"rotulo": "URGENTE",          "icone": "🟠", "cor": "#B45309", "txt": "#FFFFFF"},
    "pouco_urgente":         {"rotulo": "POUCO URGENTE",    "icone": "🟡", "cor": "#854D0E", "txt": "#FFFFFF"},
    "orientacao_domiciliar": {"rotulo": "CUIDADOS EM CASA", "icone": "🟢", "cor": "#166534", "txt": "#FFFFFF"},
}
CORES_GRAFICO = {v["rotulo"]: v["cor"] for v in URGENCIA.values()}


def badge_urgencia(nivel: str, tamanho: str = "1.4rem"):
    """Componente reutilizado no resultado e no histórico (parâmetros diferentes)."""
    u = URGENCIA[nivel]
    st.markdown(
        f'<div role="status" style="background:{u["cor"]};color:{u["txt"]};padding:.6rem 1rem;'
        f'border-radius:8px;font-size:{tamanho};font-weight:700;display:inline-block">'
        f'{u["icone"]} {u["rotulo"]}</div>',
        unsafe_allow_html=True,
    )


def lista_com_icone(titulo: str, itens: list[str], icone: str):
    st.markdown(f"**{icone} {titulo}**")
    for i in itens:
        st.markdown(f"- {i}")


def metric_card(rotulo: str, valor):
    st.metric(label=rotulo, value=valor)

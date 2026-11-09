import pandas as pd
import plotly.express as px
import streamlit as st

from state.session import get_historico
from ui.components import CORES_GRAFICO, URGENCIA, badge_urgencia, metric_card


def render():
    st.header("Painel de solicitações")
    hist = get_historico()
    if not hist:
        st.info("Nenhuma solicitação registrada ainda. Faça uma triagem na aba anterior.")
        return

    df = pd.DataFrame(hist)
    df["Urgência"] = df["nivel_final"].map(lambda k: URGENCIA[k]["rotulo"])

    # ---- Filtros (2 controles) ----
    c1, c2 = st.columns(2)
    sel = c1.multiselect("Filtrar por urgência", list(CORES_GRAFICO), default=list(CORES_GRAFICO))
    faixa = c2.slider("Faixa etária", 0, 120, (0, 120))
    f = df[df["Urgência"].isin(sel) & df["idade"].between(*faixa)]
    if f.empty:
        st.warning("Nenhum registro com esses filtros.")
        return

    m1, m2, m3 = st.columns(3)
    with m1:
        metric_card("Total", len(f))
    with m2:
        metric_card("Corrigidas pelo cidadão", int(f["corrigido"].sum()))
    with m3:
        metric_card("Marcadas como úteis", f"{int(f['util'].mean() * 100)}%")

    g1, g2 = st.columns(2)
    cont = f["Urgência"].value_counts().reset_index()
    cont.columns = ["Urgência", "Quantidade"]
    g1.plotly_chart(
        px.bar(cont, x="Urgência", y="Quantidade", color="Urgência",
               color_discrete_map=CORES_GRAFICO, text="Quantidade", title="Solicitações por urgência"),
        use_container_width=True,
    )
    g2.plotly_chart(
        px.scatter(f, x="data", y="idade", color="Urgência", color_discrete_map=CORES_GRAFICO,
                   hover_data=["protocolo"], title="Linha do tempo (hover para detalhes)"),
        use_container_width=True,
    )

    st.subheader("Últimos registros")
    for r in reversed(f.to_dict("records")[-5:]):
        badge_urgencia(r["nivel_final"], tamanho="1rem")
        st.caption(f'Protocolo {r["protocolo"]} · {r["data"]:%d/%m %H:%M}')

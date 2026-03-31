import streamlit as st

from app.ui.dashboard import render_dashboard
from app.ui.regras import regras_page
from app.ui.alertas import alertas_page
from app.ui.checkins import checkins_page
from app.ui.relatorio import relatorio_page
from app.ui.chatgpt_mvp import chatgpt_page
from app.ui.atividades import atividades_page


def main():
    # redirecionamento pós-clique (antes de instanciar widgets)
    nav_default = st.session_state.get("nav", "Dashboard")
    nav_pending = st.session_state.pop("_nav_target", None)
    if nav_pending:
        nav_default = nav_pending
        st.session_state["nav"] = nav_default

    st.sidebar.title("Navegação")
    page = st.sidebar.radio(
        "Ir para",
        ["Dashboard", "Atividades", "Regras", "Alertas", "Check-ins", "Relatório", "ChatGPT (MVP)"],
        key="nav",
        index=["Dashboard", "Atividades", "Regras", "Alertas", "Check-ins", "Relatório", "ChatGPT (MVP)"].index(nav_default)
    )
    if page == "Dashboard":
        render_dashboard()
    elif page == "Atividades":
        atividades_page()
    elif page == "Regras":
        regras_page()
    elif page == "Alertas":
        alertas_page()
    elif page == "Check-ins":
        checkins_page()
    elif page == "Relatório":
        relatorio_page()
    else:
        chatgpt_page()


if __name__ == "__main__":
    main()

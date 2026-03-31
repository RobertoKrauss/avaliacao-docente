import streamlit as st

from app.ui.dashboard import render_dashboard
from app.ui.regras import regras_page
from app.ui.alertas import alertas_page
from app.ui.checkins import checkins_page
from app.ui.relatorio import relatorio_page
from app.ui.chatgpt_mvp import chatgpt_page
from app.ui.atividades import atividades_page


def main():
    st.sidebar.title("Navegação")
    page = st.sidebar.radio(
        "Ir para",
        ["Dashboard", "Atividades", "Regras", "Alertas", "Check-ins", "Relatório", "ChatGPT (MVP)"],
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

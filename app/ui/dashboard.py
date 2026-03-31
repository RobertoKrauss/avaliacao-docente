import streamlit as st
from datetime import datetime
from app.ui.theme import apply_theme
from app.ui import components as ui
from app.db.connection import get_connection
from app.db.repositories import (
    anos_repository,
    atividades_repository,
    alertas_repository,
    sugestoes_repository,
)
from app.services.calculo_pipeline import recalcular_pontuacoes


def load_data(conn, ano_id):
    # Recalcula pontuação e alertas antes de exibir
    resumo = recalcular_pontuacoes(conn, ano_id)
    alertas = alertas_repository.list_by_ano(conn, ano_id)
    atividades = atividades_repository.list_by_ano(conn, ano_id)
    sugestoes = sugestoes_repository.list_by_ano(conn, ano_id)
    return resumo, alertas, atividades, sugestoes


def render_header(anos, ano_selecionado):
    st.title("Avaliação de Desempenho Docente — Dashboard")
    col1, col2, col3, col4 = st.columns([3, 2, 2, 2])
    def go(page):
        st.session_state["nav"] = page
        st.rerun()
    with col1:
        st.selectbox(
            "Ano de referência",
            options=[a["ano"] for a in anos],
            index=[a["ano"] for a in anos].index(ano_selecionado),
            key="ano_select",
            help="Selecione o ano que deseja analisar",
        )
    with col2:
        st.button("Nova atividade", type="primary", on_click=lambda: go("Atividades"))
    with col3:
        st.button("Gerar relatório", on_click=lambda: go("Relatório"))
    with col4:
        st.button("Analisar com ChatGPT", on_click=lambda: go("ChatGPT (MVP)"))
    st.button("Registrar check-in", use_container_width=True, on_click=lambda: go("Check-ins"))


def render_cards(meta_row, resumo):
    soma = resumo["soma_por_fator"]
    riscos = resumo["riscos"]
    cols = st.columns(3)
    fatores = [
        ("formacao", "Formação / Atualização", meta_row["meta_formacao"]),
        ("funcional", "Funcional – Pedagógico", meta_row["meta_funcional"]),
        ("producao", "Produção Institucional", meta_row["meta_producao"]),
    ]
    for col, (key, label, meta) in zip(cols, fatores):
        total = soma.get(key, 0.0)
        faltante = max(meta - total, 0)
        with col:
            ui.factor_card(label, total, meta, riscos.get(key, "alto"), faltante)


def render_dashboard():
    apply_theme()
    conn = get_connection()
    anos = anos_repository.list_all(conn)
    if not anos:
        st.error("Nenhum ano configurado.")
        return
    # usa seleção da sidebar
    ano_escolhido = st.session_state.get("ano_select", anos[0]["ano"])
    ano_row = next((a for a in anos if a["ano"] == ano_escolhido), anos[0])
    resumo, alertas, atividades, sugestoes = load_data(conn, ano_row["id"])

    render_header(anos, ano_row["ano"])
    st.markdown("---")
    render_cards(ano_row, resumo)
    st.markdown("---")
    ui.alerts_block(alertas)
    st.markdown("---")
    ui.activities_block(atividades)
    st.markdown("---")
    ui.suggestions_block(sugestoes)
    conn.close()


def main():
    render_dashboard()


if __name__ == "__main__":
    main()

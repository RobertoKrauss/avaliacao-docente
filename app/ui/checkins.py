import streamlit as st
from datetime import datetime

from app.ui.theme import apply_theme
from app.db.connection import get_connection
from app.db.repositories import checkins_repository, anos_repository
from app.db.repositories import atividades_repository
from app.db.repositories import anos_repository
from app.db.repositories import anos_repository as ar
from app.db.repositories import anos_repository


def checkins_page():
    apply_theme()
    conn = get_connection()
    anos = anos_repository.list_all(conn)
    if not anos:
        st.error("Nenhum ano configurado.")
        return
    ano_row = anos[0]
    st.title("Check-ins / Revisões")

    registros = checkins_repository.list_by_ano(conn, ano_row["id"])
    if registros:
        st.subheader("Histórico")
        data = [
            {
                "Data": r["data_checkin"],
                "Fator": r["fator"] or "geral",
                "Pontuação": r["pontuacao_acumulada"] or "-",
                "Risco": r["status_risco"] or "-",
                "Pendências": r["atividades_pendentes"] or "-",
            }
            for r in registros
        ]
        st.dataframe(data, use_container_width=True, hide_index=True)
        # Gráfico simples de evolução por ordem inversa
        scores = [r["pontuacao_acumulada"] or 0 for r in registros][::-1]
        labels = [r["data_checkin"] for r in registros][::-1]
        if any(scores):
            df_chart = {"Data": labels, "Pontuação": scores}
            st.line_chart(df_chart, x="Data", y="Pontuação")
    else:
        st.info("Nenhum check-in registrado.")

    st.markdown("---")
    st.subheader("Novo check-in")
    with st.form("checkin_form"):
        data_checkin = st.date_input("Data", value=datetime.utcnow())
        fator = st.selectbox("Fator (opcional)", ["geral", "formacao", "funcional", "producao"])
        pontuacao = st.number_input("Pontuação acumulada (opcional)", min_value=0.0, value=0.0, step=0.5)
        risco = st.selectbox("Status de risco", ["baixo", "medio", "alto"])
        pendencias = st.number_input("Atividades pendentes (opcional)", min_value=0, value=0, step=1)
        nota = st.text_area("Nota (opcional)", height=80)
        submit = st.form_submit_button("Registrar check-in")
        if submit:
            checkins_repository.create(
                conn,
                {
                    "ano_id": ano_row["id"],
                    "fator": None if fator == "geral" else fator,
                    "data_checkin": data_checkin.strftime("%Y-%m-%d"),
                    "pontuacao_acumulada": pontuacao or None,
                    "status_risco": risco,
                    "atividades_pendentes": pendencias or None,
                    "nota": nota or None,
                },
            )
            # Atualiza ultima_revisao quando fator geral
            if fator == "geral":
                anos_repository.marcar_ultima_revisao(conn, ano_row["id"], data_checkin.strftime("%Y-%m-%d"))
            st.success("Check-in registrado.")
            st.experimental_rerun()
    conn.close()

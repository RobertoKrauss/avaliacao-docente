import streamlit as st
from app.ui.theme import apply_theme
from app.db.connection import get_connection
from app.db.repositories import alertas_repository, anos_repository, atividades_repository


def alertas_page():
    apply_theme()
    conn = get_connection()
    anos = anos_repository.list_all(conn)
    if not anos:
        st.error("Nenhum ano configurado.")
        return
    ano_row = anos[0]
    st.title("Alertas e Pendências")

    todos_alertas = alertas_repository.list_by_ano(conn, ano_row["id"])
    fatores = ["todos"] + sorted({a["fator"] for a in todos_alertas if a["fator"]})
    tipos = ["todos"] + sorted({a["tipo_alerta"] for a in todos_alertas})
    severidades = ["todos"] + sorted({a["severidade"] for a in todos_alertas})

    col1, col2, col3, col4 = st.columns(4)
    with col1:
        fator_sel = st.selectbox("Filtro fator", fatores)
    with col2:
        tipo_sel = st.selectbox("Filtro tipo", tipos)
    with col3:
        sev_sel = st.selectbox("Filtro severidade", severidades)
    with col4:
        resolvido_flag = st.selectbox("Status", ["abertos", "resolvidos", "todos"])
        resolvido_val = {"abertos": 0, "resolvidos": 1, "todos": None}[resolvido_flag]

    alertas = alertas_repository.list_filtered(
        conn,
        ano_row["id"],
        fator=fator_sel,
        tipo=tipo_sel,
        severidade=sev_sel,
        resolvido=resolvido_val,
    )

    if not alertas:
        st.info("Nenhum alerta encontrado com os filtros.")
        conn.close()
        return

    for a in alertas:
        with st.expander(f"[{a['severidade'].upper()}] {a['tipo_alerta']} — {a['mensagem']}"):
            st.write(f"Fator: {a['fator'] or '-'}")
            st.write(f"Atividade: {a['atividade_id'] or '-'}")
            st.write(f"Recomendação: {a['recomendacao'] or '—'}")
            cols = st.columns(2)
            with cols[0]:
                if a["atividade_id"]:
                    if st.button("Abrir atividade", key=f"open-{a['id']}"):
                        atv = atividades_repository.get(conn, a["atividade_id"])
                        if atv:
                            st.write(atv)
                        else:
                            st.warning("Atividade não encontrada.")
            with cols[1]:
                if a["resolvido"] == 0:
                    if st.button("Marcar resolvido", key=f"resolve-{a['id']}"):
                        alertas_repository.resolver(conn, a["id"])
                        st.success("Alerta marcado como resolvido.")
                        st.rerun()
    conn.close()

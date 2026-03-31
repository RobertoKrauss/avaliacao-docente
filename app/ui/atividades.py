import streamlit as st
from datetime import date

from app.ui.theme import apply_theme
from app.db.connection import get_connection
from app.db.repositories import (
    anos_repository,
    atividades_repository,
    regras_repository,
)


def atividades_page():
    apply_theme()
    conn = get_connection()
    anos = anos_repository.list_all(conn)
    if not anos:
        st.error("Nenhum ano configurado.")
        return
    ano_row = anos[0]

    st.title("Atividades")

    tabs = st.tabs(["Nova atividade", "Editar atividade"])

    # --- Nova atividade ---
    with tabs[0]:
        st.subheader("Nova atividade")
        with st.form("nova_atv"):
            regras = regras_repository.list_padroes(conn) + regras_repository.list_personalizadas_ativas(conn)
            regra_options = {f"{r['nome']} ({r['categoria_principal']})": r["id"] for r in regras}

            titulo_n = st.text_input("Título*", key="titulo_novo")
            data_n = st.date_input("Data da atividade*", value=date.today(), key="data_novo")
            fator_n = st.selectbox("Fator*", ["formacao", "funcional", "producao"], key="fator_novo")
            regra_sel_n = st.selectbox("Regra*", list(regra_options.keys()), key="regra_novo")
            quantidade_n = st.number_input("Quantidade", value=0.0, step=0.5, key="quantidade_novo")
            carga_n = st.number_input("Carga horária", value=0.0, step=0.5, key="carga_novo")
            valor_manual_n = st.number_input("Valor manual (se aplicável)", value=0.0, step=0.5, key="manual_novo")
            status_n = st.text_input("Status", value="registrada", key="status_novo")
            salvar_n = st.form_submit_button("Criar atividade")
            if salvar_n:
                atividades_repository.create(
                    conn,
                    {
                        "ano_id": ano_row["id"],
                        "titulo": titulo_n,
                        "descricao": "",
                        "data_atividade": data_n.strftime("%Y-%m-%d"),
                        "fator": fator_n,
                        "regra_id": regra_options[regra_sel_n],
                        "quantidade": quantidade_n or None,
                        "carga_horaria": carga_n or None,
                        "valor_manual": valor_manual_n or None,
                        "status": status_n,
                    },
                )
                st.success("Atividade criada.")
                st.experimental_rerun()

    # --- Editar atividade ---
    with tabs[1]:
        atividades = atividades_repository.list_by_ano(conn, ano_row["id"])
        if not atividades:
            st.info("Nenhuma atividade cadastrada neste ano.")
            conn.close()
            return

        atv_map = {f"{a['titulo']} ({a['data_atividade']})": a for a in atividades}
        escolha = st.selectbox("Selecionar atividade", list(atv_map.keys()))
        atv = atv_map[escolha]

        regras = regras_repository.list_padroes(conn) + regras_repository.list_personalizadas_ativas(conn)
        regra_options = {f"{r['nome']} ({r['categoria_principal']})": r["id"] for r in regras}
        regra_inv = {v: k for k, v in regra_options.items()}

        st.subheader("Editar atividade")
        with st.form("edit_atv"):
            titulo = st.text_input("Título", value=atv["titulo"])
            data_atividade = st.date_input(
                "Data da atividade", value=date.fromisoformat(atv["data_atividade"])
            )
            fator = st.selectbox("Fator", ["formacao", "funcional", "producao"], index=["formacao","funcional","producao"].index(atv["fator"]))
            regra_label = regra_inv.get(atv["regra_id"], None)
            regra_sel = st.selectbox("Regra", list(regra_options.keys()), index=list(regra_options.keys()).index(regra_label) if regra_label else 0)
            quantidade = st.number_input("Quantidade", value=atv["quantidade"] or 0.0, step=0.5)
            carga = st.number_input("Carga horária", value=atv["carga_horaria"] or 0.0, step=0.5)
            valor_manual = st.number_input("Valor manual (se aplicável)", value=atv["valor_manual"] or 0.0, step=0.5)
            status = st.text_input("Status", value=atv["status"])
            enviado = st.form_submit_button("Salvar alterações")
            if enviado:
                atividades_repository.update(
                    conn,
                    atv["id"],
                    {
                        "titulo": titulo,
                        "data_atividade": data_atividade.strftime("%Y-%m-%d"),
                        "fator": fator,
                        "regra_id": regra_options[regra_sel],
                        "quantidade": quantidade,
                        "carga_horaria": carga,
                        "valor_manual": valor_manual,
                        "status": status,
                    },
                )
                st.success("Atividade atualizada.")
                st.experimental_rerun()
    conn.close()

import streamlit as st
from datetime import date, datetime

from app.ui.theme import apply_theme
from app.db.connection import get_connection
from app.db.repositories import (
    anos_repository,
    atividades_repository,
    regras_repository,
    evidencias_repository,
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
                new_id = atividades_repository.create(
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
                st.session_state["ultima_atividade_criada"] = new_id
                st.success("Atividade criada.")
                st.rerun()

        # Anexar evidência para a última criada
        last_id = st.session_state.get("ultima_atividade_criada")
        st.markdown("---")
        st.subheader("Anexar evidência (última atividade criada)")
        if last_id:
            with st.form("evid_nova"):
                tipo = st.selectbox(
                    "Tipo de evidência",
                    ["certificado", "portaria", "ata", "email", "declaracao", "pdf", "imagem", "link", "material_didatico", "print", "outro"],
                    key="ev_tipo_novo",
                )
                nome = st.text_input("Nome do arquivo (opcional)", key="ev_nome_novo")
                caminho = st.text_input("Caminho/URL (opcional)", key="ev_path_novo")
                descricao = st.text_area("Descrição (opcional)", height=80, key="ev_desc_novo")
                data_doc = st.date_input("Data do documento (opcional)", value=None, key="ev_data_doc_novo")
                obrig = st.checkbox("Obrigatória?", key="ev_obr_novo")
                aprov = st.checkbox("Aprovada?", key="ev_aprov_novo")
                salvar_ev = st.form_submit_button("Salvar evidência")
                if salvar_ev:
                    evidencias_repository.create(
                        conn,
                        {
                            "atividade_id": last_id,
                            "tipo": tipo,
                            "nome_arquivo": nome or None,
                            "caminho_arquivo": caminho or None,
                            "descricao": descricao or None,
                            "data_anexacao": datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S"),
                            "data_validade": data_doc.strftime("%Y-%m-%d") if data_doc else None,
                            "validade_status": None,
                            "obrigatoria": int(obrig),
                            "aprovada": int(aprov),
                        },
                    )
                    st.success("Evidência salva.")
        else:
            st.caption("Crie uma atividade primeiro para anexar evidências aqui.")

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
                st.rerun()

        st.markdown("---")
        st.subheader("Evidências desta atividade")
        evidencias = evidencias_repository.list_by_atividade(conn, atv["id"])
        if not evidencias:
            st.markdown('<div class="empty-state">Nenhuma evidência vinculada.</div>', unsafe_allow_html=True)
        else:
            st.markdown(
                "<div class='table-header'>Tipo | Nome | Caminho | Data inserção | Data documento | Obrigatória | Aprovada | Ações</div>",
                unsafe_allow_html=True,
            )
            for e in evidencias:
                c1, c2, c3, c4, c5, c6, c7, c8 = st.columns([1.1, 1.6, 1.6, 1.2, 1.2, 0.9, 0.9, 0.8])
                c1.markdown(f"**{e['tipo']}**")
                c2.markdown(e["nome_arquivo"] or "-")
                c3.markdown(e["caminho_arquivo"] or "-")
                c4.markdown(e["data_anexacao"])
                c5.markdown(e["data_validade"] or "-")
                c6.markdown("Sim" if e["obrigatoria"] else "Não")
                c7.markdown("Sim" if e["aprovada"] else "Não")
                if c8.button("Remover", key=f"del_ev_{e['id']}"):
                    evidencias_repository.soft_delete(conn, e["id"])
                    st.success("Evidência removida.")
                    st.rerun()

        st.subheader("Anexar nova evidência")
        with st.form("evid_edit"):
            tipo = st.selectbox(
                "Tipo de evidência",
                ["certificado", "portaria", "ata", "email", "declaracao", "pdf", "imagem", "link", "material_didatico", "print", "outro"],
                key="ev_tipo_edit",
            )
            nome = st.text_input("Nome do arquivo (opcional)", key="ev_nome_edit")
            caminho = st.text_input("Caminho/URL (opcional)", key="ev_path_edit")
            descricao = st.text_area("Descrição (opcional)", height=80, key="ev_desc_edit")
            data_doc = st.date_input("Data do documento (opcional)", value=None, key="ev_data_doc_edit")
            obrig = st.checkbox("Obrigatória?", key="ev_obr_edit")
            aprov = st.checkbox("Aprovada?", key="ev_aprov_edit")
            salvar_ev = st.form_submit_button("Salvar evidência desta atividade")
            if salvar_ev:
                evidencias_repository.create(
                    conn,
                    {
                        "atividade_id": atv["id"],
                        "tipo": tipo,
                        "nome_arquivo": nome or None,
                        "caminho_arquivo": caminho or None,
                        "descricao": descricao or None,
                        "data_anexacao": datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S"),
                        "data_validade": data_doc.strftime("%Y-%m-%d") if data_doc else None,
                        "validade_status": None,
                        "obrigatoria": int(obrig),
                        "aprovada": int(aprov),
                    },
                )
                st.success("Evidência salva.")
                st.rerun()
    conn.close()

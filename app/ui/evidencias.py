import streamlit as st
from datetime import datetime

from app.ui.theme import apply_theme
from app.ui import components as ui
from app.db.connection import get_connection
from app.db.repositories import anos_repository, atividades_repository, evidencias_repository
from app.services.alertas_service import gerar_alertas


def evidencias_page():
    apply_theme()
    conn = get_connection()
    anos = anos_repository.list_all(conn)
    if not anos:
        st.error("Nenhum ano configurado.")
        return
    ano_row = anos[0]
    st.title("Evidências")
    atividades = atividades_repository.list_by_ano(conn, ano_row["id"])
    if not atividades:
        st.info("Cadastre atividades para anexar evidências.")
        conn.close()
        return

    atividade_map = {f"{a['titulo']} ({a['data_atividade']})": a for a in atividades}
    escolha = st.selectbox("Atividade", options=list(atividade_map.keys()))
    atividade = atividade_map[escolha]

    st.subheader("Anexar nova evidência")
    with st.form("form_evidencia"):
        tipo = st.selectbox(
            "Tipo de evidência",
            ["certificado", "portaria", "ata", "email", "declaracao", "pdf", "imagem", "link", "material_didatico", "print", "outro"],
        )
        nome = st.text_input("Nome do arquivo (opcional)")
        caminho = st.text_input("Caminho/URL (opcional)")
        descricao = st.text_area("Descrição (opcional)", height=80)
        data_anexacao = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")
        obrigatoria = st.checkbox("Obrigatória?", value=False)
        aprovada = st.checkbox("Aprovada?", value=False)
        submitted = st.form_submit_button("Salvar evidência")
        if submitted:
            evidencias_repository.create(
                conn,
                {
                    "atividade_id": atividade["id"],
                    "tipo": tipo,
                    "nome_arquivo": nome or None,
                    "caminho_arquivo": caminho or None,
                    "descricao": descricao or None,
                    "data_anexacao": data_anexacao,
                    "validade_status": None,
                    "obrigatoria": int(obrigatoria),
                    "aprovada": int(aprovada),
                },
            )
            gerar_alertas(conn, ano_row["id"])
            st.success("Evidência salva e pendências atualizadas.")

    st.markdown("---")
    st.subheader("Evidências da atividade")
    evidencias = evidencias_repository.list_by_atividade(conn, atividade["id"])
    if not evidencias:
        st.markdown('<div class="empty-state">Nenhuma evidência vinculada.</div>', unsafe_allow_html=True)
    else:
        data = [
            {
                "Tipo": e["tipo"],
                "Nome": e["nome_arquivo"] or "-",
                "Caminho": e["caminho_arquivo"] or "-",
                "Data inserção": e["data_anexacao"],
                "Data documento": e["data_validade"] or "-",
                "Obrigatória": "Sim" if e["obrigatoria"] else "Não",
                "Aprovada": "Sim" if e["aprovada"] else "Não",
            }
            for e in evidencias
        ]
        st.dataframe(data, use_container_width=True, hide_index=True)
    conn.close()

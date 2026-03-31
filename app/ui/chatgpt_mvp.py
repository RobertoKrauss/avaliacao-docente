import streamlit as st
from datetime import datetime

from app.ui.theme import apply_theme
from app.db.connection import get_connection
from app.db.repositories import (
    anos_repository,
    atividades_repository,
    alertas_repository,
    sugestoes_repository,
    config_repository,
)


def generate_stub(mode, ano, fator, atividade_id, texto):
    # Placeholder de geração consultiva (sem IA real)
    base = f"[MVP ChatGPT simulado] Modo: {mode}"
    if atividade_id:
        base += f" | Atividade {atividade_id}"
    elif fator:
        base += f" | Fator {fator}"
    base += f"\nResumo automático: {texto or 'Sem texto fornecido.'}"
    base += "\nSugestões: revise pendências, anexar evidências, confirmar pontuações."
    return base


def chatgpt_page():
    apply_theme()
    conn = get_connection()
    anos = anos_repository.list_all(conn)
    if not anos:
        st.error("Nenhum ano configurado.")
        return
    ano_row = anos[0]
    st.title("ChatGPT (MVP — consultivo)")
    st.caption("Apenas consultivo. Nenhuma ação é aplicada automaticamente ao banco.")

    # Controle de perfil
    usar_perfil = config_repository.get(conn, "usar_perfil_chatgpt")
    usar_perfil_bool = usar_perfil == "true"
    consent = st.checkbox("Usar meu perfil de escrita do ChatGPT (requer consentimento explícito)", value=usar_perfil_bool)
    config_repository.set(conn, "usar_perfil_chatgpt", "true" if consent else "false")
    st.info("Privacidade: apenas dados selecionados abaixo são usados; nenhuma sugestão altera o banco automaticamente.")
    st.markdown("---")

    modo = st.selectbox(
        "Modo de análise",
        ["analisar_ano", "analisar_fator", "analisar_atividade", "redacao_assistida"],
        format_func=lambda m: {
            "analisar_ano": "Análise do ano",
            "analisar_fator": "Análise por fator",
            "analisar_atividade": "Análise por atividade",
            "redacao_assistida": "Redação assistida",
        }[m],
    )

    fator = None
    atividade_id = None
    if modo == "analisar_fator":
        fator = st.selectbox("Fator", ["formacao", "funcional", "producao"])
    if modo == "analisar_atividade":
        atividades = atividades_repository.list_by_ano(conn, ano_row["id"])
        atividade_map = {f"{a['titulo']} ({a['id']})": a["id"] for a in atividades}
        atividade_id = st.selectbox("Atividade", list(atividade_map.keys())) if atividades else None
        atividade_id = atividade_map.get(atividade_id) if atividade_id else None

    prompt = st.text_area("Contexto/Texto (opcional)", height=120)
    if st.button("Gerar sugestão (simulada)"):
        texto = generate_stub(modo, ano_row["ano"], fator, atividade_id, prompt)
        st.markdown("### Sugestão gerada")
        st.code(texto)
        if st.button("Salvar sugestão"):
            sugestoes_repository.create(
                conn,
                {
                    "ano_id": ano_row["id"],
                    "atividade_id": atividade_id,
                    "fator": fator,
                    "tipo_sugestao": modo,
                    "titulo": f"Sugestão {modo}",
                    "texto": texto,
                    "origem_contexto": "perfil_chatgpt" if consent else "dados",
                    "aplicada_pelo_usuario": 0,
                },
            )
            st.success("Sugestão salva no banco.")

    st.markdown("---")
    st.subheader("Sugestões salvas")
    sugestoes = sugestoes_repository.list_by_ano(conn, ano_row["id"])
    if not sugestoes:
        st.caption("Nenhuma sugestão salva.")
    else:
        data = [
            {
                "Título": s["titulo"],
                "Tipo": s["tipo_sugestao"],
                "Fator": s["fator"] or "-",
                "Atividade": s["atividade_id"] or "-",
                "Origem": s["origem_contexto"] or "-",
            }
            for s in sugestoes
        ]
        st.dataframe(data, use_container_width=True, hide_index=True)
    conn.close()

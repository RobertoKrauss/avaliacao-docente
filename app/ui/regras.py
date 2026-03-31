import streamlit as st
from datetime import datetime

from app.ui.theme import apply_theme
from app.db.connection import get_connection
from app.db.repositories import regras_repository


def _preview_formula(tipo: str, valor_base, divisor, unidade, teto):
    if tipo == "fixo":
        return f"{valor_base or 0} pontos fixos"
    if tipo == "por_unidade":
        return f"{valor_base or 0} pontos por {unidade or 'unidade'}"
    if tipo == "por_hora":
        return f"{valor_base or 0} pontos a cada {divisor or 1} horas"
    if tipo in ("manual", "intervalo"):
        return "Valor manual definido pelo usuário"
    return "-"


def regras_page():
    apply_theme()
    conn = get_connection()
    st.title("Regras de Pontuação")
    tab_padrao, tab_pers, tab_nova = st.tabs(["Regras padrão", "Personalizadas", "Nova regra personalizada"])

    with tab_padrao:
        regras = regras_repository.list_padroes(conn)
        data = [
            {
                "Nome": r["nome"],
                "Fator": r["categoria_principal"],
                "Tipo": r["tipo_formula"],
                "Base": r["valor_base"] or "-",
                "Unidade": r["unidade"] or "-",
                "Teto": r["pontuacao_maxima"] or "-",
            }
            for r in regras
        ]
        st.dataframe(data, use_container_width=True, hide_index=True)

    with tab_pers:
        regras_pers = regras_repository.list_personalizadas(conn)
        if not regras_pers:
            st.markdown('<div class="empty-state">Nenhuma regra personalizada ainda.</div>', unsafe_allow_html=True)
        else:
            st.dataframe(
                [
                    {
                        "ID": r["id"],
                        "Nome": r["nome"],
                        "Fator": r["categoria_principal"],
                        "Tipo": r["tipo_formula"],
                        "Base": r["valor_base"] or "-",
                        "Unidade": r["unidade"] or "-",
                        "Teto": r["pontuacao_maxima"] or "-",
                        "Ativa": "Sim" if r["ativa"] else "Não",
                    }
                    for r in regras_pers
                ],
                use_container_width=True,
                hide_index=True,
            )

        col1, col2 = st.columns([3, 1])
        with col1:
            regra_id = st.selectbox(
                "Selecionar regra personalizada",
                options=[r["id"] for r in regras_pers] if regras_pers else [],
                format_func=lambda rid: next((r["nome"] for r in regras_pers if r["id"] == rid), ""),
            )
        with col2:
            st.write("")
            if st.button("Desativar", disabled=not regras_pers or not regra_id):
                regras_repository.desativar(conn, regra_id)
                st.success("Regra desativada.")
            if st.button("Duplicar", disabled=not regras_pers or not regra_id):
                regras_repository.duplicar(conn, regra_id)
                st.success("Regra duplicada.")

    with tab_nova:
        st.subheader("Criar nova regra personalizada")
        with st.form("form_regra"):
            nome = st.text_input("Nome da regra", max_chars=120)
            categoria = st.selectbox("Fator", ["formacao", "funcional", "producao"])
            subtipo = st.text_input("Subtipo (opcional)", max_chars=60)
            descricao = st.text_area("Descrição da regra")
            justificativa = st.text_area("Justificativa (obrigatória)")
            tipo = st.selectbox("Tipo de fórmula", ["fixo", "por_unidade", "por_hora", "intervalo", "manual"])
            valor_base = st.number_input("Valor base", min_value=0.0, step=0.5, value=0.0)
            unidade = st.text_input("Unidade (evento, hora, etc.)", value="") if tipo in ("por_unidade",) else st.text_input("Unidade (opcional)", value="")
            divisor = st.number_input("Divisor (aplicável para por_hora)", min_value=0.0, step=0.5, value=10.0) if tipo == "por_hora" else None
            teto = st.number_input("Pontuação máxima (opcional)", min_value=0.0, step=0.5, value=0.0)
            evidencia = st.text_input("Evidência necessária (opcional)")
            origem_doc = st.text_input("Origem do documento (opcional)")
            ativa = st.checkbox("Ativa", value=True)
            preview = _preview_formula(tipo, valor_base, divisor, unidade, teto if teto > 0 else None)
            st.caption(f"Prévia: {preview}")
            submitted = st.form_submit_button("Salvar regra")
            if submitted:
                try:
                    regras_repository.create_personalizada(
                        conn,
                        {
                            "nome": nome,
                            "categoria_principal": categoria,
                            "subtipo": subtipo or None,
                            "descricao_regra": descricao,
                            "justificativa": justificativa,
                            "tipo_formula": tipo,
                            "valor_base": valor_base if valor_base > 0 else None,
                            "unidade": unidade or None,
                            "divisor_unidade": divisor,
                            "pontuacao_maxima": teto or None,
                            "exige_valor_manual": 1 if tipo in ("manual", "intervalo") else 0,
                            "evidencia_necessaria": evidencia or None,
                            "origem_documento": origem_doc or None,
                            "ativa": 1 if ativa else 0,
                        },
                    )
                    st.success("Regra personalizada criada.")
                except ValueError as e:
                    st.error(str(e))
    conn.close()

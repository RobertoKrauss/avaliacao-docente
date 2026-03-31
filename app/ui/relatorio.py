import streamlit as st
import csv
import io
from app.ui.theme import apply_theme
from app.db.connection import get_connection
from app.db.repositories import (
    anos_repository,
    atividades_repository,
    alertas_repository,
    regras_repository,
    sugestoes_repository,
)


def build_markdown(conn, ano_row):
    ano_id = ano_row["id"]
    atividades = atividades_repository.list_by_ano(conn, ano_id)
    alertas_abertos = alertas_repository.list_filtered(conn, ano_id, resolvido=0)
    regras_pers_ids = {a["regra_id"] for a in atividades if a["regra_id"]} - {
        r["id"] for r in regras_repository.list_padroes(conn)
    }
    regras_pers = [r for r in regras_repository.list_personalizadas(conn) if r["id"] in regras_pers_ids]
    linhas = [f"# Relatório {ano_row['ano']}", ""]
    # resumo por fator
    fatores = {"formacao": "Formação", "funcional": "Funcional – Pedagógico", "producao": "Produção Institucional"}
    linhas.append("## Resumo por fator")
    for fkey, flabel in fatores.items():
        total_est = sum(a["pontuacao_estimada"] or 0 for a in atividades if a["fator"] == fkey)
        total_conf = sum(a["pontuacao_confirmada"] or 0 for a in atividades if a["fator"] == fkey)
        linhas.append(f"- **{flabel}**: estimada {total_est:.1f}, confirmada {total_conf:.1f}")
    linhas.append("")
    linhas.append("## Atividades do ano")
    for a in atividades:
        linhas.append(
            f"- {a['data_atividade']} — {a['titulo']} (fator {a['fator']}) | estimada {a['pontuacao_estimada'] or 0} | confirmada {a['pontuacao_confirmada'] or '-'}"
        )
    linhas.append("")
    linhas.append("## Pendências abertas")
    if not alertas_abertos:
        linhas.append("- Nenhuma pendência em aberto.")
    else:
        for al in alertas_abertos:
            linhas.append(f"- [{al['severidade']}] {al['tipo_alerta']}: {al['mensagem']}")
    linhas.append("")
    linhas.append("## Regras personalizadas usadas")
    if not regras_pers:
        linhas.append("- Nenhuma regra personalizada usada.")
    else:
        for r in regras_pers:
            linhas.append(f"- {r['nome']} ({r['categoria_principal']}) — {r['descricao_regra']}")
    linhas.append("")
    linhas.append("## Observações finais")
    linhas.append("_Adicione aqui suas observações._")
    return "\n".join(linhas)


def build_csv(conn, ano_row):
    ano_id = ano_row["id"]
    atividades = atividades_repository.list_by_ano(conn, ano_id)
    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow(["titulo", "data", "fator", "regra_id", "pontuacao_estimada", "pontuacao_confirmada", "status"])
    for a in atividades:
        writer.writerow(
            [
                a["titulo"],
                a["data_atividade"],
                a["fator"],
                a["regra_id"],
                a["pontuacao_estimada"] or 0,
                a["pontuacao_confirmada"] or "",
                a["status"],
            ]
        )
    return output.getvalue()


def relatorio_page():
    apply_theme()
    conn = get_connection()
    anos = anos_repository.list_all(conn)
    if not anos:
        st.error("Nenhum ano configurado.")
        return
    ano_row = anos[0]
    st.title("Relatório Anual")
    md = build_markdown(conn, ano_row)
    csv_data = build_csv(conn, ano_row)
    st.subheader("Prévia (Markdown)")
    st.markdown(md)
    st.download_button("Baixar Markdown", data=md.encode("utf-8"), file_name=f"relatorio_{ano_row['ano']}.md")
    st.download_button("Baixar CSV", data=csv_data.encode("utf-8"), file_name=f"atividades_{ano_row['ano']}.csv")
    conn.close()

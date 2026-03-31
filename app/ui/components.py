import streamlit as st
from typing import Dict, List
from app.ui.theme import PALETTE


def risk_badge(risco: str) -> str:
    cls = {"baixo": "low", "medio": "mid", "alto": "high"}.get(risco, "mid")
    return f'<span class="badge {cls}">{risco.upper()}</span>'


def factor_card(label: str, total: float, meta: float, risco: str, faltante: float) -> None:
    st.markdown(
        f"""
        <div class="card">
            <div style="display:flex;justify-content:space-between;align-items:center;">
                <div class="metric-title">{label}</div>
                {risk_badge(risco)}
            </div>
            <div style="font-size:2rem;font-weight:800;margin-top:8px;">{total:.1f} / {meta:.1f}</div>
            <div class="muted">Faltam {faltante:.1f} pontos</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def alerts_block(alertas: List[Dict]):
    st.subheader("Alertas e pendências prioritárias")
    if not alertas:
        st.markdown('<div class="empty-state">Nenhum alerta aberto.</div>', unsafe_allow_html=True)
        return
    data = [
        {
            "Tipo": a["tipo_alerta"],
            "Severidade": a["severidade"],
            "Mensagem": a["mensagem"],
            "Fator": a["fator"] or "-",
            "Atividade": a["atividade_id"] or "-",
        }
        for a in alertas
    ]
    st.dataframe(data, use_container_width=True, hide_index=True)


def activities_block(atividades):
    st.subheader("Atividades recentes")
    if not atividades:
        st.markdown('<div class="empty-state">Nenhuma atividade cadastrada no ano.</div>', unsafe_allow_html=True)
        return
    data = [
        {
            "Título": a["titulo"],
            "Fator": a["fator"],
            "Regra": a["regra_id"] or "-",
            "Estimado": a["pontuacao_estimada"] or 0,
            "Status": a["status"],
            "Data": a["data_atividade"],
        }
        for a in atividades[:8]
    ]
    st.dataframe(data, use_container_width=True, hide_index=True)


def suggestions_block(sugestoes):
    st.subheader("Sugestões do ChatGPT (leitura)")
    if not sugestoes:
        st.markdown('<div class="empty-state">Nenhuma sugestão registrada ainda.</div>', unsafe_allow_html=True)
        return
    data = [
        {
            "Título": s["titulo"],
            "Tipo": s["tipo_sugestao"],
            "Fator": s["fator"] or "-",
            "Atividade": s["atividade_id"] or "-",
        }
        for s in sugestoes[:5]
    ]
    st.dataframe(data, use_container_width=True, hide_index=True)

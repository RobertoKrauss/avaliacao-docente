import sqlite3
from typing import Dict

THRESHOLDS = {
    "baixo": 0.8,
    "medio": 0.5,
}


def calcular_risco_por_fator(conn: sqlite3.Connection, ano_id: int) -> Dict[str, str]:
    metas = conn.execute(
        "SELECT meta_formacao, meta_funcional, meta_producao FROM anos_avaliacao WHERE id = ?",
        (ano_id,),
    ).fetchone()
    if not metas:
        return {}

    soma = conn.execute(
        """
        SELECT fator, COALESCE(SUM(pontuacao_estimada), 0) as total
        FROM atividades
        WHERE ano_id = ? AND deleted_at IS NULL
        GROUP BY fator
        """,
        (ano_id,),
    ).fetchall()
    totals = {row["fator"]: row["total"] for row in soma}

    riscos = {}
    for fator, meta in [
        ("formacao", metas["meta_formacao"]),
        ("funcional", metas["meta_funcional"]),
        ("producao", metas["meta_producao"]),
    ]:
        valor = totals.get(fator, 0)
        perc = (valor / meta) if meta else 0
        if perc >= THRESHOLDS["baixo"]:
            risco = "baixo"
        elif perc >= THRESHOLDS["medio"]:
            risco = "medio"
        else:
            risco = "alto"
        riscos[fator] = risco
    return riscos

import sqlite3
from typing import Dict

from app.db.repositories import atividades_repository
from app.services.calculo_pontuacao import Regra, calcular_pontuacao
from app.services.calculo_risco import calcular_risco_por_fator
from app.services.alertas_service import gerar_alertas


def recalcular_pontuacoes(conn: sqlite3.Connection, ano_id: int) -> Dict[str, float]:
    atividades = atividades_repository.list_by_ano(conn, ano_id)
    soma_por_fator = {"formacao": 0.0, "funcional": 0.0, "producao": 0.0}
    with conn:
        for a in atividades:
            if not a["regra_id"]:
                continue
            regra_row = conn.execute(
                "SELECT tipo_formula, valor_base, divisor_unidade, pontuacao_maxima, exige_valor_manual "
                "FROM regras_pontuacao WHERE id = ?",
                (a["regra_id"],),
            ).fetchone()
            if not regra_row:
                continue
            regra = Regra(
                tipo_formula=regra_row["tipo_formula"],
                valor_base=regra_row["valor_base"],
                divisor_unidade=regra_row["divisor_unidade"],
                pontuacao_maxima=regra_row["pontuacao_maxima"],
                exige_valor_manual=regra_row["exige_valor_manual"],
            )
            try:
                valor = calcular_pontuacao(
                    regra,
                    quantidade=a["quantidade"],
                    carga_horaria=a["carga_horaria"],
                    valor_manual=a["valor_manual"],
                )
            except ValueError:
                valor = None

            if valor is not None:
                soma_por_fator[a["fator"]] = soma_por_fator.get(a["fator"], 0) + valor
                conn.execute(
                    """
                    UPDATE atividades
                    SET pontuacao_estimada = ?, pontuacao_original = COALESCE(pontuacao_original, ?), updated_at = CURRENT_TIMESTAMP
                    WHERE id = ?
                    """,
                    (valor, valor, a["id"]),
                )
    riscos = calcular_risco_por_fator(conn, ano_id)
    gerar_alertas(conn, ano_id)
    return {"soma_por_fator": soma_por_fator, "riscos": riscos}

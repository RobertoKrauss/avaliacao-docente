from datetime import datetime, timedelta
import sqlite3
from typing import Dict, List

from app.db.repositories import (
    alertas_repository,
    atividades_repository,
    evidencias_repository,
    checkins_repository,
)
from app.services.calculo_risco import calcular_risco_por_fator


TIPOS_PENDENCIA = {
    "atividade_sem_evidencia": "Atividade sem evidência anexada.",
    "atividade_sem_regra": "Atividade sem regra de pontuação.",
    "atividade_sem_fator": "Atividade sem fator definido.",
    "valor_manual_faltante": "Valor manual obrigatório não preenchido.",
    "potencial_nao_explorado": "Atividade marcada com potencial não explorado.",
}


def detectar_pendencias(conn: sqlite3.Connection, ano_id: int) -> List[Dict]:
    pendencias = []
    atividades = atividades_repository.list_by_ano(conn, ano_id)
    for a in atividades:
        evidencias = evidencias_repository.list_by_atividade(conn, a["id"])
        if not a["fator"]:
            pendencias.append({"atividade_id": a["id"], "tipo": "atividade_sem_fator"})
        if a["regra_id"] is None:
            pendencias.append({"atividade_id": a["id"], "tipo": "atividade_sem_regra"})
        if a["regra_id"] and a["valor_manual"] is None and a["regra_id"]:
            # para regras manual/intervalo, checaremos tipo abaixo
            pass
        # Se regra exigir valor manual
        if a["regra_id"]:
            regra = conn.execute(
                "SELECT tipo_formula, exige_valor_manual FROM regras_pontuacao WHERE id = ?",
                (a["regra_id"],),
            ).fetchone()
            if regra and regra["tipo_formula"] in ("manual", "intervalo") and a["valor_manual"] is None:
                pendencias.append({"atividade_id": a["id"], "tipo": "valor_manual_faltante"})
        if not evidencias:
            pendencias.append({"atividade_id": a["id"], "tipo": "atividade_sem_evidencia"})
        if a["possui_potencial_nao_explorado"]:
            pendencias.append({"atividade_id": a["id"], "tipo": "potencial_nao_explorado"})
    return pendencias


def limpar_alertas_auto(conn: sqlite3.Connection, ano_id: int) -> None:
    with conn:
        conn.execute(
            "DELETE FROM alertas WHERE ano_id = ? AND tipo_alerta IN "
            "('atividade_sem_evidencia','atividade_sem_regra','atividade_sem_fator',"
            "'valor_manual_faltante','risco_alto','pontuacao_baixa','revisao_atrasada','potencial_nao_explorado')",
            (ano_id,),
        )


def gerar_alertas(conn: sqlite3.Connection, ano_id: int) -> None:
    limpar_alertas_auto(conn, ano_id)
    riscos = calcular_risco_por_fator(conn, ano_id)
    pendencias = detectar_pendencias(conn, ano_id)
    now = datetime.utcnow()

    for p in pendencias:
        tipo = p["tipo"]
        msg = TIPOS_PENDENCIA.get(tipo, "Pendência identificada.")
        sev = "media" if tipo == "atividade_sem_evidencia" else "baixa"
        alertas_repository.create_alert(
            conn,
            ano_id,
            tipo_alerta=tipo,
            severidade=sev,
            mensagem=msg,
            atividade_id=p["atividade_id"],
        )

    for fator, risco in riscos.items():
        if risco == "alto":
            alertas_repository.create_alert(
                conn,
                ano_id,
                tipo_alerta="risco_alto",
                severidade="alta",
                mensagem=f"Risco alto no fator {fator}.",
                fator=fator,
            )
        elif risco == "medio":
            alertas_repository.create_alert(
                conn,
                ano_id,
                tipo_alerta="pontuacao_baixa",
                severidade="media",
                mensagem=f"Pontuação ainda em progresso no fator {fator}.",
                fator=fator,
            )

    ultimo_checkin = checkins_repository.list_by_ano(conn, ano_id)
    if ultimo_checkin:
        data = datetime.fromisoformat(ultimo_checkin[0]["data_checkin"])
        if (now - data) > timedelta(days=30):
            alertas_repository.create_alert(
                conn,
                ano_id,
                tipo_alerta="revisao_atrasada",
                severidade="media",
                mensagem="Há mais de 30 dias sem check-in/revisão.",
            )
    else:
        alertas_repository.create_alert(
            conn,
            ano_id,
            tipo_alerta="revisao_atrasada",
            severidade="media",
            mensagem="Nenhum check-in registrado para o ano.",
        )

from datetime import datetime
import sqlite3
from typing import List, Optional


def list_padroes(conn: sqlite3.Connection) -> List[sqlite3.Row]:
    return conn.execute(
        "SELECT * FROM regras_pontuacao WHERE origem = 'padrao' AND deleted_at IS NULL ORDER BY categoria_principal, nome"
    ).fetchall()


def list_personalizadas(conn: sqlite3.Connection) -> List[sqlite3.Row]:
    return conn.execute(
        "SELECT * FROM regras_pontuacao WHERE origem = 'personalizada' AND deleted_at IS NULL ORDER BY created_at DESC"
    ).fetchall()


def list_personalizadas_ativas(conn: sqlite3.Connection) -> List[sqlite3.Row]:
    return conn.execute(
        "SELECT * FROM regras_pontuacao WHERE origem = 'personalizada' AND deleted_at IS NULL AND ativa = 1 ORDER BY created_at DESC"
    ).fetchall()


def get(conn: sqlite3.Connection, regra_id: int) -> Optional[sqlite3.Row]:
    return conn.execute(
        "SELECT * FROM regras_pontuacao WHERE id = ? AND deleted_at IS NULL", (regra_id,)
    ).fetchone()


def create_personalizada(conn: sqlite3.Connection, data: dict) -> int:
    now = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")
    if data.get("justificativa") is None or str(data.get("justificativa")).strip() == "":
        raise ValueError("Justificativa é obrigatória para regra personalizada.")
    payload = {
        "nome": data["nome"],
        "categoria_principal": data["categoria_principal"],
        "subtipo": data.get("subtipo"),
        "origem": "personalizada",
        "descricao_regra": data["descricao_regra"],
        "justificativa": data.get("justificativa"),
        "tipo_formula": data["tipo_formula"],
        "valor_base": data.get("valor_base"),
        "unidade": data.get("unidade"),
        "divisor_unidade": data.get("divisor_unidade"),
        "pontuacao_maxima": data.get("pontuacao_maxima"),
        "exige_valor_manual": data.get("exige_valor_manual", 0),
        "evidencia_necessaria": data.get("evidencia_necessaria"),
        "origem_documento": data.get("origem_documento"),
        "ativa": data.get("ativa", 1),
        "observacoes": data.get("observacoes"),
        "created_at": now,
        "updated_at": now,
    }
    cols = ", ".join(payload.keys())
    placeholders = ", ".join(["?"] * len(payload))
    with conn:
        cur = conn.execute(
            f"INSERT INTO regras_pontuacao ({cols}) VALUES ({placeholders})",
            tuple(payload.values()),
        )
    return cur.lastrowid


def update_personalizada(conn: sqlite3.Connection, regra_id: int, updates: dict) -> None:
    updates = {k: v for k, v in updates.items() if k not in ("id", "origem")}
    if not updates:
        return
    updates["updated_at"] = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")
    sets = ", ".join([f"{k} = ?" for k in updates.keys()])
    params = list(updates.values()) + [regra_id]
    with conn:
        conn.execute(f"UPDATE regras_pontuacao SET {sets} WHERE id = ?", params)


def desativar(conn: sqlite3.Connection, regra_id: int) -> None:
    with conn:
        conn.execute(
            "UPDATE regras_pontuacao SET ativa = 0, updated_at = ? WHERE id = ?",
            (datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S"), regra_id),
        )


def duplicar(conn: sqlite3.Connection, regra_id: int) -> int:
    row = get(conn, regra_id)
    if not row:
        raise ValueError("Regra não encontrada para duplicação.")
    data = dict(row)
    data.pop("id", None)
    data["nome"] = data["nome"] + " (cópia)"
    data["origem"] = "personalizada"
    return create_personalizada(conn, data)

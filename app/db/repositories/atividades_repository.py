from datetime import datetime
import sqlite3
from typing import List, Optional, Dict, Any


def create(conn: sqlite3.Connection, data: Dict[str, Any]) -> int:
    now = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")
    payload = {
        "created_at": now,
        "updated_at": now,
        "item_negociado": data.get("item_negociado", 0),
        "possui_potencial_nao_explorado": data.get("possui_potencial_nao_explorado", 0),
        **data,
    }
    cols = ", ".join(payload.keys())
    placeholders = ", ".join(["?"] * len(payload))
    with conn:
        cur = conn.execute(
            f"INSERT INTO atividades ({cols}) VALUES ({placeholders})",
            tuple(payload.values()),
        )
    return cur.lastrowid


def update(conn: sqlite3.Connection, atividade_id: int, updates: Dict[str, Any]) -> None:
    updates = {k: v for k, v in updates.items() if k != "id"}
    if not updates:
        return
    updates["updated_at"] = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")
    sets = ", ".join([f"{k} = ?" for k in updates.keys()])
    params = list(updates.values()) + [atividade_id]
    with conn:
        conn.execute(f"UPDATE atividades SET {sets} WHERE id = ?", params)


def soft_delete(conn: sqlite3.Connection, atividade_id: int) -> None:
    with conn:
        conn.execute(
            "UPDATE atividades SET deleted_at = ?, updated_at = ? WHERE id = ?",
            (datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S"), datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S"), atividade_id),
        )


def get(conn: sqlite3.Connection, atividade_id: int) -> Optional[sqlite3.Row]:
    return conn.execute(
        "SELECT * FROM atividades WHERE id = ? AND deleted_at IS NULL", (atividade_id,)
    ).fetchone()


def list_by_ano(conn: sqlite3.Connection, ano_id: int) -> List[sqlite3.Row]:
    return conn.execute(
        "SELECT * FROM atividades WHERE ano_id = ? AND deleted_at IS NULL ORDER BY data_atividade DESC, created_at DESC",
        (ano_id,),
    ).fetchall()


def list_filtered(conn: sqlite3.Connection, ano_id: int, fator: Optional[str] = None, status: Optional[str] = None, regra_id: Optional[int] = None) -> List[sqlite3.Row]:
    query = "SELECT * FROM atividades WHERE ano_id = ? AND deleted_at IS NULL"
    params = [ano_id]
    if fator:
        query += " AND fator = ?"
        params.append(fator)
    if status:
        query += " AND status = ?"
        params.append(status)
    if regra_id:
        query += " AND regra_id = ?"
        params.append(regra_id)
    query += " ORDER BY data_atividade DESC"
    return conn.execute(query, tuple(params)).fetchall()
